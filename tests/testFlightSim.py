import matplotlib.pyplot as plt
from src.simulation.flightSim import flightSimulation
from src.models.geometry import wingGeometry
from src.models.aero import aerodynamicState
from src.models.plane import planeProperties
from src.models.forces import aerodynamicsForce
from src.models.performance import aerodynamicPerformance
from src.control.trim import trimChecker
from src.control.control import altitudeHoldController

wing = wingGeometry(span = 64.8, chord = 6.98)
aeroState = aerodynamicState(
    rho = 0.380,
    velocity = 248,
    wing = wing,
    cl0 = 0.2,
    cd0 = 0.02,
    alphaRad = 0.075
)
mass = 274669.280707
planeMaxThrust = 1026000
plane = planeProperties(mass)
controller = altitudeHoldController(trimAlphaRad=aeroState.alphaRad, targetAltitude=10668)
    
forces = aerodynamicsForce(aeroState, plane, thrust = planeMaxThrust * 0.25)
aeroPerformance = aerodynamicPerformance(forces)

sim = flightSimulation(
    aeroState=aeroState,
    plane=plane,
    controller=controller,
    maxThrust=planeMaxThrust,
    altitude=12000,
    velocityY=0
)

results = sim.run(
    totalTime=5000,
    dt=0.1
)

print("Final Altitude:", results["altitude"][-1])
print("Final Horizonal Velocity:", results["velocity"][-1])
print("Final Vertical Velocity:", results["velocityY"][-1])
print("Final AlphaRad:", results["alphaRad"][-1])
print("Final CL:", results["cl"][-1])
print("Final Lift:", results["lift"][-1])
print("Final Weight:", results["weight"][-1])
print("Final Thrust:", results["thrust"][-1])
print("Final Deployment:", results["deployment"][-1])

plt.figure()
plt.plot(results["time"], results["altitude"])
plt.xlabel("Time [s]")
plt.ylabel("Altitude [m]")
plt.title("Altitude Hold Controller Test")
plt.grid()
plt.show()

plt.figure()
plt.plot(results["time"], results["velocity"])
plt.xlabel("Time [s]")
plt.ylabel("VelocityX [m/s]")
plt.title("VelocityX vs. Time")
plt.grid()
plt.show()

plt.figure()
plt.plot(results["time"], results["velocityY"])
plt.axhline(0, linestyle="--")
plt.xlabel("Time [s]")
plt.ylabel("Vertical Velocity [m/s]")
plt.title("Vertical Velocity vs. Time")
plt.grid()
plt.show()

plt.figure()
plt.plot(results["time"], results["thrust"])
plt.xlabel("Time [s]")
plt.ylabel("Thrust [N]")
plt.title("Thrust vs. Time")
plt.grid()
plt.show()

plt.figure()
plt.plot(results["time"], results["deployment"])
plt.xlabel("Time [s]")
plt.ylabel("Deployment")
plt.title("Deployment vs. Time")
plt.grid()
plt.show()
