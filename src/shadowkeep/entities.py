import itertools


class Entities(list):
    @property
    def solid(self):
        return [entity for entity in self if entity.solid]

    @property
    def non_solid(self):
        return [entity for entity in self if entity.non_solid]

    def on_position(self, position):
        return [entity for entity in self if entity.position == position]
