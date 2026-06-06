import pygame

from display.colors import BLACK, WHITE, CYAN, MAGENTA
from display.geometry import clamp, draw_centered_text


def draw_altitude_tape(screen, state, rect):
    pygame.draw.rect(screen, BLACK, rect)
    pygame.draw.rect(screen, WHITE, rect, 2)

    font = pygame.font.SysFont("Arial", 20, bold=True)
    small_font = pygame.font.SysFont("Arial", 16, bold=True)
    label_font = pygame.font.SysFont("Arial", 14, bold=True)

    center_y = rect.centery
    pixels_per_foot = 0.15
    visible_range_ft = rect.height / pixels_per_foot

    min_altitude = state.altitude_ft - visible_range_ft / 2
    max_altitude = state.altitude_ft + visible_range_ft / 2

    start_tick = int(min_altitude // 500 * 500)
    end_tick = int(max_altitude // 500 * 500 + 500)

    for altitude in range(start_tick, end_tick + 1, 100):
        y = altitude_to_y(altitude, state.altitude_ft, center_y, pixels_per_foot)

        if y < rect.top or y > rect.bottom:
            continue

        tick_width = 42 if altitude % 500 == 0 else 24

        pygame.draw.line(
            screen,
            WHITE,
            (rect.left + 4, y),
            (rect.left + tick_width, y),
            2,
        )

        if altitude % 500 == 0:
            label = small_font.render(str(altitude), True, WHITE)
            screen.blit(
                label,
                (rect.right - label.get_width() - 10, y - label.get_height() // 2),
            )

    draw_target_altitude_bug(screen, state, rect, pixels_per_foot)
    draw_current_altitude_box(screen, state, rect, font)
    draw_vertical_speed(screen, state, rect, label_font)


def altitude_to_y(altitude_ft, current_altitude_ft, center_y, pixels_per_foot):
    return center_y - (altitude_ft - current_altitude_ft) * pixels_per_foot


def draw_current_altitude_box(screen, state, rect, font):
    box_width = 112
    box_height = 42

    box_rect = pygame.Rect(
        rect.left + 10,
        rect.centery - box_height // 2,
        box_width,
        box_height,
    )

    pygame.draw.rect(screen, BLACK, box_rect)
    pygame.draw.rect(screen, WHITE, box_rect, 2)

    altitude_text = f"{state.altitude_ft:05.0f}"
    draw_centered_text(
        screen,
        font,
        altitude_text,
        WHITE,
        box_rect.center,
    )

    pointer = [
        (rect.left, rect.centery),
        (rect.left - 18, rect.centery - 12),
        (rect.left - 18, rect.centery + 12),
    ]
    pygame.draw.polygon(screen, WHITE, pointer)


def draw_target_altitude_bug(screen, state, rect, pixels_per_foot):
    y = altitude_to_y(
        state.target_altitude_ft,
        state.altitude_ft,
        rect.centery,
        pixels_per_foot,
    )

    if y < rect.top or y > rect.bottom:
        return

    points = [
        (rect.left + 6, y),
        (rect.left + 24, y - 10),
        (rect.left + 24, y + 10),
    ]

    pygame.draw.polygon(screen, MAGENTA, points)


def draw_vertical_speed(screen, state, rect, font):
    vs_text = f"VS {state.vertical_speed_fpm:+.0f}"
    vs_surface = font.render(vs_text, True, CYAN)

    screen.blit(
        vs_surface,
        (rect.left + 8, rect.bottom + 8),
    )