import logging
from .base import Entity

logger = logging.getLogger("shadowkeep")


class Door(Entity):

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

    def interact(self, *args, **kwargs):
        if self.game.keys > 0:
            self.game.keys -= 1
            self.destroy()
            self.game.player.ghost_step()

    def get_image(self):
        return "Door.png"


class Key(Entity):
    def turn(self):
        if self.dead:
            self.dead_time += 1
            if self.dead_time == 10:
                self.dead_time = 0
        # else:
        #     if self.position == self.game.player.position:
        #         self._meet_player()

    def interact(self, *args, **kwargs):
        self.destroy()
        self.game.player.ghost_step()
        self.game.keys += 1
        logger.info("added key")

    def get_image(self):
        return "Key.png"
