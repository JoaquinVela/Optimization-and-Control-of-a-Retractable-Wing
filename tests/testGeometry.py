from src.models.geometry import wingGeometry

wing = wingGeometry(span = 10, chord = 2)

print("Area", wing.area())
print("Aspect Ratio", wing.aspectRatio())

