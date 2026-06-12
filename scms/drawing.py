import pygame
from pygame import gfxdraw

def _int_point(point):
    return int(round(point[0])), int(round(point[1]))


def _int_points(points):
    return [_int_point(point) for point in points]


def aa_line(screen, color, start, end, width=1):
    start = _int_point(start)
    end = _int_point(end)

    if width <= 1:
        pygame.draw.aaline(screen, color, start, end)
        return

    pygame.draw.line(screen, color, start, end, width)
    pygame.draw.aaline(screen, color, start, end)


def aa_filled_circle(screen, color, center, radius):
    x, y = _int_point(center)
    radius = int(round(radius))

    circle_rect = pygame.Rect(
        x - radius,
        y - radius,
        radius * 2,
        radius * 2,
    )

    clip_rect = screen.get_clip()
    if not circle_rect.colliderect(clip_rect):
        return

    gfxdraw.filled_circle(screen, x, y, radius, color)
    gfxdraw.aacircle(screen, x, y, radius, color)


def aa_circle_outline(screen, color, center, radius, width=1):
    x, y = _int_point(center)
    radius = int(round(radius))

    circle_rect = pygame.Rect(
        x - radius,
        y - radius,
        radius * 2,
        radius * 2,
    )

    clip_rect = screen.get_clip()
    if not circle_rect.colliderect(clip_rect):
        return

    for offset in range(width):
        gfxdraw.aacircle(screen, x, y, radius - offset, color)


def aa_filled_polygon(screen, color, points):
    points = _int_points(points)

    gfxdraw.filled_polygon(screen, points, color)
    gfxdraw.aapolygon(screen, points, color)


def aa_polygon_outline(screen, color, points, width=1):
    points = _int_points(points)

    if width > 1:
        pygame.draw.lines(screen, color, True, points, width)

    pygame.draw.aalines(screen, color, True, points)