import math
from dataclasses import dataclass 

@dataclass 
class DisplayState:
    time_s: float
    altitude_ft: float
    target_altitude_ft: float
    airspeed_kt: float
    mach: float
    pitch_deg: float
    roll_deg: float
    heading_deg: float
    vertical_speed_fpm: float
    alpha_rad: float
    deployment: float
    wing_retraction_percent: float
    boom_margin_m: float
    cutoff_altitude_agl_m: float
    green_speed_min_kt: float
    green_speed_max_kt: float
    yellow_speed_min_kt: float
    yellow_speed_max_kt: float
    red_speed_min_kt: float
    red_speed_max_kt: float
    optimal_boomless_speed_kt: float
    status: str

def wing_retraction_percent_from_deployment(deployment):
    return (1.0 - deployment) / (1.0 - 0.3) * 100.0

def create_demo_state(t):
    airspeed_kt = 800.0 + 45.0 * math.sin(t * 0.35)
    altitude_ft = 39000.0 + 900.0 * math.sin(t * 0.18)
    target_altitude_ft = 40000.0
    mach = airspeed_kt / 666.7

    pitch_deg = 3.0 * math.sin(t * 0.7)
    roll_deg = 0.0
    heading_deg = 0.0
    vertical_speed_fpm = 600.0 * math.sin(t * 0.18)

    deployment = 0.65 + 0.25 * math.sin(t * 0.25)
    deployment = max(0.3, min(1.0, deployment))
    wing_retraction_percent = wing_retraction_percent_from_deployment(deployment)

    cutoff_altitude_agl_m = 45.0 + 65.0 * math.sin(t * 0.3)
    boom_margin_m = cutoff_altitude_agl_m - 30.0

    if cutoff_altitude_agl_m >= 30.0:
        status = "BOOMLESS CRUISE AVAILABLE"
    elif cutoff_altitude_agl_m > 0.0:
        status = "MARGINAL BOOM CUTOFF"
    else:
        status = "SONIC BOOM REACHES GROUND"
    
    return DisplayState(
        time_s=t,
        altitude_ft=altitude_ft,
        target_altitude_ft=target_altitude_ft,
        airspeed_kt=airspeed_kt,
        mach=mach,
        pitch_deg=pitch_deg,
        roll_deg=roll_deg,
        heading_deg=heading_deg,
        vertical_speed_fpm=vertical_speed_fpm,
        alpha_rad=0.07,
        deployment=deployment,
        wing_retraction_percent=wing_retraction_percent,
        boom_margin_m=boom_margin_m,
        cutoff_altitude_agl_m=cutoff_altitude_agl_m,
        green_speed_min_kt=667.0,
        green_speed_max_kt=800.0,
        yellow_speed_min_kt=800.0,
        yellow_speed_max_kt=866.0,
        red_speed_min_kt=866.0,
        red_speed_max_kt=900.0,
        optimal_boomless_speed_kt=485.0,
        status=status
    )

