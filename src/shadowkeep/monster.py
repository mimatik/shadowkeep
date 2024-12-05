import logging
import random

import pygame

from shadowkeep.config import IMG_DIR, TILE_HEIGHT, TILE_WIDTH
from shadowkeep.lib.coordinates import Coordinates

logger = logging.getLogger("shadowkeep")


class Entity:
    def __init__(
        self, game, position=None, velocity=Coordinates(0, 0), rotation=0, solid=True
    ):
        self.game = game

        self.solid = solid

        self.rotation = rotation
        self.surface = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.surface = pygame.image.load(IMG_DIR / self.get_image())
        self.velocity = velocity
        self.position = position

        self.surface = pygame.transform.rotate(self.surface, self.rotation)

    @property
    def non_solid(self):
        return not self.solid

    def get_image(self):
        raise NotImplementedError

    def choose_random_position(self):
        while True:
            position = Coordinates(random.randint(5, 24), random.randint(5, 24))
            if self.game.map.is_floor(position):
                self.position = position
                return

    def blit(self):
        self.game.dynamic_layer.place_surface(
            self.surface, self.position.transformed_pair()
        )

    def destroy(self):
        self.game.entities.remove(self)

    def _meet_fireball(self):
        pass


class Logic(Entity):
    def send_update(self, directions=[], exclucions=[]):
        pass

    def recive_update(self):
        pass


class Monster(Entity):

    def __init__(self, game):
        super().__init__(game)
        self.choose_random_position()
        self.choose_random_velocity()

    def turn(self):
        if random.random() < 0.25:
            self.choose_random_velocity()
        self.move()

    def choose_random_velocity(self):
        self.velocity = random.choice(
            [Coordinates(x=-1), Coordinates(x=+1), Coordinates(y=-1), Coordinates(y=+1)]
        )

    def choose_initial_velocity(self):
        self.choose_random_velocity()

    def move(self):
        self.next_position = self.position + self.velocity

        if (
            self.game.map.is_floor(self.next_position)
            and not any(
                other_entity.position == self.next_position
                for other_entity in self.game.entities.solid
                if other_entity != self
            )
            and self.next_position != self.game.player.position
            and not any(
                firebal.next_position == self.next_position
                for firebal in self.game.firebals
            )
        ):
            self.position = self.next_position
        else:
            self.choose_random_velocity()

        if (
            self.position.is_neighbour(self.game.player.position)
            or self.position == self.game.player.position
        ):
            self._meet_player()


class TalkingMonster(Monster):

    def get_image(self):
        return "Friend.png"

    def _meet_player(self):
        self.game.dialog.start("Zeptej se na neco")


class BadMonster(Monster):
    def get_image(self):
        return "Enemy.png"

    def _meet_player(self):
        self.game.player.lives -= 1


class Fireball(Entity):

    def get_image(self):
        return "Fireball.png"

    def __init__(self, game, position, velocity, rotation):
        super().__init__(position, velocity, rotation)
        self.game = game
        self.position = position
        self.velocity = velocity
        self.rotation = rotation
        self.next_position = self.position

    def turn(self):
        for entity in self.game.entities.solid:
            if self.next_position == entity.position:
                entity.destroy()
                self.destroy()

        if self.next_position == self.game.player.position:
            self.game.player.lives -= 1
            self.destroy()

        elif not self.game.map.is_floor(self.next_position):
            self.destroy()

        if (
            self.next_position == self.game.player.last_position
            and self.position == self.game.player.position
        ):
            self.game.player.lives -= 1
            self.destroy()

        self.position = self.next_position
        self.next_position = self.position + self.velocity

    def destroy(self):
        self.game.firebals.remove(self)


class FireballLauncher(Entity):
    def __init__(self, game, rotation=0, position=Coordinates(0, 0)):
        super().__init__(game, rotation=rotation)
        self.position = position
        self.get_direction()

    def get_direction(self):
        if self.rotation == 0:
            self.direction = Coordinates(0, 1)
        elif self.rotation == 90:
            self.direction = Coordinates(1, 0)
        elif self.rotation == 180:
            self.direction = Coordinates(0, -1)
        elif self.rotation == 270:
            self.direction = Coordinates(-1, 0)
        else:
            return Coordinates(0, 0)

    def get_image(self):
        return "Fireball_launcher.png"

    def turn(self):
        if self.game.current_turn % 4 == 0:
            self.game.firebals += [
                Fireball(
                    self.game,
                    position=self.position + self.direction,
                    velocity=self.direction,
                    rotation=self.rotation,
                )
            ]
            for entity in self.game.entities.solid:
                for firebal in self.game.firebals:
                    if entity.position == firebal.position:
                        entity.destroy()
                        firebal.destroy()


class Rotator(Entity):
    pass


class Door(Entity):

    def turn(self):
        if self.position == self.game.player.next_position:
            self._meet_player()

    def _meet_player(self):
        if self.game.keys > 0:
            self.game.keys -= 1
            self.destroy()
            self.game.player.ghost_step()

    def get_image(self):
        return "Door.png"


class Key(Entity):
    def turn(self):
        if self.position == self.game.player.next_position:
            self._meet_player()

    def _meet_player(self):
        self.destroy()
        self.game.player.ghost_step()
        self.game.keys += 1
        logger.info("added key")

    def get_image(self):
        return "Key.png"


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


class Box(Entity):

    def get_image(self):
        return "Box.png"

    def turn(self):
        if self.position == self.game.player.next_position:
            self._meet_player()

    def _meet_player(self):
        if self.game.map.is_floor(
            self.position + self.game.player.moved_dir
        ) and not any(
            other_entity.position == self.game.player.moved_dir
            for other_entity in self.game.entities.solid
        ):

            self.position += self.game.player.moved_dir
            self.game.player.ghost_step()
