"""
aero.py

Basic aerodynamic model for a retractable wing optimization project.

This file contains reusable functions for:
- dynamic pressure
- lift force
- drag force
- wing area as a function of extension
- simple lift/drag coefficient models
"""

import math 

def dynamicPressure(rho: float, velocity: float):
    return 0.5 * rho * (velocity**2)

def liftForce(rho: float, velocity: float, wingArea: float, cl: float):
    q = dynamicPressure(rho, velocity)
    return q * wingArea * cl

def dragFroce(rho: float, velocity: float, wingArea: float, cd: float):
    q = dynamicPressure(rho, velocity)
    return q * wingArea * cd

