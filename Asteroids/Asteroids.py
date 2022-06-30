from Global import *
from abc import ABC
from abc import abstractmethod
from flyingObject import flyingObject
from random import randint


class Asteroids(flyingObject, ABC):
    def __init__(self):
        super().__init__()
        self.type = ""
    @abstractmethod # only accept the draw functions with an image in it
    def draw(self, image):
        super().draw(image)
    @abstractmethod
    def advance(self):
        super().advance()
        
class largeAsteroid(Asteroids):
    def __init__(self):
        super().__init__()
        self.type = 'large' # identifies this asteroid as a large
        self.center.x = randint(0, SCREEN_WIDTH)
        self.center.y = randint(0, SCREEN_HEIGHT)
        random_num_not_0 = [-2,-1,1,2] # list of valid velocities
        self.radius = BIG_ROCK_RADIUS
        self.spin = BIG_ROCK_SPIN
        self.velocity.dx = random_num_not_0[randint(0, 3)] # Make a variety of fast
        self.velocity.dy = random_num_not_0[randint(0, 3)]# and slow large asteroids
    
    def draw(self):
        image = "images/meteorGrey_big1.png"
        super().draw(image)
    
    def advance(self):
        super().advance()
        
class midAsteroid(Asteroids):
    def __init__(self, previous_asteroid_info): # Pass the daddy asteroid info to
        super().__init__()                    # the new baby asteroids
        self.type = 'medium'
        self.center.x = previous_asteroid_info.center.x #Daddy asteroid center
        self.center.y = previous_asteroid_info.center.y
        self.radius = MEDIUM_ROCK_RADIUS
        self.spin = MEDIUM_ROCK_SPIN
        self.velocity.dx = -previous_asteroid_info.velocity.dx # Daddy asteroid velocity
        self.velocity.dy = previous_asteroid_info.velocity.dy
    def draw(self):
        image = "images/meteorGrey_med1.png"
        super().draw(image)
    
    def advance(self):
        super().advance()
        
class smallAsteroid(Asteroids):
    def __init__(self, previous_asteroid_info):
        super().__init__()
        self.type = 'small'
        self.center.x = previous_asteroid_info.center.x
        self.center.y = previous_asteroid_info.center.y
        self.velocity.dx = previous_asteroid_info.velocity.dx
        self.velocity.dy = -previous_asteroid_info.velocity.dy
        self.radius = SMALL_ROCK_RADIUS
        self.spin = SMALL_ROCK_SPIN
    
    def draw(self):
        image = "images/meteorGrey_small1.png"
        super().draw(image)
    
    def advance(self):
        super().advance()