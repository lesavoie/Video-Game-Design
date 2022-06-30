from Point import Point      # Import everything the Ball needs
from Velocity import Velocity
from Global import Global
import arcade
from random import randint
import math

class Ball(Global):
    def __init__(self):
        super().__init__() # call the parent class
        self.center = Point()
        self.velocity = Velocity()
        self.restart()
    def draw(self): #create ball
        arcade.draw_circle_filled(self.center.x, self.center.y, self.BALL_RADIUS, arcade.color.RED)
    def advance(self): # Have the velocity increase
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
    def bounce_horizontal(self): #bounce off left wall
        if self.center.x != (self.SCREEN_WIDTH - 2*self.BALL_RADIUS):
           self.velocity.dx = -self.velocity.dx
    def bounce_vertical(self): #bounce off top wall
        if self.center.y != (self.SCREEN_HEIGHT - 2*self.BALL_RADIUS):
            self.velocity.dy = -self.velocity.dy
    def restart(self): #Reset after ball scores. Random position on the left
        self.center.x = 0# side of the screen and random velocities
        self.center.y = randint(20, self.SCREEN_HEIGHT-20)
        self.velocity.dx = randint(1 , 10) 
        self.velocity.dy = randint(1 , 10)