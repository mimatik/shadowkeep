import pygame
import textwrap


class TextInput:
    def __init__(self, game, theme="light"):
        self.game = game
        self.text = ""
        self.bg_surface = pygame.surface.Surface((250, 150))

        self.font_size = 20
        self.line_height = round(self.font_size * 0.9)
        self.font = pygame.font.Font(None, self.font_size)

        self.themes = {
            "dark": {"background": (0, 0, 0), "text": (255, 255, 255)},
            "light": {"background": (255, 255, 255), "text": (0, 0, 0)},
        }
        self.theme_color = self.themes[theme]

    def surface_set(self, bg_surface, text, position):
        self.bg_surface.fill(self.theme_color["background"])
        wrapped_text = textwrap.wrap(text, width=32)

        for line in wrapped_text:
            text_surface = self.font.render(line, True, self.theme_color["text"])
            bg_surface.blit(text_surface, (position))
            position = (position[0], position[1] + self.line_height)

        return bg_surface

    def blit(self, text, bubble_position):
        surface = self.surface_set(self.bg_surface, text, (10, 10))
        self.game.ui_layer.place_surface(surface, (bubble_position))
