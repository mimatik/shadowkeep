from dis import Positions

import pygame

from shadowkeep.config import AUDIO_DIR, IMG_DIR, TILE_HEIGHT, TILE_WIDTH
from shadowkeep.lib.coordinates import Coordinates


class Player:
    def __init__(self, game):
        self.game = game
        self.surface = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.surface = pygame.image.load(IMG_DIR / "Player.png")
        self.last_pressed = 0
        self.position = Coordinates(11, 10)
        self.player_move_sfx = pygame.mixer.Sound(AUDIO_DIR / "player_move.mp3")
        self.player_move_sfx.set_volume(0.3)
        self.last_movement = Coordinates()
        self.movement = Coordinates()

    def move(self):
        self.movement = Coordinates()

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

        self.next_movement = self.position + movement

        self.player_move_sfx.play()
        self.game.turn()

    def blit(self):
        self.game.dynamic_layer.place_surface(
            self.surface, self.position.transformed_pair()
        )
