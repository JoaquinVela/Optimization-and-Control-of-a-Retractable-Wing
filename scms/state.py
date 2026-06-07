def create_initial_state():
    return {
        "mach": 1.42,
        "altitude_ft": 40000,
        "velocity_mps": 465,
        "vertical_speed_fpm": 600,

        "boom_margin_m": 82,
        "min_boom_margin_m": 30,

        "deployment": 0.72,
        "alpha_deg": 1.4,
        "lift_to_drag": 15.2,

        "thrust_percent": 76,
        "fuel_flow_percent": 100,

        "thermal_usage_percent": 48,
        "dynamic_pressure_usage_percent": 41,
        "structural_usage_percent": 35,
        "engine_usage_percent": 42,
        "boom_usage_percent": 65,
        "thrust_usage_percent": 76,

        "potential_mach": 1.48,
        "recommended_altitude_change_ft": 2000,
        "recommended_deployment_change_percent": -8,
        "recommended_thrust_change_percent": 4,

        "mach_rate_per_sec": 0.001,
        "climb_rate_fps": 10,
        "boom_margin_rate_mps": 0.55,

        "auto_optimization_enabled": True,
        "manual_target_altitude_ft": 40000,
        "manual_deployment": 1.0,
        "manual_thrust_percent": 25,
    }