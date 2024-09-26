import pygame
from config import TILE_HEIGHT, TILE_WIDTH

PLAYER_HEIGHT = TILE_HEIGHT
PLAYER_WIDTH = TILE_WIDTH

class Player():
    def __init__(self, window, map):
        self.x = TILE_HEIGHT * 3
        self.y = TILE_WIDTH * 3
        self.window = window
        self.surface = pygame.surface.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.surface.fill((255, 250, 250))
        self.map = map

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            self.y -= TILE_HEIGHT
        if pressed_keys[pygame.K_s]:
            self.y += TILE_HEIGHT
        if pressed_keys[pygame.K_d]:
            self.x += TILE_WIDTH
        if pressed_keys[pygame.K_a]:
            self.x -= TILE_WIDTH
    def blit(self):
        self.window.blit(self.surface, (self.x, self.y))

