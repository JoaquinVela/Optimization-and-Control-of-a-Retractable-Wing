"""
thrustController.py

Basic thrust control model for a retractable wing optimization project.

This file contains reusable functions for:
- thrust force
- specific impulse
"""

class thrustControl:
    def __init__(self, maxThrust, cruisePowerLimit=0.25, altitudeTolerance=50):
        self.maxThrust = maxThrust
        self.cruisePowerLimit = cruisePowerLimit
        self.altitudeTolerance = altitudeTolerance

    def maxAllowedThrust(self, currentAltitude, targetAltitude):
        altitudeError = targetAltitude - currentAltitude
        if altitudeError > self.altitudeTolerance:
            return self.maxThrust
        
        return self.cruisePowerLimit * self.maxThrust
    
    def requestedThrustForAltitude(self, currentAltitude, targetAltitude):
        altitudeError = targetAltitude - currentAltitude
        cruiseThrust = self.cruisePowerLimit * self.maxThrust
        if altitudeError <= self.altitudeTolerance:
            return cruiseThrust
        
        fullPowerAltitudeError = 5000.0
        climbFraction = altitudeError / fullPowerAltitudeError
        climbFraction = max(0, min(1, climbFraction))

        return cruiseThrust + climbFraction * (self.maxThrust - cruiseThrust)

    def command(self, requestedThrust, currentAltitude, targetAltitude):
        maxAllowedThrust = self.maxAllowedThrust(currentAltitude, targetAltitude)
        return max(0, min(maxAllowedThrust, requestedThrust))
    