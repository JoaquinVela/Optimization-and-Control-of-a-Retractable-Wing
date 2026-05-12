"""
cruiseScheduler.py

deploy wing retraction for a retractable wing optimization project.

This file contains reusable functions for:
- choose target
"""

class cruiseSchedule:
    def __init__(self, maxAltitude=12496.8, machCutoff=1.15, minDeployment=0.3, maxDeployment=1.0, altitudeStep=100.0, machDeadband=0.005):
        self.maxAltitude = maxAltitude
        self.machCutoff = machCutoff
        self.minDeployment = minDeployment
        self.maxDeployment = maxDeployment
        self.altitudeStep = altitudeStep
        self.machDeadband = machDeadband

    def chooseTarget(self, altitude, velocity, atmosphere, deployment):
        mach = atmosphere.machNumber(velocity)
        safeMachMargin = 0.98 * self.machCutoff
        targetAltitude = altitude
        targetDeployment = deployment

        if mach < safeMachMargin - self.machDeadband:
            if deployment > self.minDeployment:
                targetDeployment = deployment - 0.01
            else: 
                targetAltitude = altitude + self.altitudeStep

        elif mach > safeMachMargin + self.machDeadband:
            targetDeployment = deployment + 0.01
            targetAltitude = altitude

        else:
            targetAltitude = altitude
            targetDeployment = deployment

        targetAltitude = min(targetAltitude, self.maxAltitude)

        targetDeployment = max(
            self.minDeployment,
            min(self.maxDeployment, targetDeployment)
        )

        return targetAltitude, targetDeployment, mach