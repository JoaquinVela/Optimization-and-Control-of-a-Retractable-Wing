import pygame

def draw_auto_optimization(screen, rect, state, font_medium, font_small):
    enabled = state.get("auto_optimization_enabled", True)

    status = "ON" if enabled else "OFF"
    status_color = (0, 210, 90) if enabled else (240, 205, 40)

    switch_rect = pygame.Rect(rect.x + 24, rect.y + 52, 96, 42)
    knob_radius = 16
    knob_x = switch_rect.right - 24 if enabled else switch_rect.x + 24
    knob_y = switch_rect.centery

    pygame.draw.rect(
        screen,
        (0, 95, 70) if enabled else (70, 62, 35),
        switch_rect,
        border_radius=21,
    )
    pygame.draw.circle(screen, (245, 245, 245), (knob_x, knob_y), knob_radius)

    status_surface = font_medium.render(status, True, status_color)
    screen.blit(status_surface, (switch_rect.right + 20, rect.y + 57))

    mode = "AUTO SPEED OPTIMIZATION" if enabled else "PILOT MANUAL CONTROL"
    mode_surface = font_small.render(mode, True, (245, 245, 245))
    screen.blit(mode_surface, (rect.x + 24, rect.y + 108))

    if not enabled:
        lines = [
            f"ALT TARGET: {state['manual_target_altitude_ft']:,.0f} ft",
            f"DEPLOYMENT: {state['manual_deployment'] * 100:.0f}%",
            f"THRUST: {state['manual_thrust_percent']:.0f}%",
        ]

        x = rect.x + 235
        y = rect.y + 48
        for line in lines:
            surface = font_small.render(line, True, (245, 245, 245))
            screen.blit(surface, (x, y))
            y += 28