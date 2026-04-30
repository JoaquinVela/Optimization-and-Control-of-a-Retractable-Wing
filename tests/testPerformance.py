from src.models.geometry import wingGeometry
from src.models.aero import aerodynamicState
from src.models.plane import planeProperties
from src.models.forces import aerodynamicsForce
from src.models.performance import aerodynamicPerformance
from src.control.validation import physicalValidation

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

mass = 274700
plane = planeProperties(mass)

forces = aerodynamicsForce(aeroState, plane, thrust = 248000)

aeroPerformance = aerodynamicPerformance(forces)

validation = physicalValidation(aeroState, plane, forces, aeroPerformance)
validation.runAllChecks()

print("Lift to Drag Ratio:", aeroPerformance.liftToDragRatio())
print("Horizontal Net Force:", aeroPerformance.netForceX())
print("Vertical Net Force:", aeroPerformance.netForceY())
print("Horizontal Acceleration:", aeroPerformance.accX())
print("Vertical Acceleration:", aeroPerformance.accY())

print("Lift:", forces.lift())
print("Weight:", forces.weight())
print("Drag:", forces.drag())
print("Thrust:", forces.thrustForce())

print("Level Flight:", aeroPerformance.isLevelFlight())
print("Steady Speed:", aeroPerformance.isSteadySpeed())