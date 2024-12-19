import logging
import random

import pygame

from shadowkeep.config import IMG_DIR, TILE_HEIGHT, TILE_WIDTH
from shadowkeep.lib.coordinates import Coordinates

logger = logging.getLogger("shadowkeep")


class Entities(list):
    @property
    def solid(self):
        return Entities([entity for entity in self if entity.solid])

    @property
    def non_solid(self):
        return Entities([entity for entity in self if entity.non_solid])

    def on_position(self, position):
        return Entities([entity for entity in self if entity.position == position])

    def of_type(self, *args):
        return Entities(
            [
                entity
                for entity in self
                if any([isinstance(entity, cls) for cls in args])
            ]
        )


class Entity:
    def __init__(
        self,
        game,
        position=None,
        velocity=Coordinates(0, 0),
        rotation=0,
        solid=True,
        movable=False,
    ):
        self.game = game
        self.solid = solid
        self.movable = movable

        self.rotation = rotation
        self.surface = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.surface = pygame.image.load(IMG_DIR / self.get_image())
        self.velocity = velocity
        self.position = position

        self.surface = pygame.transform.rotate(self.surface, self.rotation)
        self.dead = False
        self.dead_time = 0

        self.initial_position = self.position

    def try_move(self, dir=Coordinates(0, 0)):
        print("moving " + self)
        if self.game.map.is_floor(
            self.position + dir
        ) and not self.game.entities.on_position(self.position + dir):
            self.position += dir
            return True
        else:
            return False

    @property
    def non_solid(self):
        return not self.solid

    def toggle_state(self):
        self.solid = not (self.solid)

    def get_image(self):
        raise NotImplementedError

    def choose_random_position(self):
        while True:
            position = Coordinates(random.randint(5, 24), random.randint(5, 24))
            if self.game.map.is_floor(position):
                self.position = position
                return

    def blit(self):
        if self.dead:
            pass
        else:
            self.game.dynamic_layer.place_surface(
                self.surface, self.position.transformed_pair()
            )

    def destroy(self):
        self.game.entities.remove(self)


    def hit(self):
        self.dead = True
        self.position = self.initial_position
        if self.solid:
            self.solid = False


class End(Entity):
    def turn(self):
        if self.position == self.game.player.next_position:
            self._meet_player()

    def _meet_player(self):
        self.destroy()
        self.game.player.ghost_step()
        self.game.running = False

    def get_image(self):
        return "Goal.png"

