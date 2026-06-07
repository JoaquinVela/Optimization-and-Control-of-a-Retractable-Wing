import pygame


def draw_constraint_health(screen, rect, state, font_small):
    constraints = [
        ("BOOM", state["boom_usage_percent"]),
        ("THERMAL", state["thermal_usage_percent"]),
        ("Q LIMIT", state["dynamic_pressure_usage_percent"]),
        ("STRUCT", state["structural_usage_percent"]),
        ("ENGINE", state["engine_usage_percent"]),
        ("THRUST", state["thrust_usage_percent"]),
    ]

    active_limiter, active_value = max(constraints, key=lambda item: item[1])

    label_surface = font_small.render(
        f"ACTIVE LIMITER: {active_limiter}",
        True,
        (0, 220, 255),
    )
    screen.blit(label_surface, (rect.x + 425, rect.y + 10))

    bar_x = rect.x + 120
    bar_width = rect.width - 210
    bar_height = 10

    y = rect.y + 64
    for name, usage in constraints:
        if usage > 100:
            color = (230, 55, 50)
        elif usage >= 90:
            color = (255, 165, 40)
        elif usage >= 70:
            color = (240, 205, 40)
        else:
            color = (0, 210, 90)

        name_surface = font_small.render(name, True, (245, 245, 245))
        screen.blit(name_surface, (rect.x + 18, y - 30))

        pygame.draw.rect(
            screen,
            (40, 45, 52),
            pygame.Rect(bar_x, y - 25, bar_width, bar_height),
        )

        fill_width = int(bar_width * min(usage, 120) / 120)
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(bar_x, y - 25, fill_width, bar_height),
        )

        percent_surface = font_small.render(
            f"{usage:.0f}%",
            True,
            color,
        )
        screen.blit(percent_surface, (bar_x + bar_width + 12, y - 31))

        y += 18
