import json
import pygame
from pygame.examples.music_drop_fade import volume

from shadowkeep.config import SETTINGS_FILE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (169, 169, 169)

pygame.init()
font = pygame.font.Font(None, 32)


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
        elif self.text == "volume_down":
            self.change_volume("-")
        elif self.text == "Decrease Volume":
            self.decreace_volume()
        elif self.text == "Decrease Volume":
            self.decreace_volume()
        elif self.text == "Decrease Volume":
            self.decreace_volume()
        elif self.text == "Decrease Volume":
            self.decreace_volume()
        else:
            pass

    def save(self):
        SETTINGS_FILE.parent.mkdir(exist_ok=True)
        data = {
            "volume" : self.game.audio.global_volume,
        }
        with open(SETTINGS_FILE, 'w+') as f:
            json.dump(data, f)

    def load(self):
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
        else:
            data = {
                "volume": 1,
            }
        self.game.audio.global_volume = data[volume]

    def change_volume(self, operation):
        if self.game.audio.global_volume < 2 and self.game.audio.global_volume > 0.0:
            if operation == "+":
                self.game.audio.global_volume += 0.025
            else:
                self.game.audio.global_volume -= 0.025
            self.game.audio.set_volume(self.game.audio.global_volume)
            self.save()


