"""
Wrapper for aero_core.c functions

"""

import ctypes
from pathlib import Path

library_path = Path(__file__).resolve().parents[2] / "c_src" / "libaero_core.so"

aero = ctypes.CDLL(str(library_path))

aero.dynamic_pressure.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
]
aero.dynamic_pressure.restype = ctypes.c_double

aero.lift_coefficient.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
]
aero.lift_coefficient.restype = ctypes.c_double

aero.drag_coefficient.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]
aero.drag_coefficient.restype = ctypes.c_double

aero.lift_force.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]
aero.lift_force.restype = ctypes.c_double

aero.drag_force.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]
aero.drag_force.restype = ctypes.c_double

aero.weight_force.argtypes = [
    ctypes.c_double,
]
aero.weight_force.restype = ctypes.c_double

aero.acceleration_x.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]
aero.acceleration_x.restype = ctypes.c_double

aero.acceleration_y.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]
aero.acceleration_y.restype = ctypes.c_double