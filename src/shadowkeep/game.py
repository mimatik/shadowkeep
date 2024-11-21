import random
import logging
import pygame
from PIL import Image
from pygame import Surface

from shadowkeep import config
from shadowkeep.config import AUDIO_DIR, IMG_DIR, TILE_HEIGHT, TILE_WIDTH
from shadowkeep.dialog import Dialog
from shadowkeep.layer import Layer
from shadowkeep.lib.coordinates import Coordinates
from shadowkeep.lib.open_ai import ChatGTP
from shadowkeep.map import Map
from shadowkeep.entities import Entities
from shadowkeep.monster import (
    BadMonster,
    Fireball,
    FireballLauncher,
    Key,
    TalkingMonster,
    Door,
    End,
    Box,
)
from shadowkeep.player import Player

logger = logging.getLogger("shadowkeep")

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Platformer")
        self.window = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.running = True

        self.background_layer = Layer(self)
        self.dynamic_layer = Layer(self)
        self.ui_layer = Layer(self)

        self.entities = Entities(self)
        self.map = Map(self)
        self.player = Player(self)
        self.monsters = [TalkingMonster(self) for x in range(7)]
        self.monsters += [BadMonster(self) for x in range(4)]
        self.logic = []
        self.monsters += [Box(self, position=Coordinates(2, 13))]
        self.chatGTP = ChatGTP(self)

        self.firebals = []

        self.current_turn = 0
        self.keys = 0

        self.dialog = Dialog(self)

        self.map.blit()

        self.load_data()
        self.load_logic()

        self.backround_sfx = pygame.mixer.Sound(AUDIO_DIR / "backround_music.mp3")
        self.backround_sfx.set_volume(0.2)

        self.random_sfx = pygame.mixer.Sound(AUDIO_DIR / "random_sound.mp3")
        self.random_sfx.set_volume(0.1)

        self.random_sfx2 = pygame.mixer.Sound(AUDIO_DIR / "random_sound2.mp3")
        self.random_sfx2.set_volume(0.2)

        logger.info("game:start")

        # print(open_ai_get_response("jak se mas"))

    def turn(self):
        if self.map.is_floor(self.player.next_position) and not any(
            monster.position == self.player.next_position for monster in self.monsters
        ):
            self.player.position = self.player.next_position

        elif any(
            firebal.position == self.player.next_position for firebal in self.firebals
        ):
            self.player.position = self.player.next_position

        self.current_turn += 1
        for monster in self.monsters[:]:
            monster.turn()

        for fireball in self.firebals[:]:
            fireball.turn()


    def load_logic(self):
        try:
            with Image.open(IMG_DIR / "logic.png") as image:
                self.width, self.height = image.size

                for y in range(self.height):
                    for x in range(self.width):
                        self.pixel = image.getpixel((x, y))
        except:
            print("error")

    def load_data(self):
        with Image.open(IMG_DIR / "map.png") as image:
            self.width, self.height = image.size

            for y in range(self.height):
                for x in range(self.width):
                    self.pixel = image.getpixel((x, y))
                    if self.pixel == (255, 0, 0, 255):
                        self.monsters.append(
                            FireballLauncher(
                                self, rotation=270, position=Coordinates(x, y)
                            )
                        )
                    if self.pixel == (255, 0, 1, 255):
                        self.monsters.append(
                            FireballLauncher(
                                self, rotation=0, position=Coordinates(x, y)
                            )
                        )
                    if self.pixel == (255, 0, 2, 255):
                        self.monsters.append(
                            FireballLauncher(
                                self, rotation=90, position=Coordinates(x, y)
                            )
                        )
                    if self.pixel == (255, 0, 3, 255):
                        self.monsters.append(
                            FireballLauncher(
                                self, rotation=180, position=Coordinates(x, y)
                            )
                        )
                    if self.pixel == (255, 255, 0, 255):
                        self.monsters.append(Door(self, position=Coordinates(x, y)))

                    if self.pixel == (255, 255, 1, 255):
                        self.monsters.append(Key(self, position=Coordinates(x, y)))

                    if self.pixel == (0, 255, 0, 255):
                        self.monsters.append(End(self, position=Coordinates(x, y)))

                    if self.pixel == (0, 0, 255, 255):
                        self.player.position = Coordinates(x, y)

    def update(self):
        self.dynamic_layer.clear()
        self.ui_layer.clear()
        self.player.blit()
        self.dialog.blit()

        for monster in self.monsters:
            if monster.position and self.map.is_floor(monster.position):
                monster.blit()
        for firebal in self.firebals:
            if firebal.position and self.map.is_floor(firebal.position):
                firebal.blit()

    def blit_layers(self):
        self.background_layer.blit()
        self.dynamic_layer.blit()
        self.ui_layer.blit()
        pygame.display.update()

    def run(self):
        self.backround_sfx.play(-1)
        while self.running:
            random_number = random.randint(0, 1000)
            if random.randint(0, 1000) == 1:
                self.random_sfx.play()
            if random.randint(0, 10000) == 1:
                self.random_sfx2.play()
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
