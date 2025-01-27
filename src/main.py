import logging
import logging.config

from shadowkeep.config import LOG_FILE
from shadowkeep.game import Game

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "file_shadowkeep": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(LOG_FILE),
                "maxBytes": 10,
            },
        },
        "loggers": {
            "shadowkeep": {
                "level": "DEBUG",
                "handlers": (["file_shadowkeep"] + ["console"]),
                "propagate": False,
            },
        },
    }
)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
