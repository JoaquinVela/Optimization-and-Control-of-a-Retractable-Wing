from src.control.cruiseScheduler import cruiseSchedule
from src.models.atmosphere import cruiseAtmosphere

altitude = 10668
velocity = 300
deployment0 = 1.0

scheduler = cruiseSchedule()
atmosphere = cruiseAtmosphere(altitude)

targetAltitude, deployment, mach = scheduler.chooseTarget(
    altitude,
    velocity,
    atmosphere,
    deployment0
)

print("Current Altitude:", altitude)
print("Current Velocity:", velocity)
print("Mach Number:", mach)
print("Target Altitude:", targetAltitude)
print("Target Deploymnet:", deployment)