import pygame
import grid



#Tiles
WALL = pygame.image.load("Wall.png")
WALL = pygame.transform.scale(WALL, (grid.TILE_WIDTH, grid.TILE_HEIGHT))

FLOOR = pygame.image.load("Wall.png")
FLOOR = pygame.transform.scale(FLOOR, (grid.TILE_WIDTH, grid.TILE_HEIGHT))

SELECTOR = pygame.image.load("Selector.png")
SELECTOR = pygame.transform.scale(SELECTOR, (grid.TILE_WIDTH, grid.TILE_HEIGHT))