import pygame
from pygame._sdl2.video import Renderer, Texture, Window
from scms.fonts import load_font

class ManualControlsWindow:
    def __init__(self):
        self.window = None
        self.renderer = None
        self.font_large = None
        self.font_medium = None
        self.font_small = None

    def show(self):
        if self.window is not None:
            return

        self.window = Window(
            "Manual Controls",
            size=(520, 550),
            position=(80, 80),
        )
        self.renderer = Renderer(self.window)

        self.font_large = load_font(30, bold=True)
        self.font_medium = load_font(22, bold=True)
        self.font_small = load_font(18, bold=True)

    def hide(self):
        if self.window is None:
            return

        self.window.destroy()
        self.window = None
        self.renderer = None

    def draw(self, state):
        if self.window is None or self.renderer is None:
            return

        self.renderer.draw_color = (0, 0, 0, 255)
        self.renderer.clear()

        self._draw_text("MANUAL PILOT CONTROL", self.font_large, (255, 255, 255), 32, 30)
        self._draw_text("Auto Optimization OFF", self.font_medium, (240, 205, 40), 32, 74)

        controls = [
            ("A", "Toggle Auto Optimization"),
            ("W", "Increase target altitude +500 ft"),
            ("S", "Decrease target altitude -500 ft"),
            ("E", "Increase wing deployment +2%"),
            ("D", "Decrease wing deployment -2%"),
            ("R", "Increase thrust +5%"),
            ("F", "Decrease thrust -5%"),
            ("ESC", "Quit SCMS"),
        ]

        y = 125
        for key, description in controls:
            self._draw_text(key, self.font_medium, (0, 220, 255), 48, y)
            self._draw_text(description, self.font_medium, (255, 255, 255), 145, y)
            y += 38

        values = [
            f"TARGET ALTITUDE: {state['manual_target_altitude_ft']:,.0f} ft",
            f"DEPLOYMENT: {state['manual_deployment'] * 100:.0f}%",
            f"THRUST: {state['manual_thrust_percent']:.0f}%",
        ]

        y += 18
        for value in values:
            self._draw_text(value, self.font_small, (180, 185, 195), 48, y)
            y += 28

        self.renderer.present()

    def _draw_text(self, text, font, color, x, y):
        surface = font.render(text, True, color)
        texture = Texture.from_surface(self.renderer, surface)
        texture.draw(dstrect=(x, y, surface.get_width(), surface.get_height()))