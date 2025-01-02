from unittest.mock import patch

import pygame

from shadowkeep.entities.fireballs import FireballLauncher
from shadowkeep.lib.coordinates import Coordinates
from tests._utils.fixtures import (  # noqa: F401
    game,
    mock_image,
    mock_surface,
    pygame_setup,
)
from tests._utils.keys import pressed_keys


def test_player_movement(game):
    initial_pos = game.player.position

    with patch("pygame.key.get_pressed", return_value=pressed_keys(pygame.K_d)):
        game.player.move()

    assert game.player.position.x == initial_pos.x + 1
    assert game.player.position.y == initial_pos.y


def test_static_player_vs_fireball(game):
    """Test that player dies when hit by a fireball while standing still"""
    # Place player at (5, 5)
    game.player.position = Coordinates(5, 5)
    initial_lives = game.player.lives

    # Place a fireball launcher at (5, 3) pointing down
    launcher = FireballLauncher(game, rotation=0, position=Coordinates(5, 3))
    game.entities += [launcher]

    # Run a few turns to let the fireball reach the player
    for _ in range(5):
        game.turn()

    # Player should lose a life
    assert game.player.lives == initial_lives - 1


def test_player_switching_position_with_fireball(game):
    """Test that player dies when moving into a fireball's previous position while
    the fireball moves into player's previous position"""
    game.player.position = Coordinates(5, 5)
    initial_lives = game.player.lives

    launcher = FireballLauncher(game, rotation=0, position=Coordinates(5, 3))
    game.entities += [launcher]

    # Wait for the fireball to get close to the player
    for _ in range(3):
        game.turn()

    # Now the fireball should be at (5, 4)
    # Move the player up into (5, 4) while the fireball moves down to (5, 5)
    with patch("pygame.key.get_pressed", return_value=pressed_keys(pygame.K_w)):
        game.player.move()

    # Player should lose a life
    assert game.player.lives == initial_lives - 1
