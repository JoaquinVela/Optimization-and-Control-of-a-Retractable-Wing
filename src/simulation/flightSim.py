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
    def __init__(self, aeroState, plane, controller, thrust, altitude, velocity, velocityY=0):
        self.aeroState = aeroState
        self.plane = plane
        self.controller = controller
        self.thrust = thrust
        self.altitude = altitude
        self.velocity = velocity
        self.velocityY = velocityY

        self.scheduler = cruiseSchedule()
        self.wing = self.aeroState.wing

        self.timeHistory = []
        self.altitudeHistory = []
        self.velocityHistory = []
        self.velocityYHistory = []
        self.alphaRadHistory = []
        self.clHistory = []
        self.liftHistory = []
        self.weightHistory = []
        self.machHistory = []
        self.machCutoffHistory = []
        self.deploymentHistory = []
        self.targetAltitudeHistory = []

    def step(self, time, dt):
        # 1 Build atmosphere
        atmosphere = cruiseAtmosphere(self.altitude)

        # 2 Update aerostate
        self.aeroState.rho = atmosphere.density()
        self.aeroState.velocity = self.velocity

        # 3 Ask scheduler for altitide and wing deployment targets
        targetAltitude, targetDeployment, mach = self.scheduler.chooseTarget(
            self.altitude,
            self.velocity,
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

        # 8 Get accelerations
        accY = performance.accY()
        accX = performance.accX()

        # 9 Update velocity and altitude
        self.velocity = self.velocity + accX * dt
        self.velocityY = self.velocityY + accY * dt
        self.altitude = self.altitude + self.velocityY * dt

        # 10 Small altitude scheduler correction
        altitudeError = targetAltitude - self.altitude
        altitudeRateCommand = 0.02 * altitudeError
        altitudeRateCommand = max(-5.0, min(5.0, altitudeRateCommand))
        # self.altitude += altitudeRateCommand * dt <-- Removed

        # 11 Save the data
        self.timeHistory.append(time)
        self.altitudeHistory.append(self.altitude)
        self.velocityHistory.append(self.velocity)
        self.velocityYHistory.append(self.velocityY)
        self.alphaRadHistory.append(self.aeroState.alphaRad)
        self.clHistory.append(self.aeroState.liftCoefficient())
        self.liftHistory.append(forces.lift())
        self.weightHistory.append(forces.weight())
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
            "velocity": self.velocityHistory,
            "velocityY": self.velocityYHistory,
            "alphaRad": self.alphaRadHistory,
            "cl": self.clHistory,
            "lift": self.liftHistory,
            "weight": self.weightHistory,
            "mach": self.machHistory,
            "machCutoff": self.machCutoffHistory,
            "deployment": self.deploymentHistory,
            "targetAltitude": self.targetAltitudeHistory
        }
        
    