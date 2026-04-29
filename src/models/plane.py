"""
plane.py

Basic plane model for a retractable wing optimization project.

This file contains reusable functions for:
- weight of the plane
"""

class planeProperties:
    def __init__(self, mass):
        self.mass = mass 

    def weight(self):
        g = 9.81
        return self.mass * g