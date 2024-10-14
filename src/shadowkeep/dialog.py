import pygame
from shadowkeep.text import TextInput


class Dialog:
    def __init__(self, game):
        self.game = game
        self.is_open = False

        self.bubble_moster = TextInput(game, theme="dark")
        self.text_moster = "Jake je heslo?"

        self.bubble_player = TextInput(game)
        self.text_player = ""

        self.backspace_timer = 0
        self.backspace_pressed = False

    def read_key(self, event):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_RETURN]:
            self.is_open = False
            self.text_player = ""
        elif pressed_keys[pygame.K_ESCAPE]:
            self.text_player = ""
            self.is_open = False
        elif pressed_keys[pygame.K_BACKSPACE]:
            self.text_player = self.text_player[:-1]
            self.backspace_pressed = True
            self.backspace_timer = pygame.time.get_ticks()
        else:
            self.text_player += event.unicode

    def backspace_update(self):
        if self.backspace_pressed:
            if pygame.time.get_ticks() - self.backspace_timer > 80:
                self.text_player = self.text_player[:-1]
                self.backspace_timer = pygame.time.get_ticks()

        if not pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            self.backspace_pressed = False

    def blit(self):
        if self.is_open:
            self.bubble_moster.blit(self.text_moster, (20, 20))
            self.bubble_player.blit(self.text_player, (20, 180))
