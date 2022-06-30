from Velocity import Velocity
from Angle import Angle
from Point import Point
from Global import *
from abc import ABC
from abc import abstractmethod
import arcade

class flyingObject(ABC):
    def __init__(self):
        self.center = Point() #flyingObject has a Point, Velocity, and an Angle
        self.velocity = Velocity()
        self.angle = Angle()
        self.radius = 0
        self.spin = 0
        self.alive = True
    @abstractmethod # Only accept the draws that carry an image with them
    def draw(self, image):
        img = image
        texture = arcade.load_texture(img)
        width = texture.width
        height = texture.height
        alpha = 1 # For transparency, 1 means not transparent
        x = self.center.x
        y = self.center.y
        angle = self.angle.a

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
    def advance(self): # Advance function
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy