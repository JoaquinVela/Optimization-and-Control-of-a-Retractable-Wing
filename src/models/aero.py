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

def dragForce(rho: float, velocity: float, wingArea: float, cd: float):
    q = dynamicPressure(rho, velocity)
    return q * wingArea * cd

def exposedWingArea(maxArea: float, extensionRatio: float, minAreaRatio = 0.4):
    if not 0.0 <= extensionRatio <= 1.0:
        raise ValueError("extensionRatio must be between 0 and 1")
    if not 0.0 < minAreaRatio <= 1.0:
        raise ValueError("minAreaRatio must be greater than 0 and less than or equal to 1")
    
    areaRatio = minAreaRatio + extensionRatio * (1.0 - minAreaRatio)
    return maxArea * areaRatio 

def liftCoefficient(alphaRad: float, cl0 = 0.2, clAlpha: float = 2 * math.pi, clMax: float = 1.5): 
    cl = cl0 + clAlpha * alphaRad
    return max(-clMax, min(cl, clMax))

def dragCoefficient(cl: float, cd0: float = 0.02, aspectRatio: float = 8.0, oswaldEfficiency: float = 0.8):
    inducedDrag = cl**2 / (math.pi * oswaldEfficiency * aspectRatio)
    return cd0 + inducedDrag

def weightForce(mass: float, gravity: float = 9.81):
    return mass * gravity

def aerodynamicState(rho: float, velocity: float, maxWingArea: float, extensionRatio: float, alphaRad: float, mass: float):
    wingArea = exposedWingArea(maxWingArea, extensionRatio)
    cl = liftCoefficient(alphaRad)
    cd = dragCoefficient(cl)

    lift = liftForce(rho, velocity, wingArea, cl)
    drag = dragForce(rho, velocity, wingArea, cd)
    weight = weightForce(mass)
    
    return {"Wing Area": wingArea,
            "CL": cl,
            "CD": cd,
            "Lift Force": lift,
            "Drag Force": drag,
            "Weight": weight,
            "Lift Margin": lift - weight}