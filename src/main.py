import pygame
from shadowkeep import config, grid
from shadowkeep.map import Map
from shadowkeep.player import Player

pygame.init()


running = True

window = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()

map = Map(window)

player = Player(window, map)

gridMousePos = grid.get_coords(pygame.mouse.get_pos())
while running:

    gridMousePos = grid.get_coords(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            player.move()

    map.blit()

    # window.blit(map.SELECTOR,gridMousePos)

    player.blit()

    pygame.display.update()

    clock.tick(config.FPS)
