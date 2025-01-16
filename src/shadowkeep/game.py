import logging

import pygame
from PIL import Image
from pygame import Surface
from requests.packages import target

from shadowkeep import config
from shadowkeep.audio import Audio
from shadowkeep.config import IMG_DIR
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
from shadowkeep.entities.slot import Slot
from shadowkeep.layer import Layer
from shadowkeep.lib.coordinates import Coordinates
from shadowkeep.lib.inventory import Inventory
from shadowkeep.lib.open_ai import ChatGPT
from shadowkeep.map import Map
from shadowkeep.player import Player

logger = logging.getLogger("shadowkeep")
# Size of the window


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Shadowkeep")
        self.clock = pygame.time.Clock()
        self.running = True

        self.entities = Entities()
        self.map = Map(self)
        self.player = Player(self)
        self.load_data()
        self.window = pygame.display.set_mode(
            (self.width * config.TILE_WIDTH, self.height * config.TILE_HEIGHT)
        )

        self.background_layer = Layer(self)
        self.dynamic_layer = Layer(self)
        self.ui_layer = Layer(self)

        self.inventory = Inventory()

        self.entities += [Box(self, position=Coordinates(2, 13))]
        self.entities += [Door(self, position=Coordinates(12, 16))]
        self.entities += [TalkingMonster(self) for x in range(7)]
        self.entities += [BadMonster(self) for x in range(4)]

        self.logic = []
        self.chatGPT = ChatGPT(self)

        self.audio = Audio(self)

        self.current_turn = 0
        self.keys = 0
        self.map.blit()

        self.dialog = Dialog(self)

        # self.load_logic()

        logger.info("game:start")

        # print(open_ai_get_response("jak se mas"))

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
        self.inventory.blit()

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

    def run(self):
        self.audio.play()
        while self.running:
            self.audio.random_sfx_play()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.dialog.is_open:
                        self.dialog.read_key(event)
                    else:
                        self.player.move()

            self.dialog.backspace_update()  # enables multiple chars deletion by holding backspace
            self.update()
            self.blit_layers()
            self.clock.tick(config.FPS)
