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
        self.padding = 8

        self.themes = {
            "dark": {"background": (0, 0, 0), "text": (255, 255, 255)},
            "light": {"background": (255, 255, 255), "text": (0, 0, 0)},
        }
        self.theme_color = self.themes[theme]

    def surface_set(self, bg_surface, text, position):
        height = 0
        width = 0

        wrapped_text_surface = pygame.surface.Surface((250, 500), pygame.SRCALPHA)
        wrapped_text_surface.fill((0, 0, 0, 0))
        wrapped_text = textwrap.wrap(text, width=32)

        if wrapped_text:
            for line in wrapped_text:
                text_surface = self.font.render(line, True, self.theme_color["text"])
                wrapped_text_surface.blit(text_surface, (position))
                position = (position[0], position[1] + self.line_height)

                width = max(width, pygame.surface.Surface.get_width(text_surface))
                height += self.line_height

        bg_surface = pygame.surface.Surface(
            (
                width + (self.padding * 2),
                height + (self.padding * 2),
            )
        )
        bg_surface.fill(self.theme_color["background"])
        bg_surface.blit(wrapped_text_surface, (0, 0))

        return bg_surface

    def blit(self, text, bubble_position):
        surface = self.surface_set(self.bg_surface, text, (10, 10))
        self.game.ui_layer.place_surface(surface, (bubble_position))
