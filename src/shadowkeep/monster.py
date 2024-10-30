import random
import pygame

from shadowkeep.config import TILE_HEIGHT, TILE_WIDTH
from shadowkeep.lib.coordinates import Coordinates
from shadowkeep.config import IMG_DIR


class Entity:
    def __init__(self, game, position=None, velocity=Coordinates(0, 0), rotation=0):
        self.rotation = rotation
        self.game = game
        self.surface = pygame.surface.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.surface = pygame.image.load(IMG_DIR / self.get_image())
        self.velocity = velocity
        self.position = position
        self.surface = pygame.transform.rotate(self.surface, self.rotation)

    def get_image(self):
        raise NotImplementedError

    def choose_random_position(self):
        while True:
            position = Coordinates(random.randint(5, 24), random.randint(5, 24))
            if self.game.map.is_floor(position):
                self.position = position
                return

    def meet_player(self):
        pass

    def blit(self):
        self.game.dynamic_layer.place_surface(
            self.surface, self.position.transformed_pair()
        )

    def destroy(self):
        self.game.monsters.remove(self)


class Monster(Entity):

    def __init__(self, game):
        super().__init__(game)
        self.choose_random_position()
        self.choose_random_velocity()

    def turn(self):
        if random.random() < 0.25:
            self.choose_random_velocity()
        self.move()

    def choose_random_velocity(self):
        self.velocity = random.choice(
            [Coordinates(x=-1), Coordinates(x=+1), Coordinates(y=-1), Coordinates(y=+1)]
        )

    def choose_initial_velocity(self):
        self.choose_random_velocity()

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


class TalkingMonster(Monster):

    def get_image(self):
        return "Friend.png"

    def meet_player(self):
        self.game.dialog.is_open = True


class BadMonster(Monster):
    def get_image(self):
        return "Enemy.png"

    def meet_player(self):
        self.game.running = False


class Fireball(Entity):

    def get_image(self):
        return "Fireball.png"

    # def __init__(self, game):
    #     super().__init__()
    #     self.velocity = Coordinates(0, 1)
    #     self.position = Coordinates(2, 2)

    def turn(self):
        self.position += self.velocity
        if not self.game.map.is_floor(self.position):
            self.destroy()

        elif self.position == self.game.player.position:
            self.game.running = False


class FireballLauncher(Entity):
    def __init__(self, game, rotation=0, position=Coordinates(0, 0)):
        super().__init__(game, rotation=rotation)
        self.position = position
        self.get_direction()

    def get_direction(self):
        if self.rotation == 0:
            self.direction = Coordinates(0, 1)
        elif self.rotation == 90:
            self.direction = Coordinates(1, 0)
        elif self.rotation == 180:
            self.direction = Coordinates(0, -1)
        elif self.rotation == 270:
            self.direction = Coordinates(-1, 0)
        else:
            return Coordinates(0, 0)

    def get_image(self):
        return "Fireball_launcher.png"

    def turn(self):
        if self.game.current_turn % 3 == 0:
            self.game.monsters += [
                Fireball(
                    self.game,
                    position=self.position + self.direction,
                    velocity=self.direction,
                    rotation=self.rotation,
                )
            ]
