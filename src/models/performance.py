"""
performance.py

Basic plane performance model for a retractable wing optimization project.

This file contains reusable functions for:
- Lift to drag ratio
- horizontal net force
- vertical net force
- horizontal acceleration 
- vertical acceleration
"""

class aerodynamicPerformance:
    def __init__(self, forces):
        self.forces = forces

    def liftToDragRatio(self):
        return self.forces.lift() / self.forces.drag()
    
    def netForceX(self):
        return self.forces.thrustForce() - self.forces.drag()
    
    def netForceY(self):
        return self.forces.lift() - self.forces.weight()
    
    def accX(self):
        return self.netForceX() / self.forces.plane.mass
    
    def accY(self):
        return self.netForceY() / self.forces.plane.mass
    
    def isLevelFlight(self, tolerance = 0.05):
        lift = self.forces.lift()
        weight = self.forces.weight()
        percentDiff = abs(lift - weight) / weight
        return percentDiff <= tolerance
    
    def isSteadySpeed(self, tolerance = 0.05):
        thrust = self.forces.thrustForce()
        drag = self.forces.drag()
        percentDiff = abs(thrust - drag) / drag
        return percentDiff <= tolerance
    
