import pygame
import map
import grid
import player

pygame.init()

PLAYER_X = player.player_x
PLAYER_Y = player.player_y

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

    PLAYER_X, PLAYER_Y = player.Player_move(PLAYER_X, PLAYER_Y)

    window.fill((0,0,0))

    window.blit(map.SELECTOR,gridMousePos)

    window.blit(player.player, (PLAYER_X, PLAYER_Y))

    pygame.display.update()

    clock.tick(FPS)

