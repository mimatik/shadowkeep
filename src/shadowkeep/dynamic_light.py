import pygame

from shadowkeep.config import TILE_HEIGHT, TILE_WIDTH


class Dynamic_light:
    def __init__(self, game):
        self.game = game
        self.radius = 10 * TILE_HEIGHT

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
                self.game.player.position.x * TILE_WIDTH + 16,
                self.game.player.position.y * TILE_HEIGHT + 16,
            ),
            self.radius,
        )
        self.game.window.blit(self.dark_layer, (0, 0))
        self.game.ui_layer.blit()
        pygame.display.flip()
