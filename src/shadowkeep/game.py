import json
import logging

import pygame
from PIL import Image
from pygame import Surface
from requests.packages import target

from shadowkeep import config
from shadowkeep.audio import Audio
from shadowkeep.config import LEVELS_DIR, TILE_HEIGHT, TILE_WIDTH
from shadowkeep.dialog import Dialog
from shadowkeep.dynamic_light import DynamicLight
from shadowkeep.entities import Entities
from shadowkeep.entities.base import End
from shadowkeep.entities.campfire import Campfires
from shadowkeep.entities.doors_keys import (
    Door,
    Key,
)
from shadowkeep.entities.fireballs import (
    Fireball,
    FireballLauncher,
)
from shadowkeep.entities.interactable import Box
from shadowkeep.entities.match import Match
from shadowkeep.entities.monsters import (
    BadMonster,
    TalkingMonster,
)
from shadowkeep.entities.slot import Slot
from shadowkeep.entities.trapdoor import Trapdoor
from shadowkeep.layer import Layer
from shadowkeep.lib.coordinates import Coordinates
from shadowkeep.lib.inventory import Inventory
from shadowkeep.lib.open_ai import ChatGPT
from shadowkeep.map import Map
from shadowkeep.player import Player
from shadowkeep.settings import Menu

logger = logging.getLogger("shadowkeep")
# Size of the window


class Game:
    def __init__(self):
        # pygame.init()
        pygame.display.set_caption("Shadowkeep")
        self.clock = pygame.time.Clock()
        self.running = True
        self.width = 24
        self.height = 24

        self.level = "01"

        self.window = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)  # , pygame.FULLSCREEN
        )

        with open(LEVELS_DIR / self.level / "data.json", "r") as f:
            self.data = json.load(f)

        self.entities = Entities()
        self.map = Map(self)
        self.player = Player(self)

        self.background_layer = Layer(self)
        self.dynamic_layer = Layer(self)
        self.ui_layer = Layer(self)

        self.inventory = Inventory()

        self.logic = []
        self.chatGPT = ChatGPT(self)

        self.current_turn = 0
        self.keys = 0
        self.map.blit()
        self.audio = Audio(self)
        self.menu = Menu(self)

        self.dialog = Dialog(self)

        # self.load_logic()

        # self.load_logic()\

        self.in_menu = True

        self.end_screen = False

        self.dynamic_light = DynamicLight(self)

        logger.info("game:start")
        self.add_entities()

    def add_entities(self):
        self.map.blit()
        self.load_data()
        self.entities += [Box(self, position=Coordinates(2, 13))]
        self.entities += [Door(self, position=Coordinates(12, 16))]
        self.entities += [
            TalkingMonster(self) for x in range(self.data["number_of_good_monsters"])
        ]
        self.entities += [
            BadMonster(self) for x in range(self.data["number_of_bad_monsters"])
        ]
        self.entities += [Match(self, position=Coordinates(2, 2))]
        self.entities += [Match(self, position=Coordinates(3, 3))]

        logger.info("game:start")

        # print(open_ai_get_response("jak se mas"))

    def turn(self):
        self.current_turn += 1
        self.dynamic_light.change_light()
        for entity in self.entities[:]:
            entity.turn()

        if self.player.lives == 0:
            self.update()
            self.blit_layers()
            self.end_screen = True

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
        with Image.open(LEVELS_DIR / self.level / "map.png") as image:
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
                        case (9, 9, 9, 255):
                            self.entities.append(
                                Campfires(self, position=Coordinates(x, y))
                            )
                        case (8, 8, 8, 255):
                            self.entities.append(
                                Match(self, position=Coordinates(x, y))
                            )
                        case (0, 255, 0, 255):
                            self.entities.append(End(self, position=Coordinates(x, y)))
                        case (255, 0, 255, 255):
                            self.entities.append(
                                Trapdoor(self, position=Coordinates(x, y))
                            )
                        case (0, 0, 255, 255):
                            self.player.position = Coordinates(x, y)
                            self.player.transformed_position = ()
                            self.data["player_initial_x_position"] = x
                            self.data["player_initial_y_position"] = y
                            with open(LEVELS_DIR / self.level / "data.json", "w") as f:
                                json.dump(self.data, f)

    def update(self):
        self.dynamic_layer.clear()
        self.ui_layer.clear()
        self.dialog.blit()
        self.dialog.blit()
        self.inventory.blit()

        for entity in self.entities:
            if entity.position and self.map.is_floor(entity.position):
                entity.blit()
        for firebal in self.entities.of_type(Fireball):
            if firebal.position and self.map.is_floor(firebal.position):
                firebal.blit()
        self.player.blit()

    def blit_layers(self):
        self.background_layer.blit()
        self.dynamic_layer.blit()
        self.dynamic_light.draw()
        pygame.display.update()

    def draw_settings_title(self):
        # pygame.init()
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
                        if self.in_menu or self.end_screen:
                            self.in_menu = False
                        else:
                            self.in_menu = True
                    elif not self.in_menu and not self.end_screen:
                        self.player.move()
            if self.in_menu:
                self.draw_settings_title()
                self.menu.run()
            elif self.end_screen:
                self.menu.respawn_run()
            else:
                self.audio.random_sfx_play()
                self.dialog.backspace_update()  # enables multiple chars deletion by holding backspace
                self.update()
                self.blit_layers()
            self.clock.tick(config.FPS)
