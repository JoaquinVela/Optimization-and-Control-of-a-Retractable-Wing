import pygame
from display.colors import BLACK, WHITE, GRAY, GREEN, YELLOW, RED, CYAN
from display.geometry import clamp, draw_centered_text

def draw_speed_tape(screen, state, rect):
    pygame.draw.rect(screen, BLACK, rect)
    pygame.draw.rect(screen, WHITE, rect, 2)

    font = pygame.font.SysFont("Arial", 20, bold=True)
    small_font = pygame.font.SysFont("Arial", 16, bold=True)
    label_font = pygame.font.SysFont("Arial", 14, bold=True)

    center_y = rect.centery
    pixels_per_knot = 3.0
    visible_range_kt = rect.height / pixels_per_knot

    min_speed = state.airspeed_kt - visible_range_kt / 2
    max_speed = state.airspeed_kt + visible_range_kt / 2

    draw_speed_band(
        screen,
        rect,
        state.green_speed_min_kt,
        state.green_speed_max_kt,
        state.airspeed_kt,
        pixels_per_knot,
        GREEN,
    )
    draw_speed_band(
        screen,
        rect,
        state.yellow_speed_min_kt,
        state.yellow_speed_max_kt,
        state.airspeed_kt,
        pixels_per_knot,
        YELLOW,
    )
    draw_speed_band(
        screen,
        rect,
        state.red_speed_min_kt,
        state.red_speed_max_kt,
        state.airspeed_kt,
        pixels_per_knot,
        RED,
    )

    start_tick = int(min_speed // 10 * 10)
    end_tick = int(max_speed // 10 * 10 + 10)

    for speed in range(start_tick, end_tick + 1, 10):
        y = speed_to_y(speed, state.airspeed_kt, center_y, pixels_per_knot)

        if y < rect.top or y > rect.bottom:
            continue

        tick_width = 38 if speed % 20 == 0 else 22

        pygame.draw.line(
            screen,
            WHITE,
            (rect.right - tick_width, y),
            (rect.right - 4, y),
            2,
        )

        if speed % 20 == 0:
            label = small_font.render(str(speed), True, WHITE)
            screen.blit(label, (rect.left + 8, y - label.get_height() // 2))

    draw_optimal_speed_bug(
        screen,
        state,
        rect,
        pixels_per_knot,
        CYAN,
    )

    draw_current_speed_box(screen, state, rect, font)

    mach_text = f"M {state.mach:.2f}"
    mach_surface = label_font.render(mach_text, True, WHITE)
    screen.blit(
        mach_surface,
        (rect.left + 10, rect.bottom + 8)
    )

def speed_to_y(speed_kt, current_speed_kt, center_y, pixels_per_knot):
    return center_y - (speed_kt - current_speed_kt) * pixels_per_knot

def draw_speed_band(screen, rect, min_speed, max_speed, current_speed, pixels_per_knot, color):
    y_top = speed_to_y(max_speed, current_speed, rect.centery, pixels_per_knot)
    y_bottom = speed_to_y(min_speed, current_speed, rect.centery, pixels_per_knot)

    y_top = clamp(y_top, rect.top, rect.bottom)
    y_bottom = clamp(y_bottom, rect.top, rect.bottom)

    if y_bottom <= rect.top or y_top >= rect.bottom:
        return 

    band_rect = pygame.Rect(
        rect.right - 14,
        y_top,
        10,
        max(2, y_bottom - y_top)
    )
    pygame.draw.rect(screen, color, band_rect)

def draw_current_speed_box(screen, state, rect, font):
    box_width = 92
    box_height = 42

    box_rect = pygame.Rect(
        rect.right - box_width - 10,
        rect.centery - box_height // 2,
        box_width,
        box_height,
    )
    
    pygame.draw.rect(screen, BLACK, box_rect)
    pygame.draw.rect(screen, WHITE, box_rect, 2)

    speed_text = f"{state.airspeed_kt:03.0f}"
    draw_centered_text(
        screen,
        font,
        speed_text,
        WHITE,
        box_rect.center,
    )

    pointer = [
        (rect.right, rect.centery),
        (rect.right + 18, rect.centery - 12),
        (rect.right + 18, rect.centery + 12),
    ]
    pygame.draw.polygon(screen, WHITE, pointer)

def draw_optimal_speed_bug(screen, state, rect, pixels_per_knot, color):
    y = speed_to_y(
        state.optimal_boomless_speed_kt,
        state.airspeed_kt,
        rect.centery,
        pixels_per_knot,
    )

    if y < rect.top or y > rect.bottom:
        return
    
    points = [
        (rect.right - 24, y),
        (rect.right - 6, y - 10),
        (rect.right - 6, y + 10),
    ]
    pygame.draw.polygon(screen, color, points)
    