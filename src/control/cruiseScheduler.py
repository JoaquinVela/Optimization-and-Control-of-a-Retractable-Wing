"""
cruiseScheduler.py

deploy wing retraction for a retractable wing optimization project.

This file contains reusable functions for:
- choose target
"""

from src.models.boomless import boomlessConstraint
from src.models.aero_c import aero

class cruiseSchedule:
    def __init__(self, targetAltitude=None, maxAltitude=13716.0, minDeployment=0.3, maxDeployment=1.0, altitudeStep=100.0, deploymentStep=0.00025, minCutoffAltitudeAGL=30, boomlessSafetyMargin=100):
        self.targetAltitude = targetAltitude if targetAltitude is not None else maxAltitude
        self.maxAltitude = maxAltitude
        self.minDeployment = minDeployment
        self.maxDeployment = maxDeployment
        self.altitudeStep = altitudeStep
        self.deploymentStep = deploymentStep
        self.boomlessSafetyMargin = boomlessSafetyMargin
        self.boomless = boomlessConstraint(minCutoffAltitudeAGL)

    def chooseTarget(self, altitude, velocity, deployment):
        rho = aero.air_density_at_altitude(altitude)
        temperature = aero.temperature_at_altitude(altitude)
        speedOfSound = aero.speed_of_sound(temperature)
        mach = aero.mach_number(speedOfSound, velocity)

        targetAltitude = min(self.targetAltitude, self.maxAltitude)
        targetDeployment = deployment

        dynamicPressure = aero.dynamic_pressure(rho, velocity)

        cutoffAltitude = aero.cutoff_altitude_agl(
            altitude, 
            mach,
            -0.0065
        )

        nearBoomlessLimit = (
            cutoffAltitude < self.boomless.minCutoffAltitudeAGL + self.boomlessSafetyMargin
        )

        if nearBoomlessLimit:
            targetDeployment = deployment + self.deploymentStep
        elif dynamicPressure > 12500:
            targetDeployment = deployment - self.deploymentStep
        
        targetDeployment = aero.clamp(
            targetDeployment,
            self.minDeployment,
            self.maxDeployment
        )

        return targetAltitude, targetDeployment, mach
