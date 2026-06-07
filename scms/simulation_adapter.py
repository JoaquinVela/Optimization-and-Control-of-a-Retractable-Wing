import math

def apply_simulation_sample(state, sample, dt):
    previous_mach = state["mach"]
    previous_altitude_ft = state["altitude_ft"]
    previous_boom_margin_m = state["boom_margin_m"]

    state["mach"] = sample["mach"]
    state["altitude_ft"] = sample["altitude_ft"]
    state["velocity_mps"] = sample["velocity_mps"]
    state["deployment"] = sample["deployment"]
    state["alpha_deg"] = sample["alpha_deg"]
    state["lift_to_drag"] = sample["lift_to_drag"]
    state["boom_margin_m"] = sample["boom_margin_m"]
    state["thrust_percent"] = sample["thrust_percent"]

    if dt > 0:
        state["mach_rate_per_sec"] = (state["mach"] - previous_mach) / dt
        state["climb_rate_fps"] = (state["altitude_ft"] - previous_altitude_ft) / dt
        state["vertical_speed_fpm"] = state["climb_rate_fps"] * 60
        state["boom_margin_rate_mps"] = (
            previous_boom_margin_m - state["boom_margin_m"]
        ) / dt

    state["thermal_usage_percent"] = sample.get(
        "thermal_usage_percent",
        state["thermal_usage_percent"],
    )
    state["dynamic_pressure_usage_percent"] = sample.get(
        "dynamic_pressure_usage_percent",
        state["dynamic_pressure_usage_percent"],
    )
    state["structural_usage_percent"] = sample.get(
        "structural_usage_percent",
        state["structural_usage_percent"],
    )
    state["engine_usage_percent"] = sample.get(
        "engine_usage_percent",
        state["engine_usage_percent"],
    )
    state["boom_usage_percent"] = sample.get(
        "boom_usage_percent",
        100 * state["min_boom_margin_m"] / max(state["boom_margin_m"], 1),
    )
    state["thrust_usage_percent"] = sample.get(
        "thrust_usage_percent",
        state["thrust_percent"],
    )

    state["potential_mach"] = sample.get(
        "potential_mach",
        state["mach"] + 0.06,
    )
    state["recommended_altitude_change_ft"] = sample.get(
        "recommended_altitude_change_ft",
        state["recommended_altitude_change_ft"],
    )
    state["recommended_deployment_change_percent"] = sample.get(
        "recommended_deployment_change_percent",
        state["recommended_deployment_change_percent"],
    )
    state["recommended_thrust_change_percent"] = sample.get(
        "recommended_thrust_change_percent",
        state["recommended_thrust_change_percent"],
    )

    state["supersonic_envelope"] = sample.get(
        "supersonic_envelope",
        state.get("supersonic_envelope", []),
    )

    state["auto_optimization_enabled"] = sample.get(
    "auto_optimization_enabled",
    state.get("auto_optimization_enabled", True),
    )
    state["manual_target_altitude_ft"] = sample.get(
        "manual_target_altitude_ft",
        state.get("manual_target_altitude_ft", state["altitude_ft"]),
    )
    state["manual_deployment"] = sample.get(
        "manual_deployment",
        state.get("manual_deployment", state["deployment"]),
    )
    state["manual_thrust_percent"] = sample.get(
        "manual_thrust_percent",
        state.get("manual_thrust_percent", state["thrust_percent"]),
    )