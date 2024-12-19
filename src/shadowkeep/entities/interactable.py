import logging

from shadowkeep.lib.coordinates import Coordinates
from .base import Entity

logger = logging.getLogger("shadowkeep")


class Box(Entity):
    def __init__(self, game, position=Coordinates(0, 0)):
        super().__init__(game=game, position=position, solid=True)

    def get_image(self):
        return "Box.png"

    def turn(self):
        if self.dead:
            self.dead_time += 1
            if self.dead_time == 10:
                self.dead_time = 0
                self.dead = False
                self.solid = True
        else:
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
