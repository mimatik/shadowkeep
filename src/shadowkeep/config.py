from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
SRC_DIR = ROOT_DIR / "src"
ASSETS_DIR = SRC_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img"
AUDIO_DIR = ASSETS_DIR / "audio"
KEYS_DIR = ROOT_DIR / "keys"
GENERATED_IMG_DIR = ASSETS_DIR / "generated_img"
DATA_DIR = ROOT_DIR / "data"
LEVELS_DIR = ROOT_DIR / "levels"
SETTINGS_FILE = DATA_DIR / "settings.json"
DATA_FILE = LEVELS_DIR / "data.json"

# Size of a tile note: must be >= 32
TILE_WIDTH = 32
TILE_HEIGHT = 32


# Size of the window
WINDOW_WIDTH = TILE_WIDTH * 23
WINDOW_HEIGHT = TILE_HEIGHT * 23
WINDOW_WIDTH = TILE_WIDTH * 23
WINDOW_HEIGHT = TILE_HEIGHT * 23
# Frames Per Second
FPS = 60

OPENAI_API_KEY = open(KEYS_DIR / "openai_api_key.txt").read().strip()

LOG_FILE = ROOT_DIR / "shadowkeep.log"
