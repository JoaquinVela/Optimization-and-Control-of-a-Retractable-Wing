"""
boomless.py

Boomless constraint for a retractable wing optimization project.

This file contains reusable functions for:
- TBD
"""

class boomlessConstraint:
    def __init__(self, minCutoffAltitudeAGL=30):
        self.minCutoffAltitudeAGL=minCutoffAltitudeAGL

    def cutoffAltitudeAGL(self, altitude, mach, atmosphere):
        if mach <= 1.0:
            return 999999
        
        cutoffDepth = self.cutoffDepth(mach, atmosphere)
        return altitude - cutoffDepth

    def cutoffDepth(self, mach, atmosphere):
        machExcess = mach - 1.0
        baseDepth = 25000 * machExcess
        temperatureGradient = atmosphere.temperatureGradient()

        if temperatureGradient < 0:
            gradientFactor = 1.0
        else:
            gradientFactor = 1.5

        return baseDepth * gradientFactor

    def isBoomless(self, altitude, mach, atmosphere):
        cutoffAltitude = self.cutoffAltitudeAGL(altitude, mach, atmosphere)
        return cutoffAltitude >= self.minCutoffAltitudeAGL 