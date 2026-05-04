import matplotlib.pyplot as plt
from src.simulation.flightSim import flightSimulation
from src.models.geometry import wingGeometry
from src.models.aero import aerodynamicState
from src.models.plane import planeProperties
from src.models.forces import aerodynamicsForce
from src.models.performance import aerodynamicPerformance
from src.control.trim import trimChecker
from src.control.control import altitudeHoldController
from src.simulation.animation import flightAnimation

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
controller = altitudeHoldController(trimAlphaRad=aeroState.alphaRad, targetAltitude=10668)
    
forces = aerodynamicsForce(aeroState, plane, thrust = 242476.37271298046)
aeroPerformance = aerodynamicPerformance(forces)

sim = flightSimulation(aeroState, plane, controller, thrust=242476.37271298046, altitude=10600)

history = sim.run(totalTime=1000, dt=0.1)

animation = flightAnimation(history)
animation.animate()