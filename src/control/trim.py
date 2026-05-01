"""
trim.py

Search for values that make steady flight and speed for a retractable wing optimization project.

This file contains reusable functions for:
- trim checker
- is trimmed
- trim result
"""

class trimResult:
    def __init__(self, isTrimmed, netForceX, netForceY):
        self.isTrimmed = isTrimmed
        self.netForceX = netForceX
        self.netForceY = netForceY

class trimChecker:
    def __init__(self, performance, tolerance = 1e-4):
        self.performance = performance 
        self.tolerance = tolerance

    def isTrimmed(self):
        return (
            self.performance.isLevelFlight(self.tolerance)
            and self.performance.isSteadySpeed(self.tolerance)
        )
    
    def trimResult(self):
        return trimResult(
            self.isTrimmed(),
            self.performance.netForceX(),
            self.performance.netForceY()
        )