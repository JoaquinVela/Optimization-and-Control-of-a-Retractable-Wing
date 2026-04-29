"""
forces.py

Basic aerodynamic forces model for a retractable wing optimization project.

This file contains reusable functions for:
- dynamic pressure
- lift force
- drag force
"""

class aerodynamicsForce:
    def __init__(self, state):
        self.state = state

    def dynamicPressure(self):
        rho = self.state.rho
        v = self.state.velocity 
        return 0.5 * rho * v**2
    
    def lift(self):
        q = self.dynamicPressure()
        s = self.state.exposedWingArea()
        CL = self.state.liftCoefficient() 
        return q * s * CL
    
    def drag(self):
        q = self.dynamicPressure()
        s = self.state.exposedWingArea()
        CD = self.state.dragCoefficient()
        return q * s * CD