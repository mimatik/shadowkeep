import logging
import random

import pygame
from PIL import Image
from pygame import Surface
from requests.packages import target

from shadowkeep import config
from shadowkeep.audio import Audio
from shadowkeep.config import IMG_DIR, TILE_HEIGHT, TILE_WIDTH
from shadowkeep.dialog import Dialog
from shadowkeep.entities import Entities
from shadowkeep.entities.base import End
from shadowkeep.entities.doors_keys import (
    Door,
    Key,
)
from shadowkeep.entities.fireballs import (
    Fireball,
    FireballLauncher,
)
from shadowkeep.entities.interactable import Box
from shadowkeep.entities.monsters import (
    BadMonster,
    TalkingMonster,
)
from shadowkeep.layer import Layer
from shadowkeep.lib.coordinates import Coordinates
from shadowkeep.lib.inventory import Inventory
from shadowkeep.lib.open_ai import ChatGPT
from shadowkeep.map import Map
from shadowkeep.player import Player
from shadowkeep.settings import Menu

logger = logging.getLogger("shadowkeep")


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Shadowkeep")
        self.window = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.running = True

        self.background_layer = Layer(self)
        self.dynamic_layer = Layer(self)
        self.ui_layer = Layer(self)

        self.map = Map(self)
        self.player = Player(self)
        self.inventory = Inventory()

        self.entities = Entities()
        self.entities += [Box(self, position=Coordinates(2, 13))]
        self.entities += [Door(self, position=Coordinates(12, 16))]
        self.entities += [TalkingMonster(self) for x in range(7)]
        self.entities += [BadMonster(self) for x in range(4)]

        self.audio = Audio(self)
        self.menu = Menu(self)
        self.menu.load()

        self.logic = []
        self.chatGPT = ChatGPT(self)

        self.current_turn = 0
        self.keys = 0

        self.dialog = Dialog(self)

        self.map.blit()

        self.load_data()
        # self.load_logic()

        self.in_menu = True

        logger.info("game:start")

    def turn(self):
        self.current_turn += 1
        for entity in self.entities[:]:
            entity.turn()

        if self.player.lives == 0:
            self.running = False

    # def load_logic(self):
    #     try:
    #         with Image.open(IMG_DIR / "logic.png") as image:
    #             self.width, self.height = image.size
    #
    #             for y in range(self.height):
    #                 for x in range(self.width):
    #                     self.pixel = image.getpixel((x, y))
    #     except:
    #         print("error")

    def load_data(self):
        with Image.open(IMG_DIR / "map.png") as image:
            self.width, self.height = image.size

            for y in range(self.height):
                for x in range(self.width):
                    pixel = image.getpixel((x, y))
                    match pixel:
                        case (255, 0, rotation, 255) if rotation in {0, 1, 2, 3}:
                            self.entities.append(
                                FireballLauncher(
                                    self,
                                    rotation=rotation * 90,
                                    position=Coordinates(x, y),
                                )
                            )
                        case (187, 187, pair, 255):
                            self.entities.append(
                                Door(self, position=Coordinates(x, y), pair=pair)
                            )
                        case (170, 170, pair, 255):
                            self.entities.append(
                                Key(
                                    self,
                                    position=Coordinates(x, y),
                                    pair=pair,
                                )
                            )
                        case (0, 255, 0, 255):
                            self.entities.append(End(self, position=Coordinates(x, y)))
                        case (0, 0, 255, 255):
                            self.player.position = Coordinates(x, y)

    def update(self):
        self.dynamic_layer.clear()
        self.ui_layer.clear()
        self.player.blit()
        self.dialog.blit()

        for entity in self.entities:
            if entity.position and self.map.is_floor(entity.position):
                entity.blit()
        for firebal in self.entities.of_type(Fireball):
            if firebal.position and self.map.is_floor(firebal.position):
                firebal.blit()

    def blit_layers(self):
        self.background_layer.blit()
        self.dynamic_layer.blit()
        self.ui_layer.blit()
        pygame.display.update()

    def draw_settings_title(self):
        pygame.init()
        title_font = pygame.font.Font(None, 110)
        title_surface = title_font.render("settings", True, (255, 255, 255))
        self.window.blit(title_surface, (7 * TILE_WIDTH, TILE_HEIGHT))

    def run(self):
        self.audio.play()
        while self.running:
            self.audio.random_sfx_play()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    pressed_key = pygame.key.get_pressed()
                    if self.dialog.is_open:
                        self.dialog.read_key(event)
                    elif pressed_key[pygame.K_ESCAPE]:
                        if self.in_menu:
                            self.in_menu = False
                        else:
                            self.in_menu = True
                    elif not self.in_menu:
                        self.player.move()

            if self.in_menu:
                self.draw_settings_title()
                self.menu.run()
            else:
                self.audio.random_sfx_play()
                self.dialog.backspace_update()  # enables multiple chars deletion by holding backspace
                self.update()
                self.blit_layers()
            self.clock.tick(config.FPS)
