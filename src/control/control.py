"""
control.py

Hold altitude for a retractable wing optimization project.

This file contains reusable functions for:
- TBD
"""

class altitudeHoldController:
    def __init__(self, targetAltitude, trimAlphaRad, kp=0.00002, kd=0.002, minAlphaRad=0.0, maxAlphaRad=0.15):
        self.targetAltitude = targetAltitude
        self.trimAlphaRad = trimAlphaRad
        self.kp = kp
        self.kd = kd
        self.minAlphaRad = minAlphaRad
        self.maxAlphaRad = maxAlphaRad

    def altitudeError(self, currentAltitude):
        return self.targetAltitude - currentAltitude
    
    def command(self, currentAltitude, currentVelocityY):
        error = self.altitudeError(currentAltitude)

        alphaCorrection = self.kp * error - self.kd * currentVelocityY
        alphaCommand = self.trimAlphaRad + alphaCorrection

        if alphaCommand > self.maxAlphaRad:
            alphaCommand = self.maxAlphaRad
        elif alphaCommand < self.minAlphaRad:
            alphaCommand = self.minAlphaRad
         
        return alphaCommand