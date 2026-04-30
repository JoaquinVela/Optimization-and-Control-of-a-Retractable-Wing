import matplotlib.pyplot as plt
from src.simulation.flightSim import flightSimulation
from src.models.geometry import wingGeometry
from src.models.aero import aerodynamicState
from src.models.plane import planeProperties
from src.models.forces import aerodynamicsForce
from src.models.performance import aerodynamicPerformance
from src.control.trim import trimChecker

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

sim = flightSimulation(aeroPerformance, dt = 0.1)

initialState = {
    "x": 0,
    "y": 10668,
    "vx": aeroState.velocity,
    "vy": 0 
}

print(aeroState.velocity)

history = sim.run(initialState, steps = 200)

xVals = [s["x"] for s in history]
yVals = [s["y"] for s in history]

plt.plot(xVals, yVals)
plt.xlabel("Horizontal Position x [m]")
plt.ylabel("Vertical Position y [m]")
plt.title("Simple 2D Flight Path Simulation")
plt.grid()
plt.show()