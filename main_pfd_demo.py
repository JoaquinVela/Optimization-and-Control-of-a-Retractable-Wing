import time 
import pygame

from display.display_state import create_demo_state
from display.artificial_horizon import draw_artificial_horizon
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

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()