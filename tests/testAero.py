from src.models.aero import aerodynamicState
from src.models.geometry import wingGeometry
import math

wing = wingGeometry(span = 10, chord = 2)

aero = aerodynamicState(
    rho = 1.225,
    velocity = 145,
    wing = wing,
    cl0 = 0,
    cd0 = 0.02,
    alphaRad = 0.0872665,
    deployment = 1
)

print("Wing Area:", aero.exposedWingArea())
print("Aspect Ratio:", wing.aspectRatio())
print("Lift Coefficient:", aero.liftCoefficient())
print("Drag Coefficient:", aero.dragCoefficient())