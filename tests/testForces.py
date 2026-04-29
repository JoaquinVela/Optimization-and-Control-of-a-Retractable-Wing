from src.models.geometry import wingGeometry
from src.models.aero import aerodynamicState
from src.models.forces import aerodynamicsForce
import math

wing = wingGeometry(span = 10, chord = 2)

state = aerodynamicState(
    rho = 1.225,
    velocity = 145,
    wing = wing,
    cl0 = 0.0,
    cd0 = 0.02,
    alphaRad = 0.0872665,
    deployment = 1
)

forces = aerodynamicsForce(state)

print("Dynamic Pressure:", forces.dynamicPressure())
print("Lift Force:", forces.lift())
print("Drag Force:", forces.drag())