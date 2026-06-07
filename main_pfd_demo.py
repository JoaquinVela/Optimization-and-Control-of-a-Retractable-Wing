import time 
import pygame

from display.display_state import create_demo_state
from display.artificial_horizon import draw_artificial_horizon
from display.speed_tape import draw_speed_tape
from display.altitude_tape import draw_altitude_tape
from display.heading_tape import draw_heading_tape
from display.wing_retraction_wheel import draw_wing_retraction_wheel
from display.colors import BLACK

def main():
    pygame.init()

    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("PFD Demo")

    clock = pygame.time.Clock()
    start_time = time.time()

    running = True

    while running:
        now = time.time() - start_time
        state = create_demo_state(now)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.fill(BLACK)

        horizon_rect = pygame.Rect(320, 80, 640, 460)
        draw_artificial_horizon(screen, state, horizon_rect)

        speed_rect = pygame.Rect(80, 80, 180, 460)
        draw_speed_tape(screen, state, speed_rect)

        altitude_rect = pygame.Rect(1020, 80, 180, 460)
        draw_altitude_tape(screen, state, altitude_rect)

        heading_rect = pygame.Rect(320, 610, 640, 90)
        draw_heading_tape(screen, state, heading_rect)

        wing_rect = pygame.Rect(1000, 580, 220, 180)
        draw_wing_retraction_wheel(screen, state, wing_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()