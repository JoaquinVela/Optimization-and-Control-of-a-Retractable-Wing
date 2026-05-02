"""
flightSim.py

Basic flight simulator for a retractable wing optimization project.

This file contains reusable functions for:
- TBD
"""

from src.models.forces import aerodynamicsForce
from src.models.performance import aerodynamicPerformance

class flightSimulation:
    def __init__(self, aeroState, plane, controller, thrust, altitude, velocityY=0):
        self.aeroState = aeroState
        self.plane = plane
        self.controller = controller
        self.thrust = thrust
        self.altitude = altitude
        self.velocityY = velocityY

        self.timeHistory = []
        self.altitudeHistory = []
        self.alphaRadHistory = []
        self.clHistory = []
        self.liftHistory = []
        self.weightHistory = []

    def step(self, time, dt):
        # 1: Controller decides new angle of attack
        newAlphaRad = self.controller.command(
            currentAltitude=self.altitude,
            currentVelocityY=self.velocityY
        )
    
        # 2: Update aerodynamic state
        self.aeroState.alphaRad = newAlphaRad

        # 3: Recalculate forces using new alphaRad
        forces = aerodynamicsForce(
            self.aeroState,
            self.plane,
            thrust = self.thrust
        )

        performance = aerodynamicPerformance(forces)

        # 4: Get vertical acceleration
        accY = performance.accY()

        # 5: Update vertical velocity and altitude
        self.velocityY = self.velocityY + accY * dt
        self.altitude = self.altitude + self.velocityY * dt

        # 6: Save the data
        self.timeHistory.append(time)
        self.altitudeHistory.append(self.altitude)
        self.alphaRadHistory.append(self.aeroState.alphaRad)
        self.clHistory.append(self.aeroState.liftCoefficient())
        self.liftHistory.append(forces.lift())
        self.weightHistory.append(forces.weight())

    def run(self, totalTime, dt):
        time = 0
        while time <= totalTime:
            self.step(time, dt)
            time = time + dt

        return {
            "time": self.timeHistory,
            "altitude": self.altitudeHistory,
            "alphaRad": self.alphaRadHistory,
            "cl": self.clHistory,
            "lift": self.liftHistory,
            "weight": self.weightHistory
        }
        
    