from .config import TILE_HEIGHT, TILE_WIDTH

def get_coords(pos):
    return (pos[0] // TILE_WIDTH * TILE_WIDTH, pos[1] // TILE_HEIGHT * TILE_HEIGHT)

def coords_transform_pair(x, y):
    return (x * TILE_WIDTH, y * TILE_HEIGHT)

def coords_transform_single(num, dim = TILE_WIDTH):
    return num * dim