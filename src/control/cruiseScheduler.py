"""
cruiseScheduler.py

deploy wing retraction for a retractable wing optimization project.

This file contains reusable functions for:
- choose target
"""

from src.models.boomless import boomlessConstraint
from src.models.atmosphere import cruiseAtmosphere

class cruiseSchedule:
    def __init__(self, maxAltitude=12496.8, minDeployment=0.3, maxDeployment=1.0, altitudeStep=100.0, deploymentStep=0.01, minCutoffAltitudeAGL=30):
        self.maxAltitude = maxAltitude
        self.minDeployment = minDeployment
        self.maxDeployment = maxDeployment
        self.altitudeStep = altitudeStep
        self.deploymentStep = deploymentStep
        self.boomless = boomlessConstraint(minCutoffAltitudeAGL)

    def chooseTarget(self, altitude, velocity, atmosphere, deployment):
        mach = atmosphere.machNumber(velocity)
        targetAltitude = altitude
        targetDeployment = deployment

        if self.boomless.isBoomless(altitude, mach, atmosphere):
            targetDeployment = deployment - self.deploymentStep
        else: 
            targetAltitude = altitude + self.altitudeStep

        targetAltitude = min(targetAltitude, self.maxAltitude)

        targetDeployment = max(
            self.minDeployment,
            min(self.maxDeployment, targetDeployment)
        )

        return targetAltitude, targetDeployment, mach