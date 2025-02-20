import pygame

from shadowkeep.config import TILE_HEIGHT, TILE_WIDTH
from shadowkeep.entities.campfire import Campfires


class DynamicLight:
    def __init__(self, game):
        self.game = game
        self.radius = 10 * TILE_HEIGHT
        self.half_of_tile = TILE_HEIGHT / 2

    def draw(self):
        self.dark_layer = self.surface = pygame.surface.Surface(
            (self.game.window.get_width(), self.game.window.get_height()),
            pygame.SRCALPHA,
        )
        self.dark_layer.fill((0, 0, 0, 255))
        pygame.draw.circle(
            self.dark_layer,
            (0, 0, 0, 0),
            (
                (self.game.player.position.x + 0.5) * TILE_WIDTH,
                (self.game.player.position.y + 0.5) * TILE_HEIGHT,
            ),
            self.radius,
        )
        for campfire in self.game.entities.of_type(Campfires):
            if campfire.is_lit:
                pygame.draw.circle(
                    self.dark_layer,
                    (0, 0, 0, 0),
                    (
                        (campfire.position.x + 0.5) * TILE_WIDTH,
                        (campfire.position.y + 0.5) * TILE_HEIGHT,
                    ),
                    self.radius,
                )
        self.game.window.blit(self.dark_layer, (0, 0))
        self.game.ui_layer.blit()
        pygame.display.flip()
