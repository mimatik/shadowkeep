import itertools


class Entities:
    def __init__(self, game):
        self.game = game
        self.solid = {}
        self.non_solid = {}

    def __getitem__(self, key):
        return (self.solid[key], self.non_solid[key])

    def get_solid(self, key):
        return self.solid[key]

    def get_non_solid(self, key):
        return self.non_solid[key]

    def __setitem__(self, key, value):
        if value.solid:
            self.solid[value.position] = value

        elif value.non_solid:
            self.non_solid[value.position] = value

    def __iter__(self):
        return itertools.chain(self.solid.values(), self.non_solid.values())
