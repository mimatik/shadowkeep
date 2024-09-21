import pygame
import math
import map
import grid

pygame.init()

#Size of the window
WINDOW_WIDTH = grid.TILE_WIDTH * 20
WINDOW_HEIGHT = grid.TILE_HEIGHT * 20

#Frames Per Second
FPS = 60

running = True

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()

gridMousePos = grid.GetCoords(pygame.mouse.get_pos())

while running:

    gridMousePos = grid.GetCoords(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((0,0,0))

    window.blit(map.SELECTOR,gridMousePos)

    pygame.display.update()

    clock.tick(FPS)

