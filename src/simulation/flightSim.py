"""
flightSim.py

Basic flight simulator for a retractable wing optimization project.

This file contains reusable functions for:
- TBD
"""

from src.models.forces import aerodynamicsForce
from src.models.performance import aerodynamicPerformance
from src.models.atmosphere import cruiseAtmosphere
from src.control.cruiseScheduler import cruiseSchedule
from src.control.thrustController import thrustControl

class flightSimulation:
    def __init__(self, aeroState, plane, controller, maxThrust, altitude, velocityY=0, maxThrustRateFraction=0.05):
        self.aeroState = aeroState
        self.plane = plane
        self.controller = controller
        self.maxThrust = maxThrust
        self.requestedThrust = self.maxThrust
        self.thrust = 0.25 * self.maxThrust
        self.thrustController = thrustControl(self.maxThrust)
        self.altitude = altitude
        self.velocity = aeroState.velocity
        self.velocityY = velocityY
        self.positionX = 0
        self.maxThrustRateFraction = maxThrustRateFraction

        self.scheduler = cruiseSchedule(targetAltitude=controller.targetAltitude)
        self.wing = self.aeroState.wing

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

    def step(self, time, dt):
        # 1 Build atmosphere
        atmosphere = cruiseAtmosphere(self.altitude)

        # 2 Update aerostate
        totalVelocity = self.totalVelocity()
        self.aeroState.rho = atmosphere.density()
        self.aeroState.velocity = totalVelocity

        # 3 Ask scheduler for altitide and wing deployment targets
        targetAltitude, targetDeployment, mach = self.scheduler.chooseTarget(
            self.altitude,
            totalVelocity,
            atmosphere,
            self.wing.deployment
        )

        cutoffAltitude = self.scheduler.boomless.cutoffAltitudeAGL(
            self.altitude, 
            mach,
            atmosphere
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
            boomlessFraction = max(0.0, min(1.0, boomlessFraction))
        else:
            boomlessFraction = 1.0

        proposedArea = targetDeployment * self.wing.area()
        dynamicPressure = 0.5 * atmosphere.density() * totalVelocity**2

        requiredCL = self.plane.weight() / (dynamicPressure * proposedArea)
        liftSlope = 2 * 3.141592653589793
        requiredAlphaRad = (requiredCL - self.aeroState.cl0) / liftSlope

        alphaMargin = 0.02
        maxUsableAlphaRad = self.controller.maxAlphaRad - alphaMargin

        if requiredAlphaRad > maxUsableAlphaRad:
            targetDeployment = self.wing.deployment

        self.aeroState.mach = mach
        self.controller.targetAltitude = targetAltitude

        # 4 Apply wing geometry change
        self.wing.setDeployment(targetDeployment)

        # 5 Controller decides new angle of attack
        newAlphaRad = self.controller.command(
            currentAltitude=self.altitude,
            currentVelocityY=self.velocityY,
            aeroState=self.aeroState,
            plane=self.plane
        )

        maxAlphaRate = 0.01 # rad/s
        maxAlphaChange = maxAlphaRate * dt

        alphaError = newAlphaRad - self.aeroState.alphaRad

        if alphaError > maxAlphaChange:
            newAlphaRad = self.aeroState.alphaRad + maxAlphaChange
        elif alphaError < -maxAlphaChange:
            newAlphaRad = self.aeroState.alphaRad - maxAlphaChange

        # 6 Update aerostate
        self.aeroState.alphaRad = newAlphaRad

        # 7 Limit thrust based on current flight phase 
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
            0.20 * self.maxThrust + boomlessFraction * (0.25 * self.maxThrust - 0.20 * self.maxThrust)
        )

        targetThrust = min(targetThrust, boomlessLimitedThrust)
            
        maxThrustRate = self.maxThrustRateFraction * self.maxThrust #N/s
        maxThrustChange = maxThrustRate * dt

        thrustError = targetThrust - self.thrust

        if thrustError > maxThrustChange:
            self.thrust = self.thrust + maxThrustChange
        elif thrustError < -maxThrustChange:
            self.thrust = self.thrust - maxThrustChange
        else:
            self.thrust = targetThrust

        # 8 Recalculate forces
        forces = aerodynamicsForce(
            self.aeroState,
            self.plane,
            thrust = self.thrust
        )

        performance = aerodynamicPerformance(forces)

        # 9 Get Forces
        lift = forces.lift()
        drag = forces.drag()
        weight = forces.weight()
        netForceX = performance.netForceX()
        netForceY = performance.netForceY()

        # 10 Get accelerations
        accY = performance.accY()
        accX = performance.accX()

        # 11 Update velocity and altitude
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
        
        loggedAtmosphere = cruiseAtmosphere(self.altitude)
        loggedTotalVelocity = self.totalVelocity()
        loggedMach = loggedAtmosphere.machNumber(loggedTotalVelocity)

        cutoffAltitude = self.scheduler.boomless.cutoffAltitudeAGL(
            self.altitude,
            loggedMach,
            loggedAtmosphere
        )

        # 12 Save the data
        self.timeHistory.append(time)
        self.altitudeHistory.append(self.altitude)
        self.positionXHistory.append(self.positionX)
        self.totalVelocityHistory.append(self.totalVelocity())
        self.velocityHistory.append(self.velocity)
        self.velocityYHistory.append(self.velocityY)
        self.alphaRadHistory.append(self.aeroState.alphaRad)
        self.clHistory.append(self.aeroState.liftCoefficient())
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
        
    