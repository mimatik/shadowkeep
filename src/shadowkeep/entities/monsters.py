import logging
import random

from shadowkeep.entities.fireballs import Fireball
from shadowkeep.lib.coordinates import Coordinates

from .base import Entity

logger = logging.getLogger("shadowkeep")


class Monster(Entity):
    respawn_time = 15

    def __init__(self, game):
        super().__init__(game)
        self.choose_random_position()
        self.choose_random_velocity()

    def turn(self):
        super().turn()
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
        if self.dead:
            pass
        else:
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
                    for firebal in self.game.entities.of_type(Fireball)
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

    def respawn(self):
        self.dead = False
        self.dead_time = 0
        self.solid = self.initial_solid
        self.position = self.initial_position


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
