import logging

from .base import Entity

logger = logging.getLogger("shadowkeep")


class Door(Entity):
    def interact(self, *args, **kwargs):
        if self.game.keys > 0:
            self.game.keys -= 1
            self.destroy()
            self.game.player.ghost_step()

    def get_image(self):
        return "Door.png"


class Key(Entity):
    def interact(self, *args, **kwargs):
        self.destroy()
        self.game.player.ghost_step()
        self.game.keys += 1
        logger.info("added key")

    def get_image(self):
        return "Key.png"
