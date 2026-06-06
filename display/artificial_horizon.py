import pygame

from display.colors import BLACK, WHITE, SKY_BLUE, GROUND_BROWN, CYAN
from display.geometry import deg_to_rad

def draw_artificial_horizon(screen, state, rect):
    center_x = rect.centerx
    center_y = rect.centery

    horizon_surface = pygame.Surface((rect.width, rect.height))
    horizon_surface.fill(BLACK)

    pitch_pixels_per_degree = 7
    pitch_offset = state.pitch_deg * pitch_pixels_per_degree

    local_center_x = rect.width // 2
    local_center_y = rect.height // 2 + pitch_offset

    roll_rad = deg_to_rad(state.roll_deg)

    large_size = max(rect.width, rect.height) * 3
    sky_rect = pygame.Rect(
        -large_size // 2,
        -large_size,
        large_size, 
        large_size,
    )
    ground_rect = pygame.Rect(
        0,
        large_size // 2, 
        large_size,
        large_size // 2,
    )

    world_surface = pygame.Surface((large_size, large_size))
    world_surface.fill(SKY_BLUE)
    pygame.draw.rect(world_surface, GROUND_BROWN, ground_rect)

    horizon_y = large_size // 2
    pygame.draw.line(
        world_surface,
        WHITE,
        (0, horizon_y),
        (large_size, horizon_y),
        4,
    )

    for pitch in range(-30, 35, 10):
        if pitch == 0:
            continue

        y = horizon_y - pitch * pitch_pixels_per_degree
        mark_width = 80 if pitch % 20 == 0 else 45

        pygame.draw.line(
            world_surface,
            WHITE,
            (large_size // 2 - mark_width, y),
            (large_size // 2 + mark_width, y),
            2,
        )

        font = pygame.font.SysFont("Arial", 18, bold=True)
        label = str(abs(pitch))
        left_text = font.render(label, True, WHITE)
        right_text = font.render(label, True, WHITE)

        world_surface.blit(
            left_text, 
            (large_size // 2 - mark_width - 35, y - 10),
        )
        world_surface.blit(
            right_text,
            (large_size // 2 + mark_width + 15, y - 10),
        )

    rotated_world = pygame.transform.rotate(world_surface, state.roll_deg)

    source_rect = rotated_world.get_rect(
        center=(
            large_size // 2,
            large_size // 2 - pitch_offset,
        )
    )

    horizon_surface.blit(
        rotated_world,
        (
            local_center_x - source_rect.centerx,
            local_center_y - source_rect.centery,
        ),
    )

    screen.blit(horizon_surface, rect)

    pygame.draw.rect(screen, WHITE, rect, 2)

    draw_aircraft_reference(screen, center_x, center_y)
    draw_roll_pointer(screen, center_x, rect.top + 25)

def draw_aircraft_reference(screen, center_x, center_y):
    wing_width = 90
    wing_gap = 16

    pygame.draw.line(
        screen,
        CYAN,
        (center_x - wing_gap - wing_width, center_y),
        (center_x - wing_gap, center_y),
        5,
    )
    pygame.draw.line(
        screen,
        CYAN,
        (center_x + wing_gap, center_y),
        (center_x + wing_gap + wing_width, center_y),
        5,
    )
    pygame.draw.circle(screen, CYAN, (center_x, center_y), 6, 2)

def draw_roll_pointer(screen, center_x, top_y):
    points = [
        (center_x, top_y),
        (center_x - 10, top_y + 18),
        (center_x + 10, top_y + 18),
    ]
    pygame.draw.polygon(screen, WHITE, points)

