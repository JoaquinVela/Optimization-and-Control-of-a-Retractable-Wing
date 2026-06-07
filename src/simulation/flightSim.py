"""
flightSim.py

Basic flight simulator for a retractable wing optimization project.

This file contains reusable functions for:
- TBD
"""
import ctypes
from src.models.forces import aerodynamicsForce
from src.models.performance import aerodynamicPerformance
from src.control.cruiseScheduler import cruiseSchedule
from src.control.thrustController import thrustControl
from src.models.aero_c import aero, AeroInput, AeroOutput

class flightSimulation:
    def __init__(self, aeroState, plane, controller, maxThrust, altitude, velocityY=0, maxThrustRateFraction=0.05, cruisePowerLimit=0.25):
        self.aeroState = aeroState
        self.plane = plane
        self.controller = controller
        self.maxThrust = maxThrust
        self.requestedThrust = self.maxThrust
        self.thrust = 0.25 * self.maxThrust
        self.thrustController = thrustControl(
            self.maxThrust,
            cruisePowerLimit=cruisePowerLimit
        )
        self.altitude = altitude
        self.velocity = aeroState.velocity
        self.velocityY = velocityY
        self.positionX = 0
        self.maxThrustRateFraction = maxThrustRateFraction

        self.scheduler = cruiseSchedule(targetAltitude=controller.targetAltitude)
        self.wing = self.aeroState.wing
        self.aeroInput = AeroInput()
        self.aeroOutput = AeroOutput()

        self.timeHistory = []
        self.altitudeHistory = []
        self.positionXHistory = []
        self.totalVelocityHistory = []
        self.velocityHistory = []
        self.velocityYHistory = []
        self.alphaRadHistory = []
        self.clHistory = []
        self.liftHistory = []
        self.dragHistory = []
        self.weightHistory = []
        self.thrustHistory = []
        self.netXHistory = []
        self.netYHistory = []
        self.accXHistory = []
        self.accYHistory = []
        self.machHistory = []
        self.cutoffAltitudeHistory = []
        self.deploymentHistory = []
        self.targetAltitudeHistory = []

    def totalVelocity(self):
        return (self.velocity**2 + self.velocityY**2) ** 0.5

    def step(self, time, dt, autoOptimization=True, manualTargetAltitude=None, manualDeployment=None, manualThrustFraction=None):
        # 1 Update aerostate
        totalVelocity = self.totalVelocity()
        self.aeroState.rho = aero.air_density_at_altitude(self.altitude)
        self.aeroState.velocity = totalVelocity

        # 2 Ask scheduler for altitide and wing deployment targets
        targetAltitude, targetDeployment, mach = self.scheduler.chooseTarget(
            self.altitude,
            totalVelocity,
            self.wing.deployment
        )

        if not autoOptimization:
            if manualTargetAltitude is not None:
                targetAltitude = manualTargetAltitude

            if manualDeployment is not None:
                targetDeployment = manualDeployment

        cutoffAltitude = aero.cutoff_altitude_agl(
            self.altitude,
            mach,
            -0.0065
        )

        boomlessHardLimit = (
            self.scheduler.boomless.minCutoffAltitudeAGL + self.scheduler.boomlessSafetyMargin
        )

        boomlessSoftLimit = (
            self.scheduler.boomless.minCutoffAltitudeAGL + 3.0 * self.scheduler.boomlessSafetyMargin
        )

        if cutoffAltitude < boomlessSoftLimit:
            boomlessFraction = (
                (cutoffAltitude - boomlessHardLimit) / (boomlessSoftLimit - boomlessHardLimit)
            )
            boomlessFraction = aero.clamp(boomlessFraction, 0.0, 1.0)
        else:
            boomlessFraction = 1.0

        proposedArea = targetDeployment * self.wing.area()
        
        requiredAlphaRad = aero.dynamic_trim_alpha(
            self.plane.weight(),
            self.aeroState.rho,
            totalVelocity,
            proposedArea,
            self.aeroState.cl0
        )

        alphaMargin = 0.02
        maxUsableAlphaRad = self.controller.maxAlphaRad - alphaMargin

        if requiredAlphaRad > maxUsableAlphaRad:
            targetDeployment = self.wing.deployment

        self.aeroState.mach = mach
        self.controller.targetAltitude = targetAltitude

        # 3 Apply wing geometry change
        self.wing.setDeployment(targetDeployment)

        # 4 Controller decides new angle of attack
        newAlphaRad = self.controller.command(
            currentAltitude=self.altitude,
            currentVelocityY=self.velocityY,
            aeroState=self.aeroState,
            plane=self.plane
        )

        maxAlphaRate = 0.01 # rad/s
        maxAlphaChange = maxAlphaRate * dt

        newAlphaRad = aero.rate_limit(
            self.aeroState.alphaRad,
            newAlphaRad,
            maxAlphaChange
        )

        # 5 Update aerostate
        self.aeroState.alphaRad = newAlphaRad

        # 6 Limit thrust based on current flight phase 
        if autoOptimization:
            if time == 0.0:
                targetThrust = self.thrustController.cruisePowerLimit * self.maxThrust
            else:
                requestedThrust = self.thrustController.requestedThrustForAltitude(
                    currentAltitude=self.altitude,
                    targetAltitude=targetAltitude
                )

                targetThrust = self.thrustController.command(
                    requestedThrust=requestedThrust,
                    currentAltitude=self.altitude,
                    targetAltitude=targetAltitude
                )

            boomlessLimitedThrust = (
                0.20 * self.maxThrust
                + boomlessFraction * (0.25 * self.maxThrust - 0.20 * self.maxThrust)
                )

            targetThrust = min(targetThrust, boomlessLimitedThrust)
        else:
            manualThrustFraction = (
                0.25 if manualThrustFraction is None else manualThrustFraction
            )
            manualThrustFraction = aero.clamp(manualThrustFraction, 0.0, 1.0)
            targetThrust = manualThrustFraction * self.maxThrust
            
        maxThrustRate = self.maxThrustRateFraction * self.maxThrust #N/s
        maxThrustChange = maxThrustRate * dt

        self.thrust = aero.rate_limit(
            self.thrust,
            targetThrust,
            maxThrustChange
        )

        # 7 Recalculate aerodynamic state
        wingArea = self.wing.exposedWingArea()
        aspectRatio = self.wing.aspectRatio()

        self.aeroInput.rho = self.aeroState.rho
        self.aeroInput.velocity = self.aeroState.velocity
        self.aeroInput.wing_area = wingArea
        self.aeroInput.aspect_ratio = aspectRatio
        self.aeroInput.cl0 = self.aeroState.cl0
        self.aeroInput.cd0 = self.aeroState.cd0
        self.aeroInput.alpha_rad = self.aeroState.alphaRad
        self.aeroInput.oswald_efficiency = self.aeroState.oswaldEfficiency
        self.aeroInput.mach = self.aeroState.mach
        self.aeroInput.mass = self.plane.mass
        self.aeroInput.thrust = self.thrust

        aero.calculate_aero_state(
            ctypes.byref(self.aeroInput),
            ctypes.byref(self.aeroOutput)
        )

        dynamicPressure = self.aeroOutput.dynamic_pressure
        cl = self.aeroOutput.cl 
        cd = self.aeroOutput.cd
        lift = self.aeroOutput.lift
        drag = self.aeroOutput.drag
        weight = self.aeroOutput.weight
        netForceX = self.aeroOutput.net_force_x
        netForceY = self.aeroOutput.net_force_y
        accX = self.aeroOutput.acc_x
        accY = self.aeroOutput.acc_y

        # 8 Update velocity and altitude
        self.velocity = self.velocity + accX * dt
        self.velocityY = self.velocityY + accY * dt
        self.altitude = self.altitude + self.velocityY * dt
        self.positionX = self.positionX + self.velocity * dt

        if self.altitude > self.scheduler.maxAltitude:
            self.altitude = self.scheduler.maxAltitude
            if self.velocityY > 0:
                self.velocityY = 0

        if self.altitude < 0:
            self.altitude = 0
            self.velocityY = 0
        
        loggedTotalVelocity = self.totalVelocity()
        loggedTemperature = aero.temperature_at_altitude(self.altitude)
        loggedSpeedOfSound = aero.speed_of_sound(loggedTemperature)
        loggedMach = aero.mach_number(loggedSpeedOfSound, loggedTotalVelocity)

        cutoffAltitude = aero.cutoff_altitude_agl(
            self.altitude, 
            loggedMach,
            -0.0065
        )

        # 9 Save the data
        self.timeHistory.append(time)
        self.altitudeHistory.append(self.altitude)
        self.positionXHistory.append(self.positionX)
        self.totalVelocityHistory.append(self.totalVelocity())
        self.velocityHistory.append(self.velocity)
        self.velocityYHistory.append(self.velocityY)
        self.alphaRadHistory.append(self.aeroState.alphaRad)
        self.clHistory.append(cl)
        self.liftHistory.append(lift)
        self.dragHistory.append(drag)
        self.weightHistory.append(weight)
        self.thrustHistory.append(self.thrust)
        self.netXHistory.append(netForceX)
        self.netYHistory.append(netForceY)
        self.accXHistory.append(accX)
        self.accYHistory.append(accY)
        self.machHistory.append(loggedMach)
        self.cutoffAltitudeHistory.append(cutoffAltitude)
        self.deploymentHistory.append(self.wing.deployment)
        self.targetAltitudeHistory.append(targetAltitude)

    def run(self, totalTime, dt):
        time = 0
        while time <= totalTime:
            self.step(time, dt)
            time = time + dt

        return {
            "time": self.timeHistory,
            "altitude": self.altitudeHistory,
            "positionX": self.positionXHistory,
            "totalVelocity": self.totalVelocityHistory,
            "velocity": self.velocityHistory,
            "velocityY": self.velocityYHistory,
            "alphaRad": self.alphaRadHistory,
            "cl": self.clHistory,
            "lift": self.liftHistory,
            "drag": self.dragHistory,
            "weight": self.weightHistory,
            "thrust": self.thrustHistory,
            "netX": self.netXHistory,
            "netY": self.netYHistory,
            "accX": self.accXHistory,
            "accY": self.accYHistory,
            "mach": self.machHistory,
            "cutoffAltitude": self.cutoffAltitudeHistory,
            "deployment": self.deploymentHistory,
            "targetAltitude": self.targetAltitudeHistory
        }
        
    