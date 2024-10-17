from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
SRC_DIR = ROOT_DIR / "src"
ASSETS_DIR = SRC_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img"
KEYS_DIR = ROOT_DIR / "keys"

# Size of a tile note: must be >= 32
TILE_WIDTH = 32
TILE_HEIGHT = 32

# Size of the window
WINDOW_WIDTH = TILE_WIDTH * 24
WINDOW_HEIGHT = TILE_HEIGHT * 24

# Frames Per Second
FPS = 60

OPENAI_API_KEY =open(KEYS_DIR / "openai_api_key.txt").read()
