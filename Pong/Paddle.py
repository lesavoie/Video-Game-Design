from Global import Global
from Point import Point
import arcade
import math

class Paddle(Global):
    def __init__(self):
        super().__init__()
        self.center = Point()
        self.center.x = self.SCREEN_WIDTH # Set the initial paddle posistion in the center on the right
        self.center.y = self.SCREEN_HEIGHT/2 
    def draw(self): #Create paddle
        arcade.draw_rectangle_filled(self.center.x, self.center.y, self.PADDLE_WIDTH, self.PADDLE_HEIGHT, arcade.color.BLUE)
    def move_up(self):
        if self.center.y != (self.SCREEN_HEIGHT - self.PADDLE_HEIGHT/2): # dont cross the top border
            self.center.y += self.MOVE_AMOUNT
    def move_down(self):
        if self.center.y != (self.PADDLE_HEIGHT/2):  #dont cross the bottom border
            self.center.y -= self.MOVE_AMOUNT