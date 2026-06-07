import math
import pygame

from display.colors import BLACK, WHITE, GRAY, GREEN, YELLOW, CYAN
from display.geometry import clamp, deg_to_rad, draw_centered_text


def draw_wing_retraction_wheel(screen, state, rect):
    pygame.draw.rect(screen, BLACK, rect)
    pygame.draw.rect(screen, WHITE, rect, 2)

    font = pygame.font.SysFont("Arial", 24, bold=True)
    small_font = pygame.font.SysFont("Arial", 15, bold=True)
    tiny_font = pygame.font.SysFont("Arial", 13, bold=True)

    center = rect.center
    radius = min(rect.width, rect.height) // 2 - 28

    percent = clamp(state.wing_retraction_percent, 0.0, 100.0)

    draw_scale(screen, center, radius, small_font)
    draw_retraction_arc(screen, center, radius, percent)
    draw_needle(screen, center, radius, percent)

    pygame.draw.circle(screen, WHITE, center, radius, 2)
    pygame.draw.circle(screen, CYAN, center, 5)

    draw_centered_text(
        screen,
        tiny_font,
        f"DEP {state.deployment:.2f}",
        GRAY,
        (center[0], center[1] + 24),
    )

    draw_centered_text(
        screen,
        small_font,
        "WING RETRACT",
        WHITE,
        (center[0], rect.bottom - 18),
    )


def percent_to_angle(percent):
    return 180.0 - percent * 1.8


def point_on_circle(center, radius, angle_deg):
    angle_rad = deg_to_rad(angle_deg)
    x = center[0] + radius * math.cos(angle_rad)
    y = center[1] - radius * math.sin(angle_rad)
    return int(x), int(y)


def draw_scale(screen, center, radius, font):
    for percent in range(0, 101, 10):
        angle = percent_to_angle(percent)

        outer = point_on_circle(center, radius, angle)
        inner_radius = radius - 14 if percent % 20 == 0 else radius - 8
        inner = point_on_circle(center, inner_radius, angle)

        pygame.draw.line(screen, WHITE, inner, outer, 2)

        if percent % 20 == 0:
            label_radius = radius - 32
            label_pos = point_on_circle(center, label_radius, angle)
            text = font.render(str(percent), True, WHITE)
            screen.blit(
                text,
                (
                    label_pos[0] - text.get_width() // 2,
                    label_pos[1] - text.get_height() // 2,
                ),
            )


def draw_retraction_arc(screen, center, radius, percent):
    arc_radius = radius - 18

    previous_point = point_on_circle(center, arc_radius, percent_to_angle(0))

    for value in range(1, int(percent) + 1):
        current_point = point_on_circle(center, arc_radius, percent_to_angle(value))

        color = GREEN
        if value >= 70:
            color = YELLOW

        pygame.draw.line(screen, color, previous_point, current_point, 5)
        previous_point = current_point


def draw_needle(screen, center, radius, percent):
    angle = percent_to_angle(percent)
    end = point_on_circle(center, radius - 42, angle)

    pygame.draw.line(screen, CYAN, center, end, 4)