"""
aero.py

Basic aerodynamic model for a retractable wing optimization project.

This file contains reusable functions for:
- simple lift/drag coefficient models
- simple exposed wing area
"""

import math 

class aerodynamicState:
    def __init__(self, rho, velocity, wing, cl0, cd0, alphaRad, deployment, oswaldEfficiency = 0.8):
        self.rho = rho
        self.velocity = velocity
        self.wing = wing
        self.cl0 = cl0
        self.cd0 = cd0 
        self.alphaRad = alphaRad
        self.deployment = deployment
        self.oswaldEfficiency = oswaldEfficiency 
    
    def liftCoefficient(self):
        liftSlope = 2 * math.pi
        coeffLift = self.cl0 + liftSlope * self.alphaRad
        return coeffLift 
    
    def dragCoefficient(self): 
        ar = self.wing.aspectRatio() 
        inducedDrag = (self.liftCoefficient())**2 / (math.pi * ar * self.oswaldEfficiency)
        return self.cd0 + inducedDrag
    
    def exposedWingArea(self):
        return self.deployment * self.wing.area()
