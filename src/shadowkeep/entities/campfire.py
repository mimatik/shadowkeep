import pygame

from shadowkeep.config import (
    IMG_DIR,
    TILE_HEIGHT,
    TILE_WIDTH,
)
from shadowkeep.entities.match import Match

from .base import Entity


class Campfires(Entity):
    def __init__(self, game, position=None):
        super().__init__(game=game, position=position, solid=True)
        self.game = game
        self.is_lit = False
        self.surface = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))

    def get_image(self):
        return "unlit_campfire.png"

    def interact(self, dir):
        if self.game.player.number_of_matches > 0 and not self.is_lit:
            self.game.player.number_of_matches -= 1
            self.game.inventory.remove(
                [match for match in self.game.inventory.of_type(Match)][0]
            )
            self.is_lit = True
        if self.is_lit:
            self.game.dynamic_light.radius = 10 * TILE_HEIGHT

    def blit(self):
        if self.dead:
            pass
        else:
            if self.is_lit:
                self.surface = pygame.image.load(IMG_DIR / "lit_campfire.png")
                self.game.dynamic_layer.place_surface(
                    self.surface, self.position.transformed_pair()
                )
            else:
                self.surface = pygame.image.load(IMG_DIR / "unlit_campfire.png")
                self.game.dynamic_layer.place_surface(
                    self.surface, self.position.transformed_pair()
                )
