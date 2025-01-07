import random

import pygame

from shadowkeep.config import AUDIO_DIR


class Audio:
    def __init__(self, game):
        self.game = game
        self.global_volume = None

        self.random_sfx = pygame.mixer.Sound(AUDIO_DIR / "random_sound.mp3")
        self.random_sfx.set_volume(0.1)

        self.random_sfx2 = pygame.mixer.Sound(AUDIO_DIR / "random_sound2.mp3")
        self.random_sfx2.set_volume(0.2)

        self.random = random.randint(1, 9)
        self.background_sfx = pygame.mixer.Sound(
            AUDIO_DIR / f"background_music{self.random}.mp3"
        )

    def play(self):
        self.background_sfx.set_volume(self.global_volume)
        self.background_sfx.play(-1)

    def random_sfx_play(self):
        if random.randint(0, 1000) == 1:
            self.random_sfx.play()
        if random.randint(0, 10000) == 1:
            self.random_sfx2.play()

    def setting_volume(self, volume):
        self.random_sfx.set_volume(volume)
        self.random_sfx2.set_volume(volume)
        self.background_sfx.set_volume(volume)
