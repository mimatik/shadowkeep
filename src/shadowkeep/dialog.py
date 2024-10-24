import pygame
from shadowkeep.text import TextInput


class Dialog:
    def __init__(self, game):
        self.game = game
        self.is_open = False

        self.bubble_monster = TextInput(game, theme="dark")
        self.text_monster_full = "Zeptej se na neco"
        self.text_monster_display = ""
        self.text_monster_index = 0
        self.text_monster_timer = 0
        self.text_monster_speed = 30

        self.bubble_player = TextInput(game)
        self.text_player = ""
        self.show_player_bubble = False

        self.backspace_timer = 0
        self.backspace_pressed = False

    def read_key(self, event):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_ESCAPE]:
            self.is_open = False
            self.text_player = ""

        elif pressed_keys[pygame.K_RETURN]:
            self.is_open = False
            self.game.chatGTP.text = self.text_player

            self.text_player = ""
            self.show_player_bubble = False

            self.text_monster_display = ""
            self.text_monster_index = 0
            self.text_monster_full = self.game.chatGTP.open_ai_get_response()
            self.text_monster_timer = pygame.time.get_ticks()

            self.is_open = True

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

    def text_monster(self):
        if self.text_monster_index < len(self.text_monster_full):
            current_time = pygame.time.get_ticks()

            if current_time - self.text_monster_timer > self.text_monster_speed:
                self.text_monster_display += self.text_monster_full[
                    self.text_monster_index
                ]
                self.text_monster_index += 1
                self.text_monster_timer = current_time

            if self.text_monster_index >= len(self.text_monster_full):
                self.show_player_bubble = True

    def blit(self):
        if self.is_open:
            self.text_monster()
            self.bubble_monster.blit(self.text_monster_display, (20, 20))

            if self.show_player_bubble:
                self.bubble_player.blit(
                    self.text_player,
                    (20, self.bubble_monster.surface_height + 40),
                )
