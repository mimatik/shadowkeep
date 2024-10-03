import pygame
from shadowkeep.map import Map
from shadowkeep.player import Player
from shadowkeep import config


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

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.player.move()
            self.blit()
            self.clock.tick(config.FPS)

    def blit(self):
        self.map.blit()
        self.player.blit()
        pygame.display.update()
