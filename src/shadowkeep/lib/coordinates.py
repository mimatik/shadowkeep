class Coordinates(list):
    def __new__(cls, x=0, y=0):
        return super().__new__(cls, (x, y))

    def __int__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x, y)

    @property
    def x(self):
        return self.x

    @property
    def y(self):
        return self.y

    # def coords(self):

coordinates1 = Coordinates(x=2, y=4)
print(coordinates1.x())
