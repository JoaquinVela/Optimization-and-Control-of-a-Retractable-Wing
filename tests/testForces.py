from src.models.geometry import wingGeometry
from src.models.aero import aerodynamicState
from src.models.forces import aerodynamicsForce
from src.models.plane import planeProperties
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

aircraft = planeProperties(10000)

forces = aerodynamicsForce(state, aircraft, thrust = 15000) 

print("Dynamic Pressure:", forces.dynamicPressure())
print("Lift Force:", forces.lift())
print("Drag Force:", forces.drag())
print("Weight:", forces.weight())
print("Thrust:", forces.thrustForce())
