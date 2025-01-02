import os
from unittest.mock import MagicMock, patch

import pygame
import pytest

from shadowkeep.game import Game
from shadowkeep.lib.coordinates import Coordinates
from shadowkeep.map import Map


@pytest.fixture(autouse=True)
def pygame_setup():
    """Setup pygame in a headless mode for testing"""
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()


@pytest.fixture
def mock_surface():
    """Create a real pygame surface for testing"""
    surface = pygame.Surface((32, 32))
    surface.fill((255, 255, 255))  # Fill with white
    return surface


@pytest.fixture
def mock_image():
    """Mock PIL Image for testing"""
    mock_img = MagicMock()
    mock_img.size = (20, 20)
    mock_img.__enter__.return_value = mock_img
    # Return white pixel (floor tile) instead of black (wall)
    mock_img.getpixel.return_value = (255, 255, 255, 255)
    return mock_img


@pytest.fixture
def game(mock_image, mock_surface):
    """Create a game instance with all necessary mocks for testing"""
    # Mock all potentially problematic components
    with (
        patch("pygame.display.set_mode"),
        patch("PIL.Image.open", return_value=mock_image),
        patch("pygame.image.load", return_value=mock_surface),
        patch("shadowkeep.audio.Audio"),
        patch("shadowkeep.lib.open_ai.ChatGPT"),
        patch("pygame.Surface", return_value=mock_surface),
        patch("pygame.display.update"),
        patch.object(Game, "run"),
        patch.object(Game, "update"),
        patch.object(Game, "blit_layers"),
        # Mock Map.SURFACES to avoid image loading
        patch.object(
            Map, "SURFACES", {Map.FLOOR: mock_surface, Map.WALL: mock_surface}
        ),
    ):
        # Mock entity creation to avoid image loading issues
        with (
            patch("shadowkeep.game.Box"),
            patch("shadowkeep.game.Door"),
            patch("shadowkeep.game.TalkingMonster"),
            patch("shadowkeep.game.BadMonster"),
        ):
            game = Game()
            game.player.position = Coordinates(5, 5)
            # Mock sound to avoid errors
            game.player.player_move_sfx = MagicMock()
            return game
