import ctypes
from dataclasses import dataclass
from src.models.aero_c import aero, AeroInput, AeroOutput

@dataclass
class speedOptimizationTarget:
    targetAltitude: float
    targetDeployment: float
    targetThrustFraction: float
    predictedMach: float
    reason: str

class speedOptimizer:
    def __init__(
            self,
            maxThrustFraction=0.25,
            qLimitPa=20000,
            qSafetyFactor=0.98,
            maxStagnationTemperatureK=390,
            tempGradient=-0.0065,
            predictionTime=60,
    ):
        self.maxThrustFraction = maxThrustFraction
        self.qLimitPa = qLimitPa
        self.qSafetyFactor = qSafetyFactor
        self.maxStagnationTemperatureK = maxStagnationTemperatureK
        self.tempGradient = tempGradient
        self.predictionTime = predictionTime

    def chooseTarget(
            self,
            altitude,
            velocity,
            deployment,
            aeroState,
            plane,
            controller,
            wing,
            maxAltitude,
            maxThrust,
    ):
        bestTarget = None
        bestScore = None

        altitudeCandidates = [
            altitude,
            altitude + 100,
            altitude + 250,
            altitude + 500,
        ]

        deploymentCandidates = [
            deployment,
            deployment - 0.002,
            deployment - 0.005,
            deployment + 0.002,
        ]

        thrustCandidates = [
            0.20,
            0.225,
            self.maxThrustFraction
        ]

        for targetAltitude in altitudeCandidates:
            targetAltitude = aero.clamp(targetAltitude, 0.0, maxAltitude)

            for targetDeploymnet in deploymentCandidates:
                targetDeployment = aero.clamp(targetDeploymnet, 0.3, 1.0)

                for thrustFraction in thrustCandidates:
                    candidate = self._evaluateCandidate(
                        altitude=targetAltitude,
                        velocity=velocity,
                        deployment=targetDeployment,
                        thrustFraction=thrustFraction,
                        aeroState=aeroState,
                        plane=plane,
                        controller=controller,
                        wing=wing,
                        maxThrust=maxThrust
                    )

                    if candidate is None:
                        continue

                    score = self._scoreCandidate(candidate, deployment)

                    if bestScore is None or score > bestScore:
                        bestScore = score
                        bestTarget = candidate
                    
        if bestTarget is None:
            return speedOptimizationTarget(
                targetAltitude=min(altitude + 500, maxAltitude),
                targetDeployment=deployment,
                targetThrustFraction=0.0,
                predictedMach=0.0,
                reason="NO SAFE SPEED-UP CANDIDATE"
            )
        
        return bestTarget
    
    def _evaluateCandidate(
            self,
            altitude,
            velocity,
            deployment,
            thrustFraction,
            aeroState,
            plane,
            controller,
            wing,
            maxThrust,
    ):
        temperature = aero.temperature_at_altitude(altitude)
        speedOfSound = aero.speed_of_sound(temperature)
        mach = aero.mach_number(speedOfSound, velocity)
        rho = aero.air_density_at_altitude(altitude)
        dynamicPressure = aero.dynamic_pressure(rho, velocity)

        qSafeLimit = self.qLimitPa * self.qSafetyFactor

        if dynamicPressure > qSafeLimit:
            return None

        stagnationTemperature = temperature * (1 + 0.2 * mach**2)
        
        cutoffAltitude = aero.cutoff_altitude_agl(
            altitude,
            mach,
            self.tempGradient,
        )

        minimumCutoffAltitude = 130

        exposedWingArea = deployment * wing.area()

        requiredAlpha = aero.dynamic_trim_alpha(
            plane.weight(),
            rho,
            velocity,
            exposedWingArea,
            aeroState.cl0,
        )

        maxUsableAlpha = controller.maxAlphaRad - 0.02
        
        if stagnationTemperature > self.maxStagnationTemperatureK:
            return None
        
        if cutoffAltitude < minimumCutoffAltitude:
            return None
        
        if requiredAlpha > maxUsableAlpha:
            return None
        
        if exposedWingArea <= 0:
            return None
        
        aspectRatio = wing.span**2 / exposedWingArea

        aeroInput = AeroInput()
        aeroOutput = AeroOutput()

        aeroInput.rho = rho
        aeroInput.velocity = velocity
        aeroInput.wing_area = exposedWingArea
        aeroInput.aspect_ratio = aspectRatio
        aeroInput.cl0 = aeroState.cl0
        aeroInput.cd0 = aeroState.cd0
        aeroInput.alpha_rad = requiredAlpha
        aeroInput.oswald_efficiency = aeroState.oswaldEfficiency
        aeroInput.mach = mach
        aeroInput.mass = plane.mass
        aeroInput.thrust = thrustFraction * maxThrust

        aero.calculate_aero_state(
            ctypes.byref(aeroInput),
            ctypes.byref(aeroOutput),
        )

        predictedVelocity = max(0.0, velocity + aeroOutput.acc_x * self.predictionTime)

        predictedDynamicPressure = aero.dynamic_pressure(rho, predictedVelocity)

        if predictedDynamicPressure > qSafeLimit:
            return None

        predictedMach = aero.mach_number(speedOfSound, predictedVelocity)

        return speedOptimizationTarget(
            targetAltitude=altitude,
            targetDeployment=deployment,
            targetThrustFraction=thrustFraction,
            predictedMach=predictedMach,
            reason="MAX PREDICTED MACH WITHIN CONSTRAINTS"
        )
    
    def _scoreCandidate(self, candidate, currentDeployment):
        deploymentPenalty = 0.02 * abs(candidate.targetDeployment - currentDeployment)
        thrustPenalty = 0.01 * candidate.targetThrustFraction 

        return (
            candidate.predictedMach
            - deploymentPenalty
            - thrustPenalty
        )
