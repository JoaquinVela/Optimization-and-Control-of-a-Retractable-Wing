import math

from src.control.control import altitudeHoldController
from src.models.aero import aerodynamicState
from src.models.geometry import wingGeometry
from src.models.plane import planeProperties
from src.models.aero_c import aero
from src.simulation.flightSim import flightSimulation

FT_PER_METER = 3.28084
Q_SCHEDULING_LIMIT_PA = 20000
Q_STRUCTURAL_LIMIT_PA = 25000
ENVELOPE_DYNAMIC_PRESSURE_PA = 50000
MAX_STAGNATION_TEMPERATURE_K = 390
TEMP_GRADIENT_K_PER_M = -0.0065

class Simulation:
    def __init__(self):
        wing = wingGeometry(span=64.8, chord=6.98, deployment = 0.50)

        aero_state = aerodynamicState(
            rho=0.380,
            velocity=289,
            wing=wing,
            cl0=0.2,
            cd0=0.02,
            alphaRad=0.075,
        )

        mass = 274669.280707
        max_thrust = 1026000
        plane = planeProperties(mass)

        controller = altitudeHoldController(
            trimAlphaRad=aero_state.alphaRad,
            targetAltitude=12496.8,
        )

        self.sim = flightSimulation(
            aeroState=aero_state,
            plane=plane,
            controller=controller,
            maxThrust=max_thrust,
            altitude=12496.8,
            velocityY=0,
        )

        self.time_s = 0.0
        self.max_thrust = max_thrust
        self.auto_optimization_enabled = True
        self.manual_target_altitude_m = controller.targetAltitude
        self.manual_deployment = wing.deployment
        self.manual_thrust_fraction = 0.25

    def step(self, dt):
        self.sim.step(
            self.time_s, 
            dt,
            autoOptimization=self.auto_optimization_enabled,
            manualTargetAltitude=self.manual_target_altitude_m,
            manualDeployment=self.manual_deployment,
            manualThrustFraction=self.manual_thrust_fraction,
        )
        self.time_s += dt

        return self._create_sample()

    def _create_sample(self):
        altitude_m = self.sim.altitude
        altitude_ft = altitude_m * FT_PER_METER
        velocity_mps = self.sim.totalVelocity()
        mach = self.sim.machHistory[-1]
        cutoff_altitude_m = self.sim.cutoffAltitudeHistory[-1]

        dynamic_pressure = self.sim.aeroOutput.dynamic_pressure
        dynamic_pressure_usage_percent = 100 * dynamic_pressure / Q_SCHEDULING_LIMIT_PA

        temperature_k = aero.temperature_at_altitude(altitude_m)
        stagnation_temperature_k = temperature_k * (1 + 0.2 * mach**2)
        max_stagnation_temperature_k = MAX_STAGNATION_TEMPERATURE_K
        thermal_usage_percent = (
            100 * stagnation_temperature_k / max_stagnation_temperature_k
        )

        alpha_rad = self.sim.alphaRadHistory[-1]
        alpha_usage_percent = 100 * abs(alpha_rad) / self.sim.controller.maxAlphaRad
        structural_q_usage_percent = 100 * dynamic_pressure / Q_STRUCTURAL_LIMIT_PA
        structural_usage_percent = max(structural_q_usage_percent, alpha_usage_percent)

        lift = self.sim.liftHistory[-1]
        drag = self.sim.dragHistory[-1]
        thrust = self.sim.thrustHistory[-1]
        acc_x = self.sim.accXHistory[-1]

        boom_minimum_m = (
            self.sim.scheduler.boomless.minCutoffAltitudeAGL
            + self.sim.scheduler.boomlessSafetyMargin
        )
        boom_margin_m = cutoff_altitude_m - boom_minimum_m
        boom_usage_percent = 100 * boom_minimum_m / max(cutoff_altitude_m, 1)

        thrust_percent = 100 * thrust / self.max_thrust
        lift_to_drag = lift / drag if drag != 0 else 0

        prediction_seconds = 60
        predicted_velocity_mps = max(0, velocity_mps + acc_x * prediction_seconds)
        speed_of_sound = aero.speed_of_sound(temperature_k)
        potential_mach = aero.mach_number(speed_of_sound, predicted_velocity_mps)

        target_altitude_m = self.sim.targetAltitudeHistory[-1]
        recommended_altitude_change_ft = (
            target_altitude_m - altitude_m
        ) * FT_PER_METER

        min_deployment = self.sim.scheduler.minDeployment
        current_deployment = self.sim.wing.deployment
        recommended_deployment_change_percent = (
            min_deployment - current_deployment
        ) * 100

        target_thrust = self.sim.thrustController.command(
            requestedThrust=self.sim.thrustController.requestedThrustForAltitude(
                currentAltitude=altitude_m,
                targetAltitude=target_altitude_m,
            ),
            currentAltitude=altitude_m,
            targetAltitude=target_altitude_m,
        )
        recommended_thrust_change_percent = (
            100 * (target_thrust - thrust) / self.max_thrust
        )

        optimizer_target = getattr(self.sim, "optimizerTarget", None)

        if optimizer_target is not None:
            optimizer_reason = optimizer_target.reason
            optimizer_predicted_mach = optimizer_target.predictedMach
        else:
            optimizer_reason = "NO OPTIMIZER TARGET"
            optimizer_predicted_mach = potential_mach

        return {
            "mach": mach,
            "altitude_ft": altitude_ft,
            "velocity_mps": velocity_mps,
            "deployment": current_deployment,
            "alpha_deg": math.degrees(alpha_rad),
            "lift_to_drag": lift_to_drag,
            "boom_margin_m": boom_margin_m,
            "thrust_percent": thrust_percent,

            "thermal_usage_percent": thermal_usage_percent,
            "dynamic_pressure_usage_percent": dynamic_pressure_usage_percent,
            "structural_usage_percent": structural_usage_percent,
            "engine_usage_percent": thrust_percent,
            "boom_usage_percent": boom_usage_percent,
            "thrust_usage_percent": thrust_percent,

            "potential_mach": potential_mach,
            "recommended_altitude_change_ft": recommended_altitude_change_ft,
            "recommended_deployment_change_percent": recommended_deployment_change_percent,
            "recommended_thrust_change_percent": recommended_thrust_change_percent,
            "supersonic_envelope": self._create_supersonic_envelope(),
            "auto_optimization_enabled": self.auto_optimization_enabled,
            "manual_target_altitude_ft": self.manual_target_altitude_m * FT_PER_METER,
            "manual_deployment": self.manual_deployment,
            "manual_thrust_percent": self.manual_thrust_fraction * 100,
            "optimizer_reason": optimizer_reason,
            "optimizer_predicted_mach": optimizer_predicted_mach,
        }
    
    def _create_supersonic_envelope(self):
        mach_values = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
        max_altitude_m = self.sim.scheduler.maxAltitude

        lower_boundary = []
        upper_boundary = []

        for mach in mach_values:
            lower_altitude_m = self._minimum_safe_altitude_for_mach(mach)

            if lower_altitude_m is None:
                continue

            lower_boundary.append((mach, lower_altitude_m * FT_PER_METER))
            upper_boundary.append((mach, max_altitude_m * FT_PER_METER))

        return lower_boundary + list(reversed(upper_boundary))
    
    def _minimum_safe_altitude_for_mach(self, mach):
        min_altitude_m = 0
        max_altitude_m = self.sim.scheduler.maxAltitude

        if not self._is_envelope_point_safe(max_altitude_m, mach):
            return None
        
        low = min_altitude_m
        high = max_altitude_m

        for _ in range(30):
            mid = 0.5 * (low + high)

            if self._is_envelope_point_safe(mid, mach):
                high = mid
            else:
                low = mid

        return high
    
    def _is_envelope_point_safe(self, altitude_m, mach):
        temperature_k = aero.temperature_at_altitude(altitude_m)
        speed_of_sound = aero.speed_of_sound(temperature_k)
        velocity_mps = mach * speed_of_sound

        rho = aero.air_density_at_altitude(altitude_m)
        dynamic_pressure = aero.dynamic_pressure(rho, velocity_mps)

        stagnation_temperature_k = temperature_k * (1 + 0.2 * mach**2)

        cutoff_altitude_m = aero.cutoff_altitude_agl(
            altitude_m,
            mach,
            TEMP_GRADIENT_K_PER_M,
        )

        minimum_cutoff_altitude_m = (
            self.sim.scheduler.boomless.minCutoffAltitudeAGL
            + self.sim.scheduler.boomlessSafetyMargin
        )

        return (
            mach >= 1.0
            and dynamic_pressure <= ENVELOPE_DYNAMIC_PRESSURE_PA
            and stagnation_temperature_k <= MAX_STAGNATION_TEMPERATURE_K
            and cutoff_altitude_m >= minimum_cutoff_altitude_m
        )
    
    def toggle_auto_optimization(self):
        self.auto_optimization_enabled = not self.auto_optimization_enabled

        if not self.auto_optimization_enabled:
            self.manual_target_altitude_m = self.sim.altitude
            self.manual_deployment = self.sim.wing.deployment
            self.manual_thrust_fraction = self.sim.thrust / self.max_thrust

    def adjust_manual_altitude_ft(self, delta_ft):
        self.manual_target_altitude_m += delta_ft / FT_PER_METER
        self.manual_target_altitude_m = aero.clamp(
            self.manual_target_altitude_m, 0.0, self.sim.scheduler.maxAltitude,
        )

    def adjust_manual_deployment(self, delta):
        self.manual_deployment = aero.clamp(
            self.manual_deployment + delta,
            self.sim.scheduler.minDeployment,
            self.sim.scheduler.maxDeployment,
        )

    def adjust_manual_thrust_percent(self, delta_percent):
        self.manual_thrust_fraction = aero.clamp(
            self.manual_thrust_fraction + delta_percent / 100,
            0.0,
            1.0
        )