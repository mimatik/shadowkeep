import logging
import random

import pygame

from shadowkeep.config import (
    IMG_DIR,
    TILE_HEIGHT,
    TILE_WIDTH,
)
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

    def not_of_type(self, *args):
        return Entities(
            [
                entity
                for entity in self
                if not any([isinstance(entity, cls) for cls in args])
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
        self.initial_solid = solid
        self.movable = movable

        self.rotation = rotation
        self.surface = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.surface = pygame.image.load(IMG_DIR / self.get_image())
        self.velocity = velocity
        self.position = position
        if self.position is None:
            self.choose_random_position()
        self.initial_position = self.position

        self.surface = pygame.transform.rotate(self.surface, self.rotation)
        self.dead = False
        self.dead_time = 0

    respawn_time = None

    def interact(self, dir):
        pass

    def turn(self):
        self._check_respawn()

    def _check_respawn(self):
        if self.dead and self.respawn_time is not None:
            self.dead_time += 1
            if self.dead_time == self.respawn_time:
                self.dead_time = 0
                self.dead = False
                self.solid = self.initial_solid

    @property
    def non_solid(self):
        return not self.solid

    def toggle_state(self):
        self.solid = not (self.solid)

    def get_image(self):
        raise NotImplementedError

    def choose_random_position(self):
        while True:
            position = Coordinates(
                random.randint(0, self.game.width), random.randint(0, self.game.height)
            )
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

    def interact(self, dir):
        pass

    def destroy(self):
        self.game.entities.remove(self)

    def hit(self):
        self.dead = True
        self.position = self.initial_position
        if self.solid:
            self.solid = False

    def respawn(self):
        pass


class Pickeable(Entity):
    def move_to_inventory(self):
        self.game.inventory += [self]
        self.position = Coordinates(20 + self.game.inventory.index(self), 23)
        self.destroy()


class End(Entity):
    def interact(self, *args, **kwargs):
        self.destroy()
        self.game.player.ghost_step()
        self.game.running = False

    def get_image(self):
        return "Goal.png"
