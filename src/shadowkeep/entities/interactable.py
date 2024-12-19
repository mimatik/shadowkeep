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
        if self.position == self.game.player.next_position:
            self._meet_player()

    def _meet_player(self):
        pass
