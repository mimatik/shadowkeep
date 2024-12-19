import logging

from shadowkeep.lib.coordinates import Coordinates
from .base import Entity

logger = logging.getLogger("shadowkeep")


class Fireball(Entity):

    def get_image(self):
        return "Fireball.png"

    def __init__(self, game, position, velocity, rotation):
        super().__init__(position, velocity, rotation)
        self.game = game
        self.position = position
        self.velocity = velocity
        self.rotation = rotation
        next_position = self.position
        self.solid = False

    def turn(self):
        next_position = self.next_position
        for entity in self.game.entities.solid:
            if next_position == entity.position:
                if entity.dead:
                    pass
                else:
                    entity.hit()
                    self.destroy()
                    return

        if (
            next_position == self.game.player.last_position
            and self.position == self.game.player.position
        ) or (next_position == self.game.player.position):
            self.game.player.lives -= 1
            self.destroy()
        elif not self.game.map.is_floor(next_position):
            self.destroy()
        else:
            self.position = next_position

    def destroy(self):
        self.game.entities.remove(self)

    @property
    def next_position(self):
        return self.position + self.velocity

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
            fireball = Fireball(
                self.game,
                position=self.position + self.direction,
                velocity=self.direction,
                rotation=self.rotation,
            )
            self.game.entities += [fireball]
            fireball.turn()

    def hit(self):
        pass


class Rotator(Entity):
    pass
