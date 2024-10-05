class Coordinates(tuple):
    def __new__(cls, x=0, y=0):
        return super().__new__(cls, (x, y))

    def __init__(self):
        return

    def __add__(self, other):
        return

    @property
    def x(self):
        return

    @property
    def y(self):
        return
