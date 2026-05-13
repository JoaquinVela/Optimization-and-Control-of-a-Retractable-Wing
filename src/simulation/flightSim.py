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

class flightSimulation:
    def __init__(self, aeroState, plane, controller, thrust, altitude, velocityY=0):
        self.aeroState = aeroState
        self.plane = plane
        self.controller = controller
        self.thrust = thrust
        self.altitude = altitude
        self.velocity = aeroState.velocity
        self.velocityY = velocityY
        self.positionX = 0

        self.scheduler = cruiseSchedule()
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
        self.netXHistory = []
        self.netYHistory = []
        self.accXHistory = []
        self.accYHistory = []
        self.machHistory = []
        self.machCutoffHistory = []
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

        # 6 Update aerostate
        self.aeroState.alphaRad = newAlphaRad

        # 7 Recalculate forces
        forces = aerodynamicsForce(
            self.aeroState,
            self.plane,
            thrust = self.thrust
        )

        performance = aerodynamicPerformance(forces)

        # 8 Get Forces
        lift = forces.lift()
        drag = forces.drag()
        weight = forces.weight()
        netForceX = performance.netForceX()
        netForceY = performance.netForceY()

        # 9 Get accelerations
        accY = performance.accY()
        accX = performance.accX()

        # 10 Update velocity and altitude
        self.velocity = self.velocity + accX * dt
        self.velocityY = self.velocityY + accY * dt
        self.altitude = self.altitude + self.velocityY * dt
        self.positionX = self.positionX + self.velocity * dt

        if self.altitude < 0:
            self.altitude = 0
            self.velocityY = 0

        # 11 Save the data
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
        self.netXHistory.append(netForceX)
        self.netYHistory.append(netForceY)
        self.accXHistory.append(accX)
        self.accYHistory.append(accY)
        self.machHistory.append(mach)
        self.machCutoffHistory.append(self.scheduler.machCutoff)
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
            "netX": self.netXHistory,
            "netY": self.netYHistory,
            "accX": self.accXHistory,
            "accY": self.accYHistory,
            "mach": self.machHistory,
            "machCutoff": self.machCutoffHistory,
            "deployment": self.deploymentHistory,
            "targetAltitude": self.targetAltitudeHistory
        }
        
    