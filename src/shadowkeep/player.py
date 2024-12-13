import pygame

from shadowkeep.config import AUDIO_DIR, IMG_DIR, TILE_HEIGHT, TILE_WIDTH, WINDOW_WIDTH
from shadowkeep.lib.coordinates import Coordinates


class Player:
    def __init__(self, game):
        self.game = game
        self.surface = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.surface = pygame.image.load(IMG_DIR / "Player.png")
        self.health_surface = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.health_surface = pygame.image.load(IMG_DIR / "heart.png")
        self.broken_health_surface = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.broken_health_surface = pygame.image.load(IMG_DIR / "broken_heart.png")
        self.last_pressed = 0
        self.position = Coordinates(11, 10)
        self.last_position = Coordinates()
        self.next_position = Coordinates()
        self.player_move_sfx = pygame.mixer.Sound(AUDIO_DIR / "player_move.mp3")
        self.player_move_sfx.set_volume(0.3)
        self.max_lives = 4
        self.lives = 4

    def move(self):
        movement = None

        pressed_keys = pygame.key.get_pressed()

        if sum(pressed_keys) > 1:
            return

        if pressed_keys[pygame.K_w]:
            movement = Coordinates(y=-1)

        if pressed_keys[pygame.K_s]:
            movement = Coordinates(y=+1)

        if pressed_keys[pygame.K_d]:
            movement = Coordinates(x=+1)

        if pressed_keys[pygame.K_a]:
            movement = Coordinates(x=-1)

        if movement:
            self.moved_dir = movement
            self.next_position = self.position + movement
            self.player_move_sfx.play()
            self.game.turn()
            self.last_position = self.position

    def ghost_step(self):
        self.position = self.next_position

    def _blit_health_surface(self, lives):
        if self.lives >= lives:
            surface = self.health_surface
        else:
            surface = self.broken_health_surface

        self.game.ui_layer.place_surface(surface, ((WINDOW_WIDTH - 2 * TILE_WIDTH) - (self.max_lives - lives) * 40, TILE_HEIGHT))

    def blit(self):
        self.game.dynamic_layer.place_surface(
            self.surface, self.position.transformed_pair()
        )
        for i in range(1, self.max_lives + 1):
            self._blit_health_surface(i)


