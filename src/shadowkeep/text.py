import pygame
import time


class TextInput:
    def __init__(self, game):
        self.game = game
        self.is_open = False
        self.text1 = "Jake je heslo"
        self.text2 = ""
        self.surface = pygame.surface.Surface((250, 150))
        self.font = pygame.font.Font(None, 18)
        self.maximum_letters = 250 / 18
        self.text_position = (10, 10)

    def surface_set(self, surface, text, font, position):
        self.surface.fill((255, 255, 255))
        text_surface = font.render(text, True, (0, 0, 0))
        surface.blit(text_surface, (position))
        return surface

    def blit(self):
        if self.is_open:
            self.surface1 = self.surface_set(
                self.surface, self.text1, self.font, (10, 10)
            )
            self.game.ui_layer.place_surface(self.surface1, (20, 200))
            self.surface2 = self.surface_set(
                self.surface, self.text2, self.font, (10, 10)
            )
            self.game.ui_layer.place_surface(self.surface2, (500, 200))

    def read_key(self, event):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RETURN]:
            self.is_open = False
            if self.text2 != "jablko":
                self.game.running = False
            self.text2 = ""
        elif pressed_keys[pygame.K_ESCAPE]:
            self.text2 = ""
        elif pressed_keys[pygame.K_BACKSPACE]:
            if self.text2:
                self.text2 = self.text2[:-1]
        else:
            self.text2 += event.unicode
