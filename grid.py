
#Size of a tile note: must be >= 32
TILE_WIDTH = 32
TILE_HEIGHT = 32

def GetCoords(pos):
    return (pos[0] // TILE_WIDTH * TILE_WIDTH, pos[1] // TILE_HEIGHT * TILE_HEIGHT)