import pygame
from shadowkeep.map import Map
from shadowkeep.player import Player
from shadowkeep import config
from shadowkeep.monster import Monster
from shadowkeep.layer import Layer


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Platformer")
        self.window = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.running = True

        self.map = Map(self)
        self.player = Player(self)
        self.monsters = [Monster(self)]

        self.background_layer = Layer(self, is_static=True)
        self.dynamic_layer = Layer(self)

        self.map.blit(self.background_layer)

    def turn(self):
        for monster in self.monsters:
            monster.turn()

    def update(self):
        self.dynamic_layer.clear()
        self.player.blit(self.dynamic_layer)

        for monster in self.monsters:
            monster.blit(self.dynamic_layer)

    def draw(self):
        self.background_layer.draw(self.window)
        self.dynamic_layer.draw(self.window)
        pygame.display.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.player.move()
            self.update()
            self.draw()
            self.clock.tick(config.FPS)
