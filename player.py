import pygame
import grid

player_x = grid.TILE_HEIGHT * 10
player_y = grid.TILE_WIDTH * 10
PLAYER_HEIGHT = grid.TILE_HEIGHT
PLAYER_WIDTH = grid.TILE_WIDTH
player = pygame.surface.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
player.fill((255, 250, 250))
def Player_move(player_x, player_y):
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_w]:
        player_y -= grid.TILE_HEIGHT
    if pressed_keys[pygame.K_s]:
        player_y += grid.TILE_HEIGHT
    if pressed_keys[pygame.K_d]:
        player_x += grid.TILE_WIDTH
    if pressed_keys[pygame.K_a]:
        player_x -= grid.TILE_WIDTH
    return player_x, player_y

