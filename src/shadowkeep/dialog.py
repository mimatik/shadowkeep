import pygame
from shadowkeep.text import TextInput


class Dialog:
    def __init__(self, game):
        self.game = game
        self.is_open = False

        self.bubble_moster = TextInput(game, theme="dark")
        self.text_moster = "Zeptej se na neco"

        self.bubble_player = TextInput(game)
        self.text_player = ""

        self.backspace_timer = 0
        self.backspace_pressed = False

        self.go = True

        self.guesses = 0

    def start(self, text):
        self.is_open = True
        self.text_moster = text
        self.game.chatGTP.conversation_history = [
            {
                "role": "system",
                "content": """Jste monster, ktery dava hadanky a který vrací odpovědi ve formátu JSON.
                 Pouzivej key Answers.Hodnota bude vzdy string.
                 Kdyz mi das hadanku(jenom kdys se te zeptam abys mi ji dal) a ja ti odpovim spatne,
                 tak hodnota bude Lez, pokud odpovim spravne, tak hodnota bude Pravda,
                 a pokud nebudu odpovidat na hadanku, tak hodnotu vymyslis ty.""",
            }
        ]

    def read_key(self, event):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_ESCAPE]:
            self.is_open = False
            self.text_player = ""
        elif pressed_keys[pygame.K_RETURN]:
            self.is_open = False
            self.game.chatGTP.text = self.text_player
            self.text_moster = self.game.chatGTP.open_ai_get_response()["Answers"]
            if self.text_moster == "Lez":
                self.guesses += 1
                self.text_moster = "Spatne, skus jeste jednou"
            if self.text_moster == "Pravda":
                self.guesses = 0
                self.text_moster = "Spravne"
            if self.guesses == 3:
                self.game.running = False
            self.text_player = ""
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

    def blit(self):
        if self.is_open:
            self.bubble_moster.blit(self.text_moster, (20, 20))
            self.bubble_player.blit(
                self.text_player,
                (20, self.bubble_moster.surface_height + 40),
            )
