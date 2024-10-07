import pygame
from shadowkeep.config import TILE_WIDTH, TILE_HEIGHT
from shadowkeep.grid import coords_transform_pair, coords_transform_single
import random


class Monster:
    def __init__(self, game):
        self.game = game
        self.x = 12
        self.y = 7
        self.surface = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.surface.fill((255, 0, 0))
        self.velocity = random.randint(1,2)
        self.position = (self.x, self.y)

    def move(self):
        self.where = random.randint(1, 4)

        if self.where == 1:
            if self.game.map.data[self.y - self.velocity][self.x] == 0 and self.game.map.data[self.y - 1][self.x] == 0:
                self.y -= self.velocity
            else:
                self.move()
        elif self.where == 2:
            if self.game.map.data[self.y + self.velocity][self.x] == 0 and self.game.map.data[self.y + 1][self.x] == 0:
                self.y += self.velocity
            else:
                self.move()
        elif self.where == 3:
            if self.game.map.data[self.y][self.x - self.velocity] == 0 and self.game.map.data[self.y][self.x - 1] == 0:
                self.x -= self.velocity
            else:
                self.move()
        elif self.where == 4:
            if self.game.map.data[self.y][self.x + self.velocity] == 0 and self.game.map.data[self.y][self.x + 1] == 0:
                self.x += self.velocity
            else:
                self.move()
        else:
            return

    def turn(self):
        self.move()

    def blit(self):
        self.game.window.blit(self.surface, coords_transform_pair(self.x, self.y))