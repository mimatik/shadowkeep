import logging

from shadowkeep.lib.coordinates import Coordinates
from .base import Entity

logger = logging.getLogger("shadowkeep")


class Box(Entity):
    def __init__(self, game, position=Coordinates(0, 0)):
        super().__init__(game=game, position=position, solid=True, movable=True)

    def get_image(self):
        return "Box.png"

    def turn(self):
        if self.dead:
            self.dead_time += 1
            if self.dead_time == 10:
                self.dead_time = 0
                self.dead = False
                self.solid = True
        # else:
        #     if self.position == self.game.player.position:
        #         self._meet_player()

    def interact(self, dir=Coordinates(0, 0)):
        if self.movable and self.game.map.is_floor(
            self.position + dir
        ) and not self.game.entities.on_position(self.position + dir):
            self.position += dir

    def hit(self):
        pass

    def _meet_player(self):
        self.interact(dir=self.game.player.moved_dir)
