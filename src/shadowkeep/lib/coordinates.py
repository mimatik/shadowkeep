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


# Příklad použití
# coordinates1 = Coordinates(1, 3)
# print(coordinates1.x)  # Vypíše: 1
# print(coordinates1)  # Vypíše: Coordinates(1, 2)
# print(coordinates1[0])  # Vypíše: 1
#
# coordinates3 = Coordinates(1, 2)
# coordinates3 += coordinates1
# print(coordinates3, "    <----")
#
# print(coordinates3.is_neighbour(coordinates1))
#
# # Změna hodnot
# coordinates1.x = 10
# coordinates1[1] = 20
# print(coordinates1)
#
# coordinates1.x = 1
# coordinates1.y = 2
# coordinates2 = Coordinates(3, 4)
# print(coordinates1.pos)
# print(coordinates2.pos)
# print(coordinates1 + coordinates2)  # Vypíše: Coordinates(10, 20)

test1 = Coordinates(2, 2)
test2 = Coordinates(3, 2)
print(test2.is_neighbour(test1))
# # test2 += test1
# # test2 = test2 + test2
# # i = test2
# # print(i[0])
