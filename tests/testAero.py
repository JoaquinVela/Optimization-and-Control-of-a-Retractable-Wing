from src.models.aero import aerodynamicState
import math

state = aerodynamicState(
    rho = 1.225,
    velocity = 80,
    maxWingArea = 20,
    extensionRatio = 0.75,
    alphaRad = math.radians(5),
    mass = 1000
)

print(state)