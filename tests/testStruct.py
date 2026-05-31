import ctypes

from src.models.aero_c import aero, AeroInput, AeroOutput

inputs = AeroInput(
    rho=0.38,
    velocity=248.0,
    wing_area=452.304,
    aspect_ratio=9.283,
    cl0=0.2,
    cd0=0.02,
    alpha_rad=0.075,
    oswald_efficiency=0.8,
    mach=0.85,
)

outputs = AeroOutput()

aero.calculate_aero_state(
    ctypes.byref(inputs),
    ctypes.byref(outputs)
)

print("CL:", outputs.cl)
print("CD:", outputs.cd)
print("Dynamic Pressure:", outputs.dynamic_pressure)
print("Lift:", outputs.lift)
print("Drag:", outputs.drag)