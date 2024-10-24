import pygame
from pygame.examples.scrap_clipboard import going
from shadowkeep.text import TextInput


class Dialog:
    def __init__(self, game):
        self.game = game
        self.is_open = False

        self.bubble_moster = TextInput(game, theme="dark")
        self.text_moster_to_print = "Zeptej se na neco"
        self.text_moster = "a"

        self.bubble_player = TextInput(game)
        self.text_player = ""

        self.backspace_timer = 0
        self.backspace_pressed = False

        self.go = True

    def monster_text_loader(self):
        self.letters = 0
        self.go = True
        self.with_one = 0
        current_time = pygame.time.get_ticks()
        self.last_loaded = 0
        self.monster_text = []
        self.with_one = 0
        for letter in self.text_moster_to_print:
            self.monster_text += letter
            self.letters += 1

        while self.go:
            if current_time > self.last_loaded:
                self.last_loaded += 0.2
                self.text_moster += self.monster_text[self.with_one]
                self.with_one += 1
                if self.with_one > self.letters:
                    self.go = False

    def read_key(self, event):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_ESCAPE]:
            self.is_open = False
            self.text_player = ""
        elif pressed_keys[pygame.K_RETURN]:
            self.is_open = False
            self.game.chatGTP.text = self.text_player
            self.text_player = ""
            self.text_moster_to_print = self.game.chatGTP.open_ai_get_response()
            self.is_open = True
            self.monster_text_loader()
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
            self.bubble_player.blit(
                self.text_player,
                (20, self.bubble_moster.surface_height + 40),
            )
