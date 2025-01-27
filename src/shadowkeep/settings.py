import json

import pygame

from shadowkeep.config import SETTINGS_FILE, TILE_HEIGHT, TILE_WIDTH
from shadowkeep.lib.coordinates import Coordinates

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (169, 169, 169)

pygame.init()
font = pygame.font.Font(None, 32)


class Menu:
    def __init__(self, game):
        self.game = game
        self.load_settings()
        self.right_key = f"{pygame.key.name(self.game.player.keys['right'])}"
        self.left_key = f"{pygame.key.name(self.game.player.keys['left'])}"
        self.up_key = f"{pygame.key.name(self.game.player.keys['up'])}"
        self.down_key = f"{pygame.key.name(self.game.player.keys['down'])}"
        self.buttons = [
            Button(
                self.game,
                100,
                200,
                200,
                50,
                "Increase Volume",
                "volume_up",
            ),
            Button(
                self.game,
                100,
                260,
                200,
                50,
                "Decrease Volume",
                "volume_down",
            ),
            Button(
                self.game,
                310,
                320,
                200,
                50,
                self.up_key,
                "up_button",
            ),
            Button(
                self.game,
                310,
                380,
                200,
                50,
                self.down_key,
                "down_button",
            ),
            Button(
                self.game,
                310,
                440,
                200,
                50,
                self.left_key,
                "left_button",
            ),
            Button(
                self.game,
                310,
                500,
                200,
                50,
                self.right_key,
                "right_button",
            ),
            Button(
                self.game,
                550,
                40,
                200,
                50,
                "Exit",
                "exit",
            ),
        ]
        for i, key in enumerate(self.game.player.keys):
            y_position = 320
            offset = 60
            self.buttons.append(
                Button(
                    self.game,
                    100,
                    y_position + offset * i,
                    200,
                    50,
                    f"Change {key} key:",
                    None,
                )
            )
        self.dead_buttons = [
            Button(
                self.game,
                100,
                200,
                200,
                50,
                "Respawn",
                "respawn",
            ),
            Button(
                self.game,
                100,
                260,
                200,
                50,
                "Exit",
                "exit",
            ),
        ]

    def load_settings(self):
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
        else:
            data = {
                "volume": 1,
                "keys": self.game.player.keys,
            }
        self.game.audio.global_volume = data["volume"]
        self.game.player.keys = data["keys"]
        self.game.audio.setting_volume(self.game.audio.global_volume)

    def run(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.game.window)
            if button.is_hovered(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    button.click()

    def respawn_run(self):
        self.respawn_draw(self.game.window)
        mouse_pos = pygame.mouse.get_pos()
        for button in self.dead_buttons:
            button.draw(self.game.window)
            if button.is_hovered(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    button.click()

    def respawn_draw(self, surface):
        pygame.init()
        title_font = pygame.font.Font(None, 110)
        title_surface = title_font.render("You are dead", True, (255, 255, 255))
        self.game.window.blit(title_surface, (5 * TILE_WIDTH, TILE_HEIGHT))


class Button:
    def __init__(self, game, x, y, width, height, text, action):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.action = action
        self.choosing_key = False

    def draw(self, surface):
        pygame.draw.rect(self.game.window, GREY, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        pygame.display.flip()

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def click(self):
        if self.action == "volume_up":
            self.change_volume("+")
        elif self.action == "volume_down":
            self.change_volume("-")
        elif self.action == "up_button":
            self.change_key("up")
        elif self.action == "down_button":
            self.change_key("down")
        elif self.action == "left_button":
            self.change_key("left")
        elif self.action == "right_button":
            self.change_key("right")
        elif self.action == "respawn":
            self.respawn()
        elif self.action == "exit":
            self.game.running = False
        else:
            pass

    def save(self):
        SETTINGS_FILE.parent.mkdir(exist_ok=True)
        data = {
            "volume": self.game.audio.global_volume,
            "keys": self.game.player.keys,
        }
        with open(SETTINGS_FILE, "w+") as f:
            json.dump(data, f)

    def change_volume(self, operation):
        if operation == "+":
            if self.game.audio.global_volume < 2:
                self.game.audio.global_volume += 0.025
        else:
            if self.game.audio.global_volume > 0.0:
                self.game.audio.global_volume -= 0.025
        self.game.audio.setting_volume(self.game.audio.global_volume)
        self.save()

    def change_key(self, key):
        self.choosing_key = True
        self.text = "Press a key"
        while self.choosing_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.choosing_key = False
                        self.text = f"{pygame.key.name(self.game.player.keys[key])}"
                    else:
                        self.game.player.keys[key] = event.key
                        self.text = f"{pygame.key.name(event.key)}"
                        self.choosing_key = False
                        self.save()
            self.draw(self.game.window)

    def respawn(self):
        self.game.current_turn = 0
        self.game.player.position = Coordinates(
            self.game.data["player_initial_x_position"],
            self.game.data["player_initial_y_position"],
        )
        self.game.player.lives = 4
        for entity in self.game.entities:
            entity.destroy()
        self.game.add_entities()
        self.game.end_screen = False
