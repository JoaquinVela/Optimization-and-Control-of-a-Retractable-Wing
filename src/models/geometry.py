"""
geometry.py

Basic wing geomrety for a retractable wing optimization project.

This file contains reusable functions for:
- area of wing
- aspect ratio of wing
"""

class wingGeometry:
    def __init__(self, span, chord):
        self.span = span 
        self.chord = chord 

    def area(self):
        return self.span * self.chord
    
    def aspectRatio(self): 
        return self.span**2 / self.area()
    
