import random
import pygame
from shadowkeep.config import TILE_HEIGHT, TILE_WIDTH
from shadowkeep.lib.coordinates import Coordinates
from shadowkeep.config import IMG_DIR


class Entity:
    def __init__(self, game):
        self.game = game
        self.surface = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.surface = pygame.image.load(IMG_DIR / self.get_image())
        self.choose_random_velocity()
        self.choose_random_position()

    def get_image(self):
        raise NotImplementedError

    def choose_random_position(self):
        while True:
            position = Coordinates(random.randint(5, 24), random.randint(5, 24))
            if self.game.map.is_floor(position):
                self.position = position
                return

    def choose_random_velocity(self):
        self.velocity = random.choice(
            [Coordinates(x=-1), Coordinates(x=+1), Coordinates(y=-1), Coordinates(y=+1)]
        )

    def move(self):
        next_position = self.position + self.velocity

        if (
            self.game.map.is_floor(next_position)
            and not any(
                other_monster.position == next_position
                for other_monster in self.game.monsters
                # if other_monster != self
            )
            and next_position != self.game.player.position
        ):
            self.position = next_position
        else:
            self.choose_random_velocity()

        if (
            self.position.is_neighbour(self.game.player.position)
            or self.position == self.game.player.position
        ):
            self.meet_player()

    def meet_player(self):
        raise NotImplementedError

    def blit(self):
        self.game.dynamic_layer.place_surface(
            self.surface, self.position.transformed_pair()
        )

    def turn(self):
        if random.random() < 0.25:
            self.choose_random_velocity()
        self.move()
class TalkingMonster(Entity):
    def get_image(self):
        return "Friend.png"

    def meet_player(self):
        self.game.dialog.is_open = True

class BadMonster(Entity):
    def get_image(self):
        return "Enemy.png"

    def meet_player(self):
        self.game.running = False
