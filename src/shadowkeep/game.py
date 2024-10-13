import pygame
from shadowkeep import config
from shadowkeep.layer import Layer
from shadowkeep.map import Map
from shadowkeep.monster import Monster
from shadowkeep.player import Player
from shadowkeep.text import TextInput


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
        self.monsters = [Monster(self) for x in range(10)]

        self.text_input = TextInput(self)

        self.map.blit()

    def turn(self):
        for monster in self.monsters:
            monster.turn()

    def update(self):
        self.dynamic_layer.clear()
        self.ui_layer.clear()
        self.player.blit()
        self.text_input.blit()

        for monster in self.monsters:
            monster.blit()

    def blit_layers(self):
        self.background_layer.blit()
        self.dynamic_layer.blit()
        self.ui_layer.blit()
        pygame.display.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.text_input.is_open:
                        self.text_input.read_key(event)
                    else:
                        self.player.move()

            self.update()
            self.blit_layers()
            self.clock.tick(config.FPS)
