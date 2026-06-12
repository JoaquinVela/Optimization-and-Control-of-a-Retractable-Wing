import pygame


def draw_envelope_plot(screen, rect, state, font_small):
    plot_rect = pygame.Rect(
        rect.x + 58,
        rect.y + 60,
        rect.width - 88,
        rect.height - 122,
    )

    mach_min = 0.9
    mach_max = 1.9
    altitude_min_ft = 25000
    altitude_max_ft = 50000

    safe_envelope = state.get("supersonic_envelope", [])

    pygame.draw.rect(screen, (8, 12, 18), plot_rect)

    draw_plot_grid(screen, plot_rect)

    envelope_points = [
        map_envelope_point(
            mach,
            altitude,
            plot_rect,
            mach_min,
            mach_max,
            altitude_min_ft,
            altitude_max_ft,
        )
        for mach, altitude in safe_envelope
    ]

    current_point = map_envelope_point(
        state["mach"],
        state["altitude_ft"],
        plot_rect,
        mach_min,
        mach_max,
        altitude_min_ft,
        altitude_max_ft,
    )

    future_mach = state["mach"] + state["mach_rate_per_sec"] * 60
    future_altitude = state["altitude_ft"] + state["climb_rate_fps"] * 60

    future_point = map_envelope_point(
        future_mach,
        future_altitude,
        plot_rect,
        mach_min,
        mach_max,
        altitude_min_ft,
        altitude_max_ft,
    )

    previous_clip = screen.get_clip()
    screen.set_clip(plot_rect)

    if len(envelope_points) >= 3:
        pygame.draw.polygon(screen, (20, 80, 70), envelope_points)
        pygame.draw.polygon(screen, (0, 210, 90), envelope_points, 2)

    pygame.draw.line(screen, (0, 220, 255), current_point, future_point, 2)
    pygame.draw.circle(screen, (0, 220, 255), current_point, 7)
    pygame.draw.circle(screen, (245, 245, 245), current_point, 11, 2)
    pygame.draw.circle(screen, (240, 205, 40), future_point, 5)

    future_surface = font_small.render("+60s", True, (240, 205, 40))
    screen.blit(future_surface, (future_point[0] + 10, future_point[1] - 10))

    screen.set_clip(previous_clip)

    pygame.draw.rect(screen, (90, 96, 105), plot_rect, 1)

    mach_label = font_small.render("MACH", True, (245, 245, 245))
    screen.blit(
        mach_label,
        (plot_rect.centerx - mach_label.get_width() // 2, rect.bottom - 30),
    )

    altitude_label = font_small.render("ALTITUDE", True, (245, 245, 245))
    screen.blit(altitude_label, (rect.x + 10, plot_rect.y - 29))

    draw_axis_labels(
        screen,
        plot_rect,
        mach_min,
        mach_max,
        altitude_min_ft,
        altitude_max_ft,
        font_small,
    )

def map_envelope_point(
    mach,
    altitude_ft,
    plot_rect,
    mach_min,
    mach_max,
    altitude_min_ft,
    altitude_max_ft,
):
    mach_fraction = (mach - mach_min) / (mach_max - mach_min)
    altitude_fraction = (altitude_ft - altitude_min_ft) / (
        altitude_max_ft - altitude_min_ft
    )

    x = plot_rect.x + int(mach_fraction * plot_rect.width)
    y = plot_rect.bottom - int(altitude_fraction * plot_rect.height)

    return x, y


def draw_plot_grid(screen, plot_rect):
    grid_color = (30, 38, 48)

    for i in range(1, 5):
        x = plot_rect.x + int(plot_rect.width * i / 5)
        pygame.draw.line(
            screen,
            grid_color,
            (x, plot_rect.y),
            (x, plot_rect.bottom),
            1,
        )

    for i in range(1, 5):
        y = plot_rect.y + int(plot_rect.height * i / 5)
        pygame.draw.line(
            screen,
            grid_color,
            (plot_rect.x, y),
            (plot_rect.right, y),
            1,
        )


def draw_axis_labels(
    screen,
    plot_rect,
    mach_min,
    mach_max,
    altitude_min_ft,
    altitude_max_ft,
    font_small,
):
    for mach in [0.9, 1.1, 1.3, 1.5, 1.7, 1.9]:
        x = plot_rect.x + int((mach - mach_min) / (mach_max - mach_min) * plot_rect.width)
        pygame.draw.line(
            screen,
            (90, 96, 105),
            (x, plot_rect.bottom),
            (x, plot_rect.bottom + 5),
            1,
        )
        label = font_small.render(f"{mach:.1f}", True, (170, 178, 190))
        screen.blit(label, (x - label.get_width() // 2, plot_rect.bottom + 8))

    for altitude in [25000, 30000, 35000, 40000, 45000, 50000]:
        y = plot_rect.bottom - int(
            (altitude - altitude_min_ft)
            / (altitude_max_ft - altitude_min_ft)
            * plot_rect.height
        )
        pygame.draw.line(
            screen,
            (90, 96, 105),
            (plot_rect.x - 5, y),
            (plot_rect.x, y),
            1,
        )
        label = font_small.render(f"{altitude // 1000}k", True, (170, 178, 190))
        screen.blit(label, (plot_rect.x - 42, y - 9))
