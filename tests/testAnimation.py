from src.simulation.flightSim import flightSimulation
from src.simulation.animation import flightAnimation
from src.control.trim import trimChecker
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
mass = 274669.280707
plane = planeProperties(mass)
forces = aerodynamicsForce(aeroState, plane, thrust = 242476.37271298046)
aeroPerformance = aerodynamicPerformance(forces)
trim = trimChecker(aeroPerformance)

sim = flightSimulation(aeroPerformance, dt = 0.1)

initialState = {
    "x": 0,
    "y": 10668,
    "vx": forces.state.velocity,
    "vy": 0
}

history = sim.run(initialState, steps = 200)

animation = flightAnimation(history)
animation.animate()