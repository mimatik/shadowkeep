from shadowkeep.config import TILE_HEIGHT, TILE_WIDTH


def GetCoords(pos):
    return (pos[0] // TILE_WIDTH * TILE_WIDTH, pos[1] // TILE_HEIGHT * TILE_HEIGHT)
