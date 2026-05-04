import matplotlib.pyplot as plt
from src.simulation.flightSim import flightSimulation
from src.models.geometry import wingGeometry
from src.models.aero import aerodynamicState
from src.models.plane import planeProperties
from src.models.forces import aerodynamicsForce
from src.models.performance import aerodynamicPerformance
from src.control.trim import trimChecker
from src.control.control import altitudeHoldController

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

sim = flightSimulation(
    aeroState=aeroState,
    plane=plane,
    controller=controller,
    thrust=242476.37271298046,
    altitude=10650,
    velocityY=0
)

results = sim.run(
    totalTime=1000,
    dt=0.1
)

print("Final Altitude:", results["altitude"][-1])
print("Final Vertical Velocity:", results["velocityY"][-1])
print("Final AlphaRad:", results["alphaRad"][-1])
print("Final CL:", results["cl"][-1])
print("Final Lift:", results["lift"][-1])
print("Final Weight:", results["weight"][-1])

plt.figure()
plt.plot(results["time"], results["altitude"])
plt.xlabel("Time [s]")
plt.ylabel("Altitude [m]")
plt.title("Altitude Hold Controller Test")
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
plt.plot(results["time"], results["alphaRad"])
plt.xlabel("Time [s]")
plt.ylabel("Angle of Attack [rad]")
plt.title("Angle of Attack vs. Time")
plt.grid()
plt.show()

plt.figure()
plt.plot(results["time"], results["cl"])
plt.xlabel("Time [s]")
plt.ylabel("Coefficient of Lift")
plt.title("CL vs. Time")
plt.grid()
plt.show()

plt.figure()
plt.plot(results["time"], results["lift"], label="Lift")
plt.plot(results["time"], results["weight"], label="Weight")
plt.xlabel("Time [s]")
plt.ylabel("Force [N]")
plt.title("Lift vs. Weight")
plt.legend()
plt.grid()
plt.show()
