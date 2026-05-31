"""
control.py

Hold altitude for a retractable wing optimization project.

This file contains reusable functions for:
- TBD
"""

from src.models.aero_c import aero

class altitudeHoldController:
    def __init__(self, targetAltitude, trimAlphaRad, kp=0.00002, kd=0.002, minAlphaRad=-0.05, maxAlphaRad=0.15):
        self.targetAltitude = targetAltitude
        self.trimAlphaRad = trimAlphaRad
        self.kp = kp
        self.kd = kd
        self.minAlphaRad = minAlphaRad
        self.maxAlphaRad = maxAlphaRad

    def altitudeError(self, currentAltitude):
        return self.targetAltitude - currentAltitude
    
    def dynamicTrimAlpha(self, aeroState, plane):
        return aero.dynamic_trim_alpha(
            plane.weight(),
            aeroState.rho,
            aeroState.velocity,
            aeroState.wing.exposedWingArea(),
            aeroState.cl0
        )
    
    def command(self, currentAltitude, currentVelocityY, aeroState=None, plane=None):
        error = self.altitudeError(currentAltitude)

        if aeroState is not None and plane is not None:
            trimAlphaRad = self.dynamicTrimAlpha(aeroState, plane)
        else:
            trimAlphaRad = self.trimAlphaRad

        alphaCorrection = self.kp * error - self.kd * currentVelocityY
        alphaCommand = trimAlphaRad + alphaCorrection

        if alphaCommand > self.maxAlphaRad:
            alphaCommand = self.maxAlphaRad
        elif alphaCommand < self.minAlphaRad:
            alphaCommand = self.minAlphaRad
         
        return alphaCommand