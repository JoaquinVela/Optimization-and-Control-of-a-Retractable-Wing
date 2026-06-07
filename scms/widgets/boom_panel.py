import pygame


def draw_boom_panel(screen, rect, state, font_small):
    margin = state["boom_margin_m"]
    minimum = state["min_boom_margin_m"]

    if margin < minimum:
        status = "VIOLATION"
        color = (230, 55, 50)
    elif margin < 60:
        status = "CAUTION"
        color = (240, 205, 40)
    else:
        status = "SAFE"
        color = (0, 210, 90)

    lines = [
        "BOOM MARGIN",
        f"{margin:+.0f} m",
        "",
        "MIN REQUIRED",
        f"{minimum:+.0f} m",
        "",
        "STATUS",
        status,
    ]

    y = rect.y + 48
    for line in lines:
        line_color = color if line == status or "m" in line else (245, 245, 245)
        surface = font_small.render(line, True, line_color)
        screen.blit(surface, (rect.x + 18, y))
        y += 24

    gauge_x = rect.right - 48
    gauge_top = rect.y + 48
    gauge_height = rect.height - 78
    gauge_width = 18

    pygame.draw.rect(
        screen,
        (40, 45, 52),
        pygame.Rect(gauge_x, gauge_top, gauge_width, gauge_height),
    )

    max_margin = 150
    fill_fraction = max(0, min(1, margin / max_margin))
    fill_height = int(gauge_height * fill_fraction)

    pygame.draw.rect(
        screen,
        color,
        pygame.Rect(
            gauge_x,
            gauge_top + gauge_height - fill_height,
            gauge_width,
            fill_height,
        ),
    )

    limit_fraction = max(0, min(1, minimum / max_margin))
    limit_y = gauge_top + gauge_height - int(gauge_height * limit_fraction)

    pygame.draw.line(
        screen,
        (245, 245, 245),
        (gauge_x - 8, limit_y),
        (gauge_x + gauge_width + 8, limit_y),
        2,
    )

    limit_surface = font_small.render("LIMIT", True, (245, 245, 245))
    screen.blit(limit_surface, (gauge_x - 62, limit_y - 10))
