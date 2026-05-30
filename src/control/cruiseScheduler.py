"""
cruiseScheduler.py

deploy wing retraction for a retractable wing optimization project.

This file contains reusable functions for:
- choose target
"""

from src.models.boomless import boomlessConstraint
from src.models.atmosphere import cruiseAtmosphere

class cruiseSchedule:
    def __init__(self, targetAltitude=None, maxAltitude=12496.8, minDeployment=0.3, maxDeployment=1.0, altitudeStep=100.0, deploymentStep=0.00025, minCutoffAltitudeAGL=30, boomlessSafetyMargin=100):
        self.targetAltitude = targetAltitude if targetAltitude is not None else maxAltitude
        self.maxAltitude = maxAltitude
        self.minDeployment = minDeployment
        self.maxDeployment = maxDeployment
        self.altitudeStep = altitudeStep
        self.deploymentStep = deploymentStep
        self.boomlessSafetyMargin = boomlessSafetyMargin
        self.boomless = boomlessConstraint(minCutoffAltitudeAGL)

    def chooseTarget(self, altitude, velocity, atmosphere, deployment):
        mach = atmosphere.machNumber(velocity)
        targetAltitude = min(self.targetAltitude, self.maxAltitude)
        targetDeployment = deployment
        dynamicPressure = 0.5 * atmosphere.density() * velocity**2
        cutoffAltitude = self.boomless.cutoffAltitudeAGL(altitude, mach, atmosphere)

        nearBoomlessLimit = (
            cutoffAltitude < self.boomless.minCutoffAltitudeAGL + self.boomlessSafetyMargin
        )

        if nearBoomlessLimit:
            targetDeployment = deployment + self.deploymentStep
        elif dynamicPressure > 12500:
            targetDeployment = deployment - self.deploymentStep
        
        targetDeployment = max(
            self.minDeployment,
            min(self.maxDeployment, targetDeployment)
        )

        return targetAltitude, targetDeployment, mach