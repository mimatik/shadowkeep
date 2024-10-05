import pygame
from shadowkeep.config import TILE_WIDTH, TILE_HEIGHT
from shadowkeep.grid import coords_transform_pair, coords_transform_single


class Monster:
    def __init__(self, game):
        self.game = game
        self.x = 10
        self.y = 10
        self.surface = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.surface.fill((255, 0, 0))

    def blit(self, layer):
        layer.blit(self.surface, coords_transform_pair(self.x, self.y))

    def turn(self):
        self.x += 1
