def update_state(state, dt):
    state["mach"] += state["mach_rate_per_sec"] * dt
    state["altitude_ft"] += state["climb_rate_fps"] * dt
    state["velocity_mps"] += 0.2 * dt
    state["boom_margin_m"] -= state["boom_margin_rate_mps"] * dt

    if state["mach"] > 1.55:
        state["mach_rate_per_sec"] = -0.0006
    elif state["mach"] < 1.35:
        state["mach_rate_per_sec"] = 0.001
    
    if state["boom_margin_m"] < 35:
        state["boom_margin_rate_mps"] = -0.35
    elif state["boom_margin_m"] > 95:
        state["boom_margin_rate_mps"] = 0.55

    state["potential_mach"] = state["mach"] + 0.06