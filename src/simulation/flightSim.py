"""
flightSim.py

Basic flight simulator for a retractable wing optimization project.

This file contains reusable functions for:
- TBD
"""

class flightSimulation:
    def __init__(self, performance, dt):
        self.performance = performance
        self.dt = dt

    def step(self, state):
        ax = self.performance.accX()
        ay = self.performance.accY()
        state["vx"] += ax * self.dt
        state["vy"] += ay * self.dt
        state["x"] += state["vx"] * self.dt
        state["y"] += state["vy"] * self.dt
        return state
    
    def run(self, initialState, steps):
        history = []
        state = initialState.copy()
        for i in range(steps):
            state = self.step(state)
            history.append(state.copy())
        return history
        
    