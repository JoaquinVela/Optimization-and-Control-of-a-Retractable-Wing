def draw_optimization_advisor(screen, rect, state, font_small):
    recommendation, action_status, action_color = get_recommendation(state)

    current_mach = state["mach"]
    potential_mach = state["potential_mach"]
    speed_gain = potential_mach - current_mach

    left_x = rect.x + 22
    right_x = rect.x + 320
    y = rect.y + 42

    metrics = [
        ("CURRENT MACH:", f"{current_mach:.2f}"),
        ("POTENTIAL MACH:", f"{potential_mach:.2f}"),
        ("SPEED GAIN:", f"{speed_gain:+.2f} Mach"),
    ]

    for label, value in metrics:
        label_surface = font_small.render(label, True, (170, 178, 190))
        value_surface = font_small.render(value, True, (245, 245, 245))
        screen.blit(label_surface, (left_x, y))
        screen.blit(value_surface, (left_x + 170, y))
        y += 25

    rec_title = font_small.render(
        "RECOMMENDED ACTION:",
        True,
        (170, 178, 190)
    )
    screen.blit(rec_title, (right_x, rect.y + 42))

    rec_surface = font_small.render(
        recommendation,
        True,
        (245, 245, 245),
    )
    screen.blit(rec_surface, (right_x, rect.y + 68))

    status_label = font_small.render(
        "ACTION STATUS:",
        True,
        (170, 178, 190),
    )
    status_surface = font_small.render(
        action_status,
        True,
        action_color,
    )

    screen.blit(status_label, (right_x, rect.y + 96))
    screen.blit(status_surface, (right_x + 150, rect.y + 96))


def get_recommendation(state):
    boom_margin = state["boom_margin_m"]
    min_boom_margin = state["min_boom_margin_m"]
    deployment = state["deployment"]
    thrust_percent = state["thrust_percent"]

    if boom_margin < min_boom_margin:
        return (
            "CLIMB IMMEDIATLEY",
            " BLOCKED BY BOOM LIMIT",
            (230, 55, 50),
        )

    if boom_margin < 45:
        return (
            "CLIMB +2,000 ft BEFORE ACCELERATING",
            " LIMITED BY BOOM MARGIN",
            (240, 205, 40),
        )

    if deployment > 0.5:
        deployment_change = state["recommended_deployment_change_percent"]
        return (
            f"RETRACT WING {abs(deployment_change):.0f}%",
            " APPROVED",
            (0, 210, 90),
        )

    if thrust_percent < 80:
        thrust_change = state["recommended_thrust_change_percent"]
        return (
            f"INCREASE THRUST {thrust_change:.0f}%",
            " APPROVED",
            (0, 210, 90),
        )

    return (
        "MAINTAIN CURRENT CONFIGURATION",
        " APPROVED",
        (0, 210, 90),
    )
