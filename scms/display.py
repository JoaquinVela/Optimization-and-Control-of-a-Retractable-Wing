import pygame

from scms.widgets.boom_panel import draw_boom_panel
from scms.widgets.constraint_health import draw_constraint_health
from scms.widgets.envelope_plot import draw_envelope_plot
from scms.widgets.future_prediction import draw_future_prediction
from scms.widgets.optimization_advisor import draw_optimization_advisor
from scms.widgets.top_bar import draw_top_bar_values
from scms.widgets.wing_indicator import draw_wing_configuration


class SCMSDisplay:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        self.font_large = pygame.font.SysFont("Arial", 32, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 18, bold=True)

    def draw(self, state):
        self.screen.fill((5, 8, 12))
        self.draw_layout(state)

    def draw_layout(self, state):
        w, h = self.width, self.height

        top_bar_rect = pygame.Rect(0, 0, w, 56)
        envelope_rect = pygame.Rect(20, 76, 745, 380)
        boom_rect = pygame.Rect(785, 76, 230, 270)
        wing_rect = pygame.Rect(1030, 76, 230, 270)
        advisor_rect = pygame.Rect(20, 476, 745, 130)
        constraint_rect = pygame.Rect(20, 626, 745, 154)
        future_rect = pygame.Rect(785, 366, 475, 414)

        self.draw_panel(top_bar_rect, "SCMS")
        self.draw_panel(envelope_rect, "SUPERSONIC ENVELOPE")
        self.draw_panel(boom_rect, "BOOMLESS CORRIDOR")
        self.draw_panel(wing_rect, "WING CONFIGURATION")
        self.draw_panel(advisor_rect, "SPEED OPTIMIZATION ADVISOR")
        self.draw_panel(constraint_rect, "CONSTRAINT HEALTH")
        self.draw_panel(future_rect, "PREDICTED STATE")

        draw_top_bar_values(self.screen, top_bar_rect, state, self.font_medium)
        draw_boom_panel(self.screen, boom_rect, state, self.font_small)
        draw_constraint_health(self.screen, constraint_rect, state, self.font_small)
        draw_optimization_advisor(self.screen, advisor_rect, state, self.font_small)
        draw_future_prediction(
            self.screen,
            future_rect,
            state,
            self.font_medium,
            self.font_small,
        )
        draw_wing_configuration(self.screen, wing_rect, state, self.font_small)
        draw_envelope_plot(self.screen, envelope_rect, state, self.font_small)

    def draw_panel(self, rect, title):
        pygame.draw.rect(self.screen, (14, 18, 24), rect)
        pygame.draw.rect(self.screen, (245, 245, 245), rect, 2)

        title_surface = self.font_small.render(title, True, (0, 220, 255))
        self.screen.blit(title_surface, (rect.x + 12, rect.y + 10))
