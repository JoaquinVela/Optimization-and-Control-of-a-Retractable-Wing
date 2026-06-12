def draw_top_bar_values(screen, rect, state, font_medium):
    status, status_color = get_status(state)

    items = [
        (150, f"MACH {state['mach']:.2f}", (245, 245, 245)),
        (330, f"ALT {state['altitude_ft']:,.0f} ft", (245, 245, 245)),
        (570, f"SPD {state['velocity_mps'] * 1.94384:.0f} knots", (245, 245, 245)),
        (830, "STATUS:", (245, 245, 245)),
        (950, status.strip(), status_color),
    ]

    y = rect.y + 15

    for x, text, color in items:
        surface = font_medium.render(text, True, color)
        screen.blit(surface, (x, y))


def get_status(state):
    margins = [
        state["boom_margin_m"] - state["min_boom_margin_m"],
        100 - state["thermal_usage_percent"],
        100 - state["dynamic_pressure_usage_percent"],
        100 - state["structural_usage_percent"],
        100 - state["engine_usage_percent"],
        100 - state["thrust_usage_percent"],
    ]

    if any(margin < 0 for margin in margins):
        return "VIOLATION", (230, 55, 50)
    if any(margin < 10 for margin in margins):
        return "CAUTION", (240, 205, 40)
    return "SAFE", (0, 210, 90)
