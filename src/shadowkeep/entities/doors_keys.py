import logging
from .base import Entity
logger = logging.getLogger("shadowkeep")

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

