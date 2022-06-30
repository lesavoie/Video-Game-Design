"""
Thayne Peters
File: skeet.py
Original Author: Br. Burton
Designed to be completed by others
This program implements an awesome version of skeet.
"""
import arcade
import math
import random
from random import randint
from abc import ABC
from abc import abstractmethod
# These are Global constants to use throughout the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 3
BULLET_COLOR = arcade.color.BLACK_OLIVE
BULLET_SPEED = 10

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.CARROT_ORANGE
TARGET_SAFE_COLOR = arcade.color.AIR_FORCE_BLUE
TARGET_SAFE_RADIUS = 15

class Point(): # initialize the point to be used throughout this program
    def __init__(self):
        self.x = 0
        self.y = 0

class Velocity(): # initialize the velocity to be used throughout this program
    def __init__(self):
        self.dx = randint(1,2)
        self.dy = randint(-2,2)
        
class FlyingObject(ABC): #parent function of all flying objects
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 0.0
        self.alive = True
    def advance(self):
         # Have the velocity increase
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        # Parent of all flying objects
    @abstractmethod #Only accepts class with draw function
    def draw(self, radius, color, flytype):
        if flytype == 'h': #Hard or strong target
            arcade.draw_circle_outline(self.center.x, self.center.y, radius, color)
            text_x = self.center.x - (radius / 2)
            text_y = self.center.y - (radius / 2)
            arcade.draw_text(repr(self.life), text_x, text_y, color, font_size=20)
        elif flytype == 's': #safe target
            arcade.draw_rectangle_filled(self.center.x, self.center.y, radius, radius, color)
        else: #flytype == 'n' or 'b' being the Normal target or bullet
            arcade.draw_circle_filled(self.center.x, self.center.y, radius, color)
    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        if self.center.x > SCREEN_WIDTH or self.center.y > SCREEN_HEIGHT:
            return True
        
        
class Target(FlyingObject): # Parent of all targets and is child of Flying Object
    def __init__(self):
        super().__init__()
        self.center.x = 0
        self.center.y = randint(SCREEN_HEIGHT/2, SCREEN_HEIGHT)
        self.life = 1
    def draw(self,radius, color, type): # call the Flying object object
        self.advance()
        super().draw(radius, color, type)
    
    
class Safe(Target): # A target that gets hit, disappears, and subtracts 10 points
    def __init__(self):
        super().__init__()
        self.radius = TARGET_SAFE_RADIUS
        self.color = TARGET_SAFE_COLOR
        self.type = 's'
    def draw(self):
        super().draw(self.radius, self.color, self.type)
    def hit(self):
        self.alive = False # target dies when hit
        return -10 # safe target subtracts 10 points when hit
        
    
class Normtarget(Target): # A target that gets hit, disappears, and adds one point
    def __init__(self):
        super().__init__()
        self.radius = TARGET_RADIUS # Globals
        self.color = TARGET_COLOR
        self.type = 'n'
    def draw(self):
        super().draw(self.radius, self.color, self.type)
    def hit(self):
        self.alive = False
        return 1 # normal target earns a point when hit
    
    
class Hardtarget(Target): # A target that gets hit, loses a life, and adds one point,
    def __init__(self):   # repeats for 2 lives, and then disappears after last hit
        super().__init__() # and adds 3 points
        self.radius = TARGET_RADIUS
        self.color = TARGET_COLOR
        self.life = 3         # Each Hard or Strong target can take 3 hits
        self.type = 'h'
        self.velocity.dx = randint(1,1)
        self.velocity.dy = randint(-2,1)
    def draw(self):
        super().draw(self.radius, self.color, self.type)
    def hit(self): # each life of the hard target scores a different point
        self.life -= 1
        if self.life == 2:
            return 1       # first hit earns one point
        elif self.life == 1:
            return 1       # second hit earns one point
        elif self.life == 0:
            self.alive = False
            return 5      # final hit kills the target and adds 5 points
    
    
class Bullet(FlyingObject):
    def __init__(self):
        super().__init__()
        self.type = 'b' # b for bullet
    def draw(self):
        super().draw(BULLET_RADIUS, BULLET_COLOR, self.type) #send radius, color, and its flying object type
    def fire(self, angle):
        self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED # adjust the bullet to match the angle
        self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED # of the mouse and bullet speed
        self.advance()

class Rifle():
    """
    The rifle is a rectangle that tracks the mouse.
    """
    def __init__(self):
        self.center = Point()
        self.center.x = 0
        self.center.y = 0

        self.angle = 45

    def draw(self): # draw the rifle
        arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, self.angle)


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Point
        Velocity
        Bullet
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
 
        self.rifle = Rifle() # create rifle object
        self.score = 0

        self.bullets = [] # create bullet list

        # Creates a list for your targets (similar to the above bullets)
        self.targets = []

        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.rifle.draw()

        for bullet in self.bullets:
            if bullet.alive == True:
                bullet.draw()
            else:
                self.bullets.remove(bullet)

        # TODO: iterate through your targets and draw them...
        for target in self.targets:
            if target.alive == True:
                target.draw()
            else:               # if a target dies, remove it
                self.targets.remove(target)

        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()

        # decide if we should start a target
        if random.randint(1, 50) == 1:
            self.create_target()

        for bullet in self.bullets:
            bullet.advance()

        # TODO: Iterate through your targets and tell them to advance
        for target in self.targets:
            target.advance()

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """
        targets = Target()
        ranlist = []
        ranlist.append(Hardtarget())
        ranlist.append(Safe())
        ranlist.append(Normtarget())
        ranTarg = ranlist[randint(0,2)]


        self.targets.append(ranTarg)
        # TODO: Decide what type of target to create and append it to the list

    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        self.score += target.hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.is_off_screen:
                self.bullets.remove(bullet)
                

        if Target.is_off_screen == True:
            self.targets.remove(target)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.targets.remove(target)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle = self._get_angle_degrees(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!
        angle = self._get_angle_degrees(x, y)

        bullet = Bullet()
        bullet.fire(angle)

        self.bullets.append(bullet)

    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.
        Note: This could be a static method, but we haven't
        discussed them yet...
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()