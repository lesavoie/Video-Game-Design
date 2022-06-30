from Global import *
from flyingObject import flyingObject
from random import randint
import math

class Ship(flyingObject):
    def __init__(self):
        super().__init__()
        self.velocity.dy = 0
        self.velocity.dx = 0
        self.center.x = SCREEN_WIDTH // 2 # start in the middle of the screen
        self.center.y = SCREEN_HEIGHT // 2
        self.angle.a = 0
        self.radius = SHIP_RADIUS
        self.lives = SHIP_LIVES # BONUS
    
    def draw(self):
        image = "images/playerShip1_orange.png" #images/Poooooooooop.png"
        super().draw(image)
    
    def advance(self):
        super().advance()
