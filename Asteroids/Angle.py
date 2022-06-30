import math

class Angle():
    def __init__(self):
        self.a = 0
    @property
    def a(self):
        return self._a

    @a.setter # prevent the angle from getting larger than 360
    def a(self, a):
        self._a = a % 360
        