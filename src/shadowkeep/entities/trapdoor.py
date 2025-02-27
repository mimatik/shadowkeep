from .base import Entity


class Trapdoor(Entity):
    def __init__(self, game, position):
        super().__init__(game=game, position=position, solid=False)
        self.game = game
        self.position = position

    def get_image(self):
        return "trapdoor.png"

    def turn(self):
        for entity in self.game.entities.not_of_type(Trapdoor):
            if entity.position == self.position:
                entity.destroy()
        if self.position == self.game.player.position:
            self.game.player.lives = 0
            self.game.player.blit()
            self.game.update()
            self.game.blit_layers()
            self.game.end_screen = True
