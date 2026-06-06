import pygame

from display.colors import BLACK, WHITE, CYAN
from display.geometry import draw_centered_text


def draw_heading_tape(screen, state, rect):
    pygame.draw.rect(screen, BLACK, rect)
    pygame.draw.rect(screen, WHITE, rect, 2)

    font = pygame.font.SysFont("Arial", 20, bold=True)
    small_font = pygame.font.SysFont("Arial", 15, bold=True)

    center_x = rect.centerx
    center_y = rect.centery
    pixels_per_degree = 8.0

    visible_degrees = rect.width / pixels_per_degree
    min_heading = state.heading_deg - visible_degrees / 2
    max_heading = state.heading_deg + visible_degrees / 2

    start_heading = int(min_heading // 10 * 10)
    end_heading = int(max_heading // 10 * 10 + 10)

    for heading in range(start_heading, end_heading + 1, 5):
        wrapped_heading = heading % 360
        x = heading_to_x(heading, state.heading_deg, center_x, pixels_per_degree)

        if x < rect.left or x > rect.right:
            continue

        tick_height = 28 if wrapped_heading % 10 == 0 else 16

        pygame.draw.line(
            screen,
            WHITE,
            (x, rect.top + 8),
            (x, rect.top + 8 + tick_height),
            2,
        )

        if wrapped_heading % 10 == 0:
            label = heading_label(wrapped_heading)
            text = small_font.render(label, True, WHITE)
            screen.blit(
                text,
                (x - text.get_width() // 2, rect.bottom - text.get_height() - 8),
            )

    draw_current_heading_box(screen, state, rect, font)
    draw_heading_pointer(screen, rect)


def heading_to_x(heading_deg, current_heading_deg, center_x, pixels_per_degree):
    return center_x + (heading_deg - current_heading_deg) * pixels_per_degree


def heading_label(heading_deg):
    if heading_deg == 0:
        return "N"
    if heading_deg == 90:
        return "E"
    if heading_deg == 180:
        return "S"
    if heading_deg == 270:
        return "W"

    return f"{heading_deg:03.0f}"


def draw_current_heading_box(screen, state, rect, font):
    box_width = 86
    box_height = 36

    box_rect = pygame.Rect(
        rect.centerx - box_width // 2,
        rect.top + 8,
        box_width,
        box_height,
    )

    pygame.draw.rect(screen, BLACK, box_rect)
    pygame.draw.rect(screen, WHITE, box_rect, 2)

    heading_text = heading_label(round(state.heading_deg / 1.0) % 360)

    draw_centered_text(
        screen,
        font,
        heading_text,
        WHITE,
        box_rect.center,
    )


def draw_heading_pointer(screen, rect):
    points = [
        (rect.centerx, rect.top),
        (rect.centerx - 10, rect.top + 14),
        (rect.centerx + 10, rect.top + 14),
    ]

    pygame.draw.polygon(screen, CYAN, points)