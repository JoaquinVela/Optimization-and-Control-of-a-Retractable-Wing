"""
Wrapper for aero_core.c functions

"""

import ctypes
from pathlib import Path

library_path = Path(__file__).resolve().parents[2] / "c_src" / "libaero_core.so"

aero = ctypes.CDLL(str(library_path))

class AeroInput(ctypes.Structure):
    _fields_ = [
        ("rho", ctypes.c_double),
        ("velocity", ctypes.c_double),
        ("wing_area", ctypes.c_double),
        ("aspect_ratio", ctypes.c_double),
        ("cl0", ctypes.c_double),
        ("cd0", ctypes.c_double),
        ("alpha_rad", ctypes.c_double),
        ("oswald_efficiency", ctypes.c_double),
        ("mach", ctypes.c_double),
        ("mass", ctypes.c_double),
        ("thrust", ctypes.c_double),
    ]

class AeroOutput(ctypes.Structure):
    _fields_ = [
        ("cl", ctypes.c_double),
        ("cd", ctypes.c_double),
        ("dynamic_pressure", ctypes.c_double),
        ("lift", ctypes.c_double),
        ("drag", ctypes.c_double),
        ("weight", ctypes.c_double),
        ("net_force_x", ctypes.c_double),
        ("net_force_y", ctypes.c_double),
        ("acc_x", ctypes.c_double),
        ("acc_y", ctypes.c_double),
    ]

aero.calculate_aero_state.argtypes = [
    ctypes.POINTER(AeroInput),
    ctypes.POINTER(AeroOutput),
]
aero.calculate_aero_state.restype = None

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

aero.air_density_at_altitude.argtypes = [
    ctypes.c_double,
]
aero.air_density_at_altitude.restype = ctypes.c_double

aero.speed_of_sound.argtypes = [
    ctypes.c_double,
]
aero.speed_of_sound.restype = ctypes.c_double

aero.mach_number.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
]
aero.mach_number.restype = ctypes.c_double

aero.dynamic_trim_alpha.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]
aero.dynamic_trim_alpha.restype = ctypes.c_double

aero.clamp.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]
aero.clamp.restype = ctypes.c_double

aero.rate_limit.argtypes = [
    ctypes.c_double, 
    ctypes.c_double,
    ctypes.c_double,
]
aero.rate_limit.restype = ctypes.c_double

aero.cutoff_altitude_agl.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]
aero.cutoff_altitude_agl.restype = ctypes.c_double

aero.temperature_at_altitude.argtypes = [
    ctypes.c_double,
]
aero.temperature_at_altitude.restype = ctypes.c_double