"""
atmosphere.py

Atmospheric information for cruise flight for a retractable wing optimization project.

This file contains reusable functions for:
- temperature
- pressure
- density
- speed of sound
- mach number
"""

import math

class cruiseAtmosphere:
    def __init__(self, altitudeMeters):
        self.altitudeMeters = altitudeMeters

    def temperature(self):
        # ISA termperature model for troposphere
        seaLevelTemp = 288.15 # K
        lapseRate = 0.0065 # K/m
        return seaLevelTemp - lapseRate * self.altitudeMeters
    
    def temperatureGradient(self):
        return -0.0065
    
    def pressure(self):
        # ISA pressure model
        seaLevelPressure = 101325 # Pa
        seaLevelTemp = 288.15 # K
        lapseRate = 0.0065 # K/m
        gravity = 9.80665 # m/s^2
        gasConstant = 287.05 # J/(kg * K)
        return seaLevelPressure * (
            self.temperature() / seaLevelTemp
        ) ** (gravity / (gasConstant * lapseRate))
    
    def density(self):
        # Density from ideal gas law
        gasConstant = 287.05 # J/(kg * K)
        return self.pressure() / (gasConstant * self.temperature())
    
    def speedOfSound(self):
        # a = sqrt(gamma * R * T)
        gamma = 1.4
        gasConstant = 287.05
        return math.sqrt(gamma * gasConstant * self.temperature())
    
    def machNumber(self, velocity):
        # mach = aircraft speed / speed of sound
        return velocity / self.speedOfSound()