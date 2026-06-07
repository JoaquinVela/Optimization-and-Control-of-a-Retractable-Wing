import pygame 
from scms.state import create_initial_state
from scms.simulation_stub import update_state
from scms.display import SCMSDisplay

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 800))
    pygame.display.set_caption("SCMS")

    clock = pygame.time.Clock()
    display = SCMSDisplay(screen)
    state = create_initial_state()

    running = True
    while running:
        dt = clock.tick(30) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        
        update_state(state, dt)
        display.draw(state)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()