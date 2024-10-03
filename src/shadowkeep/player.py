import pygame
import time
from shadowkeep.config import TILE_HEIGHT, TILE_WIDTH
from shadowkeep.grid import coords_transform_pair, coords_transform_single

PLAYER_HEIGHT = TILE_HEIGHT
PLAYER_WIDTH = TILE_WIDTH


class Player:
    def __init__(self, game):
        self.x = 10
        self.y = 10
        self.game = game
        self.surface = pygame.surface.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.surface.fill((255, 250, 250))
        self.last_pressed = 0

    def move(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pressed < 40:
            return
        self.last_pressed = current_time
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            if self.game.map.data[self.y - 1][self.x] == 0:
                self.y -= 1
        if pressed_keys[pygame.K_s]:
            if self.game.map.data[self.y + 1][self.x] == 0:
                self.y += 1
        if pressed_keys[pygame.K_d]:
            if self.game.map.data[self.y][self.x + 1] == 0:
                self.x += 1
        if pressed_keys[pygame.K_a]:
            if self.game.map.data[self.y][self.x - 1] == 0:
                self.x -= 1

    def blit(self):
        self.game.window.blit(self.surface, coords_transform_pair(self.x, self.y))
