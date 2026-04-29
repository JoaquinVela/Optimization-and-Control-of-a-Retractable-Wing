from src.models.geometry import wingGeometry
from src.models.aero import aerodynamicState
from src.models.plane import planeProperties
from src.models.forces import aerodynamicsForce
from src.models.performance import aerodynamicPerformance
from src.control.validation import physicalValidation

wing = wingGeometry(span = 10, chord = 1)

aeroState = aerodynamicState(
    rho = 1.225,
    velocity = 145,
    wing = wing,
    cl0 = 0.2,
    cd0 = 0.02,
    alphaRad = 0.0872665,
    deployment = 1
)

plane = planeProperties(10000)

forces = aerodynamicsForce(aeroState, plane, thrust = 500000)

aeroPerformance = aerodynamicPerformance(forces)

print("Lift to Drag Ratio:", aeroPerformance.liftToDragRatio())
print("Horizontal Net Force:", aeroPerformance.netForceX())
print("Vertical Net Force:", aeroPerformance.netForceY())
print("Horizontal Acceleration:", aeroPerformance.accX())
print("Vertical Acceleration:", aeroPerformance.accY())

validation = physicalValidation(aeroState, plane, forces, aeroPerformance)
validation.runAllChecks()