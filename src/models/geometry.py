"""
geometry.py

Basic wing geomrety for a retractable wing optimization project.

This file contains reusable functions for:
- area of wing
- aspect ratio of wing
"""

class wingGeometry:
    def __init__(self, span, chord, deployment=1.0):
        self.span = span 
        self.chord = chord
        self.deployment = deployment 

    def area(self):
        return self.span * self.chord
    
    def exposedWingArea(self):
        return self.deployment * self.area()
    
    def aspectRatio(self): 
        return self.span**2 / self.exposedWingArea()
    
    def setDeployment(self, deployment):
        self.deployment = max(0.3, min(1.0, deployment))


    
