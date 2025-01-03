from shadowkeep.config import TILE_HEIGHT, TILE_WIDTH


class Coordinates(list):
    def __init__(self, x=0, y=0):
        super().__init__([x, y])

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    def __add__(self, other):
        return Coordinates(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __str__(self):
        return f"Coordinates({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def is_neighbour(self, other):
        return (
            abs(self.x - other.x) == 1
            and self.y == other.y
            or self.x == other.x
            and abs(self.y - other.y) == 1
        )

    def transformed_pair(self):
        return self.x * TILE_WIDTH, self.y * TILE_HEIGHT

    def copy(self):
        return Coordinates(self.x, self.y)
