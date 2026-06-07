import pygame 
from scms.state import create_initial_state
from scms.simulation import Simulation
from scms.simulation_adapter import apply_simulation_sample
from scms.display import SCMSDisplay

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 800))
    pygame.display.set_caption("SCMS")

    clock = pygame.time.Clock()
    display = SCMSDisplay(screen)
    display_state = create_initial_state()
    simulation = Simulation()

    running = True
    while running:
        dt = clock.tick(30) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if display.get_auto_optimization_rect().collidepoint(event.pos):
                    simulation.toggle_auto_optimization()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    simulation.toggle_auto_optimization()

                if not simulation.auto_optimization_enabled:
                    if event.key == pygame.K_w:
                        simulation.adjust_manual_altitude_ft(500)
                    elif event.key == pygame.K_s:
                        simulation.adjust_manual_altitude_ft(-500)
                    elif event.key == pygame.K_e:
                        simulation.adjust_manual_deployment(0.02)
                    elif event.key == pygame.K_d:
                        simulation.adjust_manual_deployment(-0.02)
                    elif event.key == pygame.K_r:
                        simulation.adjust_manual_thrust_percent(5)
                    elif event.key == pygame.K_f:
                        simulation.adjust_manual_thrust_percent(-5)

        sample = simulation.step(dt)
        apply_simulation_sample(display_state, sample, dt)

        display.draw(display_state)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()