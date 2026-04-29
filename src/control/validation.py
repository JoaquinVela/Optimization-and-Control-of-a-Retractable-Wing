"""
validation.py

BBasic physics validation for a retractable wing optimization project.

This file contains reusable functions for:
- TBD
"""

class physicalValidation:
    def __init__(self, aeroState, plane, forces, performace):
        self.aeroState = aeroState
        self.plane = plane
        self.forces = forces
        self.performance = performace

    def checkPositiveValues(self):
        if self.aeroState.rho <= 0:
            print("ERROR: Air density must be positive")

        if self.aeroState.velocity < 0:
            print("ERROR: Velocity cannot be negative")

        if self.plane.mass <= 0:
            print("ERROR: Plane mass must be positive")

        if self.aeroState.wing.area() <= 0:
            print("ERROR: Wing area must be positive")

    def checkForceRanges(self):
        lift = self.forces.lift()
        drag = self.forces.drag()
        weight = self.forces.weight()
        thrust = self.forces.thrustForce()

        if lift < 0:
            print("WARNING: Lift is negative")

        if drag < 0:
            print("ERROR: Drag should be positive")

        if weight <= 0:
            print("ERROR: Weight should be positive")

        if thrust < 0: 
            print("WARNING: Thrust is negative")

    def checkPerformanceRanges(self):
        ld = self.performance.liftToDragRatio()

        if ld <= 0:
            print("WARNING: Lift to drag ratio should be positive")

        if ld > 30:
            print("WARNING: Lift to drag ratio is very high. Check CL, CD, or wing area")

        if ld < 2:
            print("WARNING: Lift to drag ratio is very low. Plane may be very inefficient or values may be wrong")

    def checkWeightFormula(self):
        expectedWeight = self.plane.mass * 9.81
        actualWeight = self.plane.weight()
        if abs(expectedWeight - actualWeight) > 0.001:
            print("ERROR: Weight formula may be incorrect")
    
    def runAllChecks(self):
        self.checkPositiveValues()
        self.checkForceRanges()
        self.checkPerformanceRanges()
        self.checkWeightFormula()
        print("Validation checks complete")