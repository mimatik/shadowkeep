import pygame
import random
from shadowkeep import config
from shadowkeep.layer import Layer
from shadowkeep.map import Map
from shadowkeep.monster import TalkingMonster, BadMonster, Fireball, FireballLauncher
from shadowkeep.player import Player
from shadowkeep.dialog import Dialog
from shadowkeep.lib.open_ai import ChatGTP


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

        self.map = Map(self)
        self.player = Player(self)
        self.monsters = [TalkingMonster(self) for x in range(7)]
        self.monsters += [BadMonster(self) for x in range(4)]
        self.monsters += [FireballLauncher(self)]
        self.monsters_bin = []
        self.chatGTP = ChatGTP(self)

        self.current_turn = 0

        self.dialog = Dialog(self)

        self.map.blit()

        self.backround_sfx = pygame.mixer.Sound("shadowkeep/backround_music.mp3")
        self.backround_sfx.set_volume(0.2)

        self.random_sfx = pygame.mixer.Sound("shadowkeep/random_sound.mp3")
        self.random_sfx.set_volume(0.1)

        self.random_sfx2 = pygame.mixer.Sound("shadowkeep/random_sound2.mp3")
        self.random_sfx2.set_volume(0.2)

        # print(open_ai_get_response("jak se mas"))

    def turn(self):
        self.current_turn += 1
        for monster in self.monsters[:]:
            monster.turn()

    def update(self):
        self.dynamic_layer.clear()
        self.ui_layer.clear()
        self.player.blit()
        self.dialog.blit()

        for monster in self.monsters:
            if monster.position and self.map.is_floor(monster.position):
                monster.blit()

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
