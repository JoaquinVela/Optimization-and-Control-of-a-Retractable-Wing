"""
flightSim.py

Basic flight animation for a retractable wing optimization project.

This file contains reusable functions for:
- animation
- update
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class flightAnimation:
    def __init__(self, history):
        self.history = history

    def animate(self):
        xVals = [s["x"] for s in self.history]
        yVals = [s["y"] for s in self.history]

        fig, ax = plt.subplots()

        ax.set_xlim(min(xVals), max(xVals))
        ax.set_ylim(min(yVals) - 100, max(yVals) + 100)

        ax.set_xlabel("Horizontal Position x [m]")
        ax.set_ylabel("Altitude [m]")
        ax.set_title("2D Cruise Flight Animation")
        ax.grid(True)

        plane, = ax.plot([], [], marker=">", markersize = 12)

        def update(frame):
            plane.set_data([xVals[frame]], [yVals[frame]])
            return plane,

        anim = FuncAnimation(
            fig, 
            update,
            frames = len(self.history),
            interval = 50,
            blit = True
        )

        plt.show()
