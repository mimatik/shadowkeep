from .base import Pickeable


class Match(Pickeable):
    def get_image(self):
        return "match.png"

    def interact(self, dir):
        self.move_to_inventory()
        self.game.player.ghost_step()
        self.game.player.number_of_matches += 1
