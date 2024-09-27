import pygame
from shadowkeep import grid
from shadowkeep.config import IMG_DIR, TILE_HEIGHT, TILE_WIDTH


class Map:
    def __init__(self, window):
        self.data = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
        ]
        self.surface_1 = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.surface_1.fill((255, 0, 255))
        self.surface_2 = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.surface_2.fill((0, 0, 255))
        self.window = window

    def blit(self):
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                if cell == 1:
                    self.window.blit(self.surface_1, (x * TILE_WIDTH, y * TILE_HEIGHT))
                elif cell == 0:
                    self.window.blit(self.surface_2, (x * TILE_WIDTH, y * TILE_HEIGHT))


# Tiles
WALL = pygame.image.load(IMG_DIR / "Wall.png")
WALL = pygame.transform.scale(WALL, (TILE_WIDTH, TILE_HEIGHT))

FLOOR = pygame.image.load(IMG_DIR / "Floor.png")
FLOOR = pygame.transform.scale(FLOOR, (TILE_WIDTH, TILE_HEIGHT))

SELECTOR = pygame.image.load(IMG_DIR / "Selector.png")
SELECTOR = pygame.transform.scale(SELECTOR, (TILE_WIDTH, TILE_HEIGHT))
