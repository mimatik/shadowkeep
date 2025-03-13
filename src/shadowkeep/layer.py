import pygame
from pygame import Surface


class Layer:
    def __init__(self, game):
        self.game = game
        self.surface = pygame.surface.Surface(
            (game.window.get_width(), game.window.get_height()),
            pygame.SRCALPHA,
        )
        self.target = game.window

    def clear(self):
        self.surface.fill((0, 0, 0, 0))

    def place_surface(self, surface, position):
        self.surface.blit(surface, position)

    def blit(self, position=(0, 0)):
        self.target.blit(self.surface, position)
