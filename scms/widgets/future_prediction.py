def draw_future_prediction(screen, rect, state, font_medium, font_small):
    predictions = [
        predict_state(state, 30),
        predict_state(state, 60),
    ]

    column_width = rect.width // 2

    for index, prediction in enumerate(predictions):
        x = rect.x + 24 + index * column_width
        y = rect.y + 52

        title = font_medium.render(
            f"+{prediction['time_s']} SEC",
            True,
            (0, 220, 255),
        )
        screen.blit(title, (x, y))

        lines = [
            f"MACH: {prediction['mach']:.2f}",
            f"ALT: {prediction['altitude_ft']:,.0f} ft",
            f"BOOM: {prediction['boom_margin_m']:+.0f} m",
        ]

        y += 48
        for line in lines:
            surface = font_small.render(line, True, (245, 245, 245))
            screen.blit(surface, (x, y))
            y += 30


def predict_state(state, seconds):
    return {
        "time_s": seconds,
        "mach": state["mach"] + state["mach_rate_per_sec"] * seconds,
        "altitude_ft": state["altitude_ft"] + state["climb_rate_fps"] * seconds,
        "boom_margin_m": state["boom_margin_m"]
        - state["boom_margin_rate_mps"] * seconds,
    }
