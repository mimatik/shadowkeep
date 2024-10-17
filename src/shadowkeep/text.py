import pygame
import textwrap


class TextInput:
    def __init__(self, game, theme="light"):
        self.game = game
        self.text = ""

        self.font_size = 20
        self.line_height = round(self.font_size * 0.9)
        self.font = pygame.font.Font(None, self.font_size)
        self.padding = round(self.font_size * 0.5)

        self.themes = {
            "dark": {"background": (0, 0, 0), "text": (255, 255, 255)},
            "light": {"background": (255, 255, 255), "text": (0, 0, 0)},
        }
        self.theme_color = self.themes[theme]

    def surface_set(self, text):
        height = 0
        width = 0
        position = (self.padding, self.padding)

        wrapped_text_surface = pygame.surface.Surface((500, 500), pygame.SRCALPHA)
        wrapped_text_surface.fill((0, 0, 0, 0))
        wrapped_text = textwrap.wrap(text, width=32)

        if wrapped_text:
            for line in wrapped_text:
                text_surface = self.font.render(line, True, self.theme_color["text"])
                wrapped_text_surface.blit(text_surface, (position))
                position = (position[0], position[1] + self.line_height)

                width = max(width, pygame.surface.Surface.get_width(text_surface))
                height += self.line_height

            self.surface_width = width + (self.padding * 2)
            self.surface_height = height + (self.padding * 2) - 4

            bg_surface = pygame.surface.Surface(
                (
                    self.surface_width,
                    self.surface_height,
                )
            )
            bg_surface.fill(self.theme_color["background"])
            bg_surface.blit(wrapped_text_surface, (0, 0))

        else:
            bg_surface = self.blink()

        return bg_surface

    def blink(self):
        size = (self.padding * 2, self.line_height + self.padding * 2 - 4)
        blink_surface = pygame.Surface(size, pygame.SRCALPHA)
        blink_surface.fill(self.theme_color["background"])

        alpha = int(abs(pygame.time.get_ticks() / 500 % 2 - 1) * 255)
        blink_surface.set_alpha(alpha)

        return blink_surface

    def blit(self, text, bubble_position):
        surface = self.surface_set(text)
        self.game.ui_layer.place_surface(surface, (bubble_position))
