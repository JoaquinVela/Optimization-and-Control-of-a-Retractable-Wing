import ctypes
from pathlib import Path

library_path = Path(__file__).resolve().parents[1] / "c_src" / "libaero_core.so"

aero = ctypes.CDLL(str(library_path))

aero.lift_coefficient.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
]
aero.lift_coefficient.restype = ctypes.c_double

aero.dynamic_pressure.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
]

aero.dynamic_pressure.restype = ctypes.c_double

cl = aero.lift_coefficient(0.2, 0.05)
q = aero.dynamic_pressure(1.225, 145.0)

print("CL:", cl)
print("Dynamic Pressure:", q)