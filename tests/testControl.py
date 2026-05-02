from src.control.control import altitudeHoldController

controller = altitudeHoldController(
    targetAltitude=10668,
    tolerance=5,
    liftChange=0.02
)

currentCl = 0.5

# Case 1: Aircraft is too low
newCl = controller.command(
    currentAltitude=10650,
    currentCl=currentCl
)
print("Too low Cl:", newCl)

# Case 2: Aircraft is too high
newCl = controller.command(
    currentAltitude=10690,
    currentCl=currentCl
)
print("Too high Cl:", newCl)

# Case 3: Aircraft is close enough
newCl = controller.command(
    currentAltitude=10667,
    currentCl=currentCl
)
print("Close enough Cl:", newCl)