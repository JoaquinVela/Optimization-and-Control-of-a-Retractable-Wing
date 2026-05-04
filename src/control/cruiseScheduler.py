"""
cruiseScheduler.py

deploy wing retraction for a retractable wing optimization project.

This file contains reusable functions for:
- choose target
"""

class cruiseSchedule:
    def __init__(self, maxAltitude=12496.8, machCutoff=1.15, minDeployment=0.3, maxDeployment=1.0):
        self.maxAltitude = maxAltitude
        self.machCutoff = machCutoff
        self.minDeployment = minDeployment
        self.maxDeployment = maxDeployment

    def chooseTarget(self, altitude, velocity, atmosphere, deployment):
        mach = atmosphere.machNumber(velocity)
        targetAltitude = altitude
        deployment = deployment
        safeMachMargin = 0.97 * self.machCutoff

        if mach < safeMachMargin:
            deployment -= 0.01
            targetAltitude += 2.0

        elif mach > safeMachMargin:
            deployment += 0.02
            targetAltitude += 5.0

        else:
            deployment = deployment

        targetAltitude = min(targetAltitude, self.maxAltitude)

        deployment = max(
            self.minDeployment,
            min(self.maxDeployment, deployment)
        )

        return targetAltitude, deployment, mach