import pygame


class Layer:
    def __init__(self, game):
        self.game = game
        self.surface = pygame.Surface(
            (game.window.get_width(), game.window.get_height()), pygame.SRCALPHA
        )

    def clear(self):
        self.surface.fill((0, 0, 0, 0))

    def blit(self, surface, position):
        self.surface.blit(surface, position)

    def draw(self, target_surface):
        target_surface.blit(self.surface, (0, 0))
