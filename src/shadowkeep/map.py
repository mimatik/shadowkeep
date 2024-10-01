import pygame
from pygame.examples.cursors import image
from shadowkeep import grid
from shadowkeep.config import IMG_DIR, TILE_HEIGHT, TILE_WIDTH
from PIL import Image

class Map:
    def __init__(self, window):

        self.image = Image.open(IMG_DIR / "map.png")
        self.width, self.height = self.image.size
        print(self.image.size)
        self.data = []

        for h in range(self.height):
            self.row = []
            for w in range(self.width):
                self.pixel = self.image.getpixel((w ,h))
                if self.pixel == (0, 0, 0, 255):
                    self.row.append(1)
                else:
                    self.row.append(0)
            self.data.append(self.row)

        print(self.data)

        self.wall = pygame.image.load(IMG_DIR / "Wall.png")
        self.floor = pygame.image.load(IMG_DIR / "Floor.png")
        self.window = window


    def blit(self):
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                if cell == 1:
                    self.window.blit(self.wall, (x * TILE_WIDTH, y * TILE_HEIGHT))
                elif cell == 0:
                    self.window.blit(self.floor, (x * TILE_WIDTH, y * TILE_HEIGHT))


# Tiles
# WALL = pygame.image.load(IMG_DIR / "Wall.png")
# WALL = pygame.transform.scale(wall, (TILE_WIDTH, TILE_HEIGHT))
# 
# FLOOR = pygame.image.load(IMG_DIR / "Floor.png")
# FLOOR = pygame.transform.scale(FLOOR, (TILE_WIDTH, TILE_HEIGHT))

SELECTOR = pygame.image.load(IMG_DIR / "Selector.png")
SELECTOR = pygame.transform.scale(SELECTOR, (TILE_WIDTH, TILE_HEIGHT))
