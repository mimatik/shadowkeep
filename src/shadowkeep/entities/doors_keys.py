import logging

from shadowkeep.lib.coordinates import Coordinates

from .base import Entity, Pickeable

logger = logging.getLogger("shadowkeep")


class Door(Entity):
    def __init__(self, game, position=Coordinates(0, 0), pair=0):
        super().__init__(game=game, position=position)
        self.pair = pair

    def interact(self, *args, **kwargs):
        if any(self.pair == key.pair for key in self.game.inventory.of_type(Key)):
            self.game.inventory.remove(
                [
                    key
                    for key in self.game.inventory.of_type(Key)
                    if key.pair == self.pair
                ][0]
            )
            self.destroy()
            logger.info(
                f"opened door pair {self.pair} on x:{self.position.x} y:{self.position.y}"
            )

    def get_image(self):
        return "Door.png"


class Key(Pickeable):
    def __init__(self, game, position=Coordinates(0, 0), pair=0):
        super().__init__(game=game, position=position)
        self.pair = pair

    def interact(self, *args, **kwargs):
        logger.info(
            f"moved key pair {self.pair} on x:{self.position.x} y:{self.position.y}"
        )
        self.move_to_inventory()
        self.game.player.ghost_step()

    def get_image(self):
        return "Key.png"
