import pygame


def draw_wing_configuration(screen, rect, state, font_small):
    deployment = state["deployment"]
    deployment_percent = deployment * 100

    lines = [
        f"DEPLOYMENT: {deployment_percent:.0f}%",
        f"ALPHA: {state['alpha_deg']:.1f} deg",
        f"L/D: {state['lift_to_drag']:.1f}",
    ]

    y = rect.y + 48
    for line in lines:
        surface = font_small.render(line, True, (245, 245, 245))
        screen.blit(surface, (rect.x + 18, y))
        y += 28

    center_x = rect.centerx
    center_y = rect.y + 195

    body_length = 86
    body_width = 14

    pygame.draw.line(
        screen,
        (245, 245, 245),
        (center_x, center_y - body_length // 2),
        (center_x, center_y + body_length // 2),
        body_width,
    )

    pygame.draw.polygon(
        screen,
        (245, 245, 245),
        [
            (center_x, center_y - body_length // 2 - 18),
            (center_x - 12, center_y - body_length // 2 + 8),
            (center_x + 12, center_y - body_length // 2 + 8),
        ],
    )

    min_span = 42
    max_span = 98
    span = min_span + (deployment - 0.3) / (1.0 - 0.3) * (max_span - min_span)

    wing_color = (0, 220, 255)
    if deployment < 0.45:
        wing_color = (240, 205, 40)

    left_wing = [
        (center_x - 6, center_y - 8),
        (center_x - span, center_y + 12),
        (center_x - span, center_y + 32),
        (center_x - 6, center_y + 12),
    ]

    right_wing = [
        (center_x + 6, center_y - 8),
        (center_x + span, center_y + 12),
        (center_x + span, center_y + 32),
        (center_x + 6, center_y + 12),
    ]

    pygame.draw.polygon(screen, wing_color, left_wing)
    pygame.draw.polygon(screen, wing_color, right_wing)

    pygame.draw.polygon(screen, (245, 245, 245), left_wing, 2)
    pygame.draw.polygon(screen, (245, 245, 245), right_wing, 2)

    tail_span = 36
    tail_y = center_y + body_length // 2 - 16

    pygame.draw.line(
        screen,
        (245, 245, 245),
        (center_x - tail_span, tail_y),
        (center_x + tail_span, tail_y),
        5,
    )
