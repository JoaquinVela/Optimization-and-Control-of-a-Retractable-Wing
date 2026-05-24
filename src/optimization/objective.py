from src.simulation.flightSim import flightSimulation
from src.models.geometry import wingGeometry
from src.models.aero import aerodynamicState
from src.models.plane import planeProperties
from src.control.control import altitudeHoldController

def runCandidate(params):
    wing = wingGeometry(
        span=params["span"],
        chord=params["chord"],
        deployment=params["initialDeployment"]
    )
    
    aeroState = aerodynamicState(
    rho=params["rho"],
    velocity=params["initialVelocity"],
    wing=wing,
    cl0=params["cl0"],
    cd0=params["cd0"],
    alphaRad=params["initialAlphaRad"]
    )

    plane = planeProperties(params["mass"])

    controller = altitudeHoldController(
        trimAlphaRad=params["initialAlphaRad"],
        targetAltitude=params["targetAltitude"],
        kp=params.get("kp", 0.00002),
        kd=params.get("kd", 0.002)
    )

    sim = flightSimulation(
    aeroState=aeroState,
    plane=plane,
    controller=controller,
    maxThrust=params["maxThrust"],
    altitude=params["initialAltitude"],
    velocityY=params.get("initialVelocityY", 0),
    cruisePowerLimit=params.get("cruisePowerLimit", 0.25)
    )

    return sim.run(
        totalTime=params.get("totalTime", 3000),
        dt=params.get("dt", 0.1)
    )

def evaluateCandidate(params):
    results = runCandidate(params)
    finalSpeed = results["velocity"][-1]
    finalMach = results["mach"][-1]
    finalAltitude = results["altitude"][-1]
    finalVelocityY = results["velocityY"][-1]
    maxMach = max(results["mach"])
    minDeployment = min(results["deployment"])
    maxAlphaRad = max(results["alphaRad"])
    maxAltitude = max(results["altitude"])
    minCutoffAltitude = min(results["cutoffAltitude"])
    averageThrust = sum(results["thrust"]) / len(results["thrust"])
    thrustFraction = averageThrust / params["maxThrust"]
    finalAltitudeError  = abs(finalAltitude - params["targetAltitude"])

    valid = (
        maxAltitude <= 12496.8
        and minCutoffAltitude >= 30
        and minDeployment >= 0.3
        and maxAlphaRad <= 0.15
        and abs(finalVelocityY) <= 5
        and finalAltitudeError <= 200
    )

    return {
        "finalSpeed": finalSpeed,
        "finalMach": finalMach,
        "finalAltitude": finalAltitude,
        "finalVelocityY": finalVelocityY,
        "maxMach": maxMach,
        "minDeployment": minDeployment,
        "maxAlphaRad": maxAlphaRad,
        "valid": valid,
        "maxAltitude": maxAltitude,
        "minCutoffAltitude": minCutoffAltitude,
        "averageThrust": averageThrust,
        "thrustFraction": thrustFraction,
        "finalAltitudeError": finalAltitudeError,
        "results": results
    }

if __name__ == "__main__":
    params = {
        "span": 64.8,
        "chord": 6.98,
        "initialDeployment": 1.0,
        "rho": 0.380,
        "initialVelocity": 248,
        "cl0": 0.2,
        "cd0": 0.02,
        "initialAlphaRad": 0.075,
        "mass": 274669.280707,
        "maxThrust": 1026000,
        "initialAltitude": 12000,
        "targetAltitude": 10668,
        "totalTime": 3000,
        "dt": 0.1
    }

    evaluation = evaluateCandidate(params)

    print("Final Speed:", evaluation["finalSpeed"])
    print("Final Mach:", evaluation["finalMach"])
    print("Final Altitude:", evaluation["finalAltitude"])
    print("Final Vertical Velocity:", evaluation["finalVelocityY"])
    print("Max Mach:", evaluation["maxMach"])
    print("Min Deployment:", evaluation["minDeployment"])
    print("Max AlphaRad:", evaluation["maxAlphaRad"])
    print("Valid:", evaluation["valid"])
    print("Max Altitude:", evaluation["maxAltitude"])
    print("Min Cutoff Altitude:", evaluation["minCutoffAltitude"])
    print("Final Altitude Error:", evaluation["finalAltitudeError"])
