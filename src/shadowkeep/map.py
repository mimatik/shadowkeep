import pygame
from PIL import Image

from shadowkeep.config import IMG_DIR, TILE_HEIGHT, TILE_WIDTH


class Map:
    FLOOR = 0
    WALL = 1
    SURFACES = {
        FLOOR: pygame.image.load(IMG_DIR / "Floor.png"),
        WALL: pygame.image.load(IMG_DIR / "Wall.png"),
    }

    def __init__(self, game):
        self.game = game
        self.data = []
        self.load_map_from_image()

    def load_map_from_image(self):
        with Image.open(IMG_DIR / "map.png") as image:
            self.width, self.height = image.size

            for h in range(self.height):
                row = []
                for w in range(self.width):
                    self.pixel = image.getpixel((w, h))
                    if self.pixel == (0, 0, 0, 255):
                        row.append(self.WALL)
                    elif self.pixel == (255, 255, 255, 255):
                        row.append(self.FLOOR)
                    elif self.pixel == (255, 0, 0, 255):
                        row.append(self.FLOOR)

                self.data.append(row)

    def blit(self):
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                self.game.background_layer.place_surface(
                    self.SURFACES[cell], (x * TILE_WIDTH, y * TILE_HEIGHT)
                )

    def is_floor(self, coordinates):
        try:
            return self.data[coordinates.y][coordinates.x] == self.FLOOR
        except IndexError:
            return False


# Tiles
# WALL = pygame.image.load(IMG_DIR / "Wall.png")
# WALL = pygame.transform.scale(wall, (TILE_WIDTH, TILE_HEIGHT))
#
# FLOOR = pygame.image.load(IMG_DIR / "Floor.png")
# FLOOR = pygame.transform.scale(FLOOR, (TILE_WIDTH, TILE_HEIGHT))

SELECTOR = pygame.image.load(IMG_DIR / "Selector.png")
SELECTOR = pygame.transform.scale(SELECTOR, (TILE_WIDTH, TILE_HEIGHT))
