import pygame
import time
from shadowkeep.config import TILE_HEIGHT, TILE_WIDTH
from shadowkeep.grid import coords_transform_pair, coords_transform_single
from shadowkeep.lib.coordinates import Coordinates


class Player:
    def __init__(self, game):
        self.x = 10
        self.y = 10
        self.game = game
        self.layer = game.dynamic_layer
        self.surface = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.surface.fill((255, 250, 250))
        self.last_pressed = 0
        self.position = Coordinates(self.x, self.y)

    def move(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pressed < 40:
            return
        self.last_pressed = current_time
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            if self.game.map.data[self.position.y - 1][self.position.x] == 0:
                self.position.y -= 1
        if pressed_keys[pygame.K_s]:
            if self.game.map.data[self.position.y + 1][self.position.x] == 0:
                self.position.y += 1
        if pressed_keys[pygame.K_d]:
            if self.game.map.data[self.position.y][self.position.x + 1] == 0:
                self.position.x += 1
        if pressed_keys[pygame.K_a]:
            if self.game.map.data[self.position.y][self.position.x - 1] == 0:
                self.position.x -= 1
        self.game.turn()

    def blit(self):
        self.layer.place_surface(
            self.surface, coords_transform_pair(self.position.x, self.position.y)
        )
