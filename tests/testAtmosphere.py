from src.models.atmosphere import cruiseAtmosphere

altitude = 10668
velocity = 300
atm = cruiseAtmosphere(altitude)

print("Temperature:", atm.temperature())
print("Pressure:", atm.pressure())
print("Density:", atm.density())
print("Speed of Sound:", atm.speedOfSound())
print("Mach Number:", atm.machNumber(velocity))