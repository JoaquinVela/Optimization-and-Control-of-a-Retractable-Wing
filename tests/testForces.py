from src.models.geometry import wingGeometry
from src.models.aero import aerodynamicState
from src.models.forces import aerodynamicsForce
from src.models.plane import planeProperties
import math

wing = wingGeometry(span = 64.8, chord = 13.36)
aeroState = aerodynamicState(
    rho = 0.380,
    velocity = 230,
    wing = wing,
    cl0 = 0.2,
    cd0 = 0.02,
    alphaRad = 0.0174533,
    deployment = 1
)
mass = 274669.280707
plane = planeProperties(mass)
forces = aerodynamicsForce(aeroState, plane, thrust = 242476.37271298046)

print("Dynamic Pressure:", forces.dynamicPressure())
print("Lift Force:", forces.lift())
print("Drag Force:", forces.drag())
print("Weight:", forces.weight())
print("Thrust:", forces.thrustForce())
