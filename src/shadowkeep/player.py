import pygame
from shadowkeep.config import TILE_HEIGHT, TILE_WIDTH
from shadowkeep.lib.coordinates import Coordinates


class Player:
    def __init__(self, game):
        self.x = 10
        self.y = 10
        self.game = game
        self.surface = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.surface.fill((255, 250, 250))
        self.last_pressed = 0
        self.position = Coordinates(self.x, self.y)

    def move(self):
        current_time = pygame.time.get_ticks()
        movement = Coordinates()

        if current_time - self.last_pressed < 40:
            return

        self.last_pressed = current_time

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_w]:
            movement = Coordinates(y=-1)

        if pressed_keys[pygame.K_s]:
            movement = Coordinates(y=+1)

        if pressed_keys[pygame.K_d]:
            movement = Coordinates(x=+1)

        if pressed_keys[pygame.K_a]:
            movement = Coordinates(x=-1)

        next_movement = self.position + movement

        if self.game.map.is_floor(next_movement):
            self.position = next_movement

        self.game.turn()

    def blit(self):
        self.game.dynamic_layer.place_surface(
            self.surface, self.position.transformed_pair()
        )
