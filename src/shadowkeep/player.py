import pygame
from shadowkeep.config import TILE_HEIGHT, TILE_WIDTH
from shadowkeep.grid import coords_transform_pair, coords_transform_single

PLAYER_HEIGHT = TILE_HEIGHT
PLAYER_WIDTH = TILE_WIDTH
class Player:
    def __init__(self, window, map):
        self.x = 10
        self.y = 10
        self.window = window
        self.surface = pygame.surface.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.surface.fill((255, 250, 250))
        self.data = map.data
        self.clock = pygame.time.Clock()

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            if self.data[self.y - 1][self.x] == 0:
                self.y -= 1
        elif pressed_keys[pygame.K_s]:
            if self.data[self.y + 1][self.x] == 0:
                self.y += 1
        elif pressed_keys[pygame.K_d]:
            if self.data[self.y][self.x + 1] == 0:
                self.x += 1
        elif pressed_keys[pygame.K_a]:
            if self.data[self.y][self.x - 1] == 0:
                self.x -= 1

    def blit(self):
        self.window.blit(self.surface, coords_transform_pair(self.x, self.y))
