import pygame
from shadowkeep.config import TILE_HEIGHT, TILE_WIDTH

from shadowkeep.grid import coords_transform_pair, coords_transform_single

PLAYER_HEIGHT = TILE_HEIGHT
PLAYER_WIDTH = TILE_WIDTH


class Player:
    def __init__(self, window, map):
        self.x = 3
        self.y = 3
        self.window = window
        self.surface = pygame.surface.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.surface.fill((255, 250, 250))
        self.map = map

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            self.y -= 1
        if pressed_keys[pygame.K_s]:
            self.y += 1
        if pressed_keys[pygame.K_d]:
            self.x += 1
        if pressed_keys[pygame.K_a]:
            self.x -= 1

    def blit(self):
        self.window.blit(self.surface, coords_transform_pair(self.x, self.y))
