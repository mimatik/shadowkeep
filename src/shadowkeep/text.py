import pygame
import textwrap


class TextInput:
    def __init__(self, game, theme="light"):
        self.game = game
        self.text = ""

        self.bg_surface = pygame.surface.Surface((0, 0))

        self.font_size = 20
        self.line_height = round(self.font_size * 0.9)
        self.font = pygame.font.Font(None, self.font_size)

        self.themes = {
            "dark": {"background": (0, 0, 0), "text": (255, 255, 255)},
            "light": {"background": (255, 255, 255), "text": (0, 0, 0)},
        }
        self.theme_color = self.themes[theme]

    def make_bgSurface(self, text):
        wrapped_text = textwrap.wrap(text, width=32)
        rows = 0
        symbols = 0
        most_symbols = 0
        for row in wrapped_text:
            rows += 1
            for symbol in row:
                symbols += 1
                if symbols > most_symbols:
                    most_symbols = symbols
            symbols = 0
        surface = pygame.surface.Surface((most_symbols * 9, rows * 20 + 3))
        return surface

    def surface_set(self, bg_surface, text, position):
        wrapped_text = textwrap.wrap(text, width=32)

        for line in wrapped_text:
            text_surface = self.font.render(line, True, self.theme_color["text"])
            self.bg_surface.blit(text_surface, (position))
            position = (position[0], position[1] + self.line_height)

        height = pygame.surface.Surface.get_height(text_surface)
        width = pygame.surface.Surface.get_width(text_surface)

        bg_surface = pygame.surface.Surface(
            (
                width + 3,
                height + 3,
            )
        )
        bg_surface.fill(self.theme_color["background"])
s
        return bg_surface

    def blit(self, text, bubble_position):
        surface = self.make_bgSurface(text)
        surface = self.surface_set(self.bg_surface, text, (10, 10))
        self.game.ui_layer.place_surface(surface, (bubble_position))
