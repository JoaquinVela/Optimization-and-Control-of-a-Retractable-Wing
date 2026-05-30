from scipy.optimize import differential_evolution
from src.optimization.objective import evaluateCandidate

def buildParams(x):
    targetAltitude = x[0]
    initialDeployment = x[1]
    initialAlphaRad = x[2]
    kp = x[3]
    kd = x[4]
    cruisePowerLimit = x[5]

    return {
        "span": 64.8,
        "chord": 6.98,
        "initialDeployment": initialDeployment,
        "rho": 0.380,
        "initialVelocity": 248,
        "cl0": 0.2,
        "cd0": 0.02,
        "initialAlphaRad": initialAlphaRad,
        "mass": 274669.280707,
        "maxThrust": 1026000,
        "initialAltitude": 12000,
        "targetAltitude": targetAltitude,
        "kp": kp,
        "kd": kd,
        "cruisePowerLimit": cruisePowerLimit,
        "totalTime": 3000,
        "dt": 0.1
    }

def objective(x):
    params = buildParams(x)
    evaluation = evaluateCandidate(params)

    if not evaluation["valid"]:
        penalty = 1e6

        if evaluation["minCutoffAltitude"] < 30:
            penalty += 10000 * (30 - evaluation["minCutoffAltitude"])

        if evaluation ["maxAltitude"] > 12496.8:
            penalty += 10000 * (evaluation["maxAltitude"] - 12496.8)

        penalty += 1000 * abs(evaluation["finalVelocityY"])
        penalty += 100 * evaluation["finalAltitudeError"]

        return penalty
    
    speedReward = -evaluation["finalSpeed"]
    thrustPenalty = 20 * evaluation["thrustFraction"]

    return speedReward + thrustPenalty

if __name__ ==  "__main__":
    bounds = [
        (8000, 12496.8), # targetAltitude
        (0.3, 1.0), #initialDeployment
        (0.03, 0.10), # initialAlphaRad 
        (0.000005, 0.00005),  # kp
        (0.0005, 0.006), # kd
        (0.15, 0.35) # cruisePowerLimit
    ]

    result = differential_evolution(
        objective, 
        bounds, 
        maxiter=30,
        popsize=8,
        polish=False,
        seed=1
    )

    bestParams = buildParams(result.x)
    bestEvaluation = evaluateCandidate(bestParams)

    print("Best Target Altitude:", bestParams["targetAltitude"])
    print("Best Initial Deployment:", bestParams["initialDeployment"])
    print("Best Initial Alpha:", bestParams["initialAlphaRad"])
    print("Best Kp:", bestParams["kp"])
    print("Best Kd:", bestParams["kd"])
    print("Best Final Speed:", bestEvaluation["finalSpeed"])
    print("Best Mach:", bestEvaluation["finalMach"])
    print("Best Final Altitude:", bestEvaluation["finalAltitude"])
    print("Best Final Vertical Velocity:", bestEvaluation["finalVelocityY"])
    print("Valid:", bestEvaluation["valid"])
    print("Max Altitude:", bestEvaluation["maxAltitude"])
    print("Min Cutoff Altitude:", bestEvaluation["minCutoffAltitude"])
    print("Best Cruise Power Limit:", bestParams["cruisePowerLimit"])
    print("Average Thrust:", bestEvaluation["averageThrust"])
    print("Average Thrust Fraction:", bestEvaluation["thrustFraction"])
    print("Final Altitude Error:", bestEvaluation["finalAltitudeError"])
    print("Optimizer Success:", result.success)
    print("Optimizer Score:", result.fun)

    # PLOTTING 
    import matplotlib.pyplot as plt

    results = bestEvaluation["results"]

    plt.figure()
    plt.plot(results["time"], results["velocity"])
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [m/s]")
    plt.title("Best Candidate Velocity")
    plt.grid()
    plt.show()
    
    plt.figure()
    plt.plot(results["time"], results["altitude"])
    plt.xlabel("Time [s]")
    plt.ylabel("Altitude [m]")
    plt.title("Best Candidate Altitude")
    plt.grid()
    plt.show()

    plt.figure()
    plt.plot(results["time"], results["thrust"])
    plt.xlabel("Time [s]")
    plt.ylabel("Thrust [N]")
    plt.title("Best Candidate Thrust")
    plt.grid()
    plt.show()