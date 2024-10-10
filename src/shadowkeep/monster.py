import random
import pygame
from shadowkeep.config import TILE_HEIGHT, TILE_WIDTH
from shadowkeep.grid import coords_transform_pair, coords_transform_single
from shadowkeep.lib.coordinates import Coordinates

from src.shadowkeep.lib.coordinates import Coordinates


class Monster:
    def __init__(self, game):
        self.game = game
        self.x = 15
        self.y = 15
        self.layer = game.dynamic_layer
        self.surface = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.surface.fill((255, 0, 0))
        self.velocity = random.randint(1, 2)
        self.position = Coordinates(self.x, self.y)

    def move(self):
        self.where = random.randint(1, 4)

        if self.where == 1:
            if (
                self.game.map.data[self.position.y - self.velocity][self.position.x]
                == 0
                and self.game.map.data[self.position.y - 1][self.position.x] == 0
            ):
                self.position.y -= self.velocity
            else:
                self.move()
        elif self.where == 2:
            if (
                self.game.map.data[self.position.y + self.velocity][self.position.x]
                == 0
                and self.game.map.data[self.position.y + 1][self.position.x] == 0
            ):
                self.position.y += self.velocity
            else:
                self.move()
        elif self.where == 3:
            if (
                self.game.map.data[self.position.y][self.position.x - self.velocity]
                == 0
                and self.game.map.data[self.position.y][self.position.x - 1] == 0
            ):
                self.position.x -= self.velocity
            else:
                self.move()
        elif self.where == 4:
            if (
                self.game.map.data[self.position.y][self.position.x + self.velocity]
                == 0
                and self.game.map.data[self.position.y][self.position.x + 1] == 0
            ):
                self.position.x += self.velocity
            else:
                self.move()
        else:
            return
        if self.position.is_neighbour(self.game.player.position):
            self.game.running = False

    def blit(self):
        self.layer.place_surface(
            self.surface, coords_transform_pair(self.position.x, self.position.y)
        )

    def turn(self):
        self.move()
