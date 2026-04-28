from src.models.aero import aerodynamicState
from src.models.geometry import wingGeometry
import math

wing = wingGeometry(span = 10, chord = 2)

aero = aerodynamicState(
    rho = 1.225,
    velocity = 50,
    wing = wing,
    cl = 0.5,
    cd = 0.03
)

print("Wing Area:", wing.area())
print("Lift:", aero.lift())
print("Drag:", aero.drag())