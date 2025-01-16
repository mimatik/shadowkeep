from pathlib import Path
from PIL import Image

ROOT_DIR = Path(__file__).parent.parent.parent
SRC_DIR = ROOT_DIR / "src"
ASSETS_DIR = SRC_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img"
AUDIO_DIR = ASSETS_DIR / "audio"
KEYS_DIR = ROOT_DIR / "keys"
GENERATED_IMG_DIR = ASSETS_DIR / "generated_img"

# Size of a tile note: must be >= 32
TILE_WIDTH = 32
TILE_HEIGHT = 32

# Size of the window
with Image.open(IMG_DIR / "map.png") as image:
    WINDOW_WIDTH = image.width * TILE_WIDTH
    WINDOW_HEIGHT = image.height * TILE_HEIGHT

# Frames Per Second
FPS = 60

OPENAI_API_KEY = open(KEYS_DIR / "openai_api_key.txt").read().strip()

LOG_FILE = ROOT_DIR / "shadowkeep.log"
