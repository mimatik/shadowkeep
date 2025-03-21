import pygame

from shadowkeep.config import IMG_DIR
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

        self.monster_surface = pygame.surface.Surface((400, 400))
        self.monster_surface = pygame.image.load(IMG_DIR / "monster.jpg")

        self.player_surface = pygame.surface.Surface((400, 400))
        self.player_surface = pygame.image.load(IMG_DIR / "player.jpg")

    def start(self, text):
        self.is_open = True
        self.text_moster = text
        self.game.chatGPT.conversation_history = [
            {
                "role": "system",
                "content": """
                    Jste NPC ve hře, ktery dava hadanky a který vrací odpovědi
                    ve formátu JSON.  Máš klíč, který můžeš dát hráči, ale jen pokud
                    správně odpoví na hádanku, kterou mu dáš.  Máš smysl pro suchý
                    humor a ironii. Neprozraď hráči, že jsi AI, hraj roli NPC.

                    Vždy používej formát:
                        {
                            "command": {command},
                            "text": "{text}"
                        }
                    Command je string, který může být:
                        - say: řekni text, v tom případě text bude obsahovat text,
                          který mám říct
                        - end_dialogue: ukonči dialog, pokud hráč již 3x neuhodl
                        - attack: zaútoč na hráče, pokud bude hráč diskutovat útočně
                        - give_key: předej hráči klíč, kdyz odpovy zapravne na otazku
                          nebo jeho odpovet sedi

                    Kdyz das hraci klic, tak az priste neco rekne ta vrat "end dialogue"
                     """,
            }
        ]

    def read_key(self, event):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_ESCAPE]:
            self.is_open = False
            self.text_player = ""
        elif pressed_keys[pygame.K_RETURN]:
            self.is_open = False
            self.game.chatGPT.text = self.text_player
            self.text_moster = self.game.chatGPT.response()
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
            self.bubble_moster.blit(self.text_moster, (80, 20))
            self.bubble_player.blit(
                self.text_player,
                (80, self.bubble_moster.surface_height + 40),
            )
            self.game.ui_layer.place_surface(
                self.monster_surface,
                (
                    20,
                    10,
                ),
            )

            self.game.ui_layer.place_surface(
                self.player_surface,
                (
                    20,
                    self.bubble_moster.surface_height + 40,
                ),
            )
