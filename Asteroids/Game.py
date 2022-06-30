"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
import arcade
from Ship import Ship
from Bullets import Bullets
from Asteroids import *
import math
from random import randint
from Global import *

# These are Global constants to use throughout the game



class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()
        
        self.ship = Ship()
        self.asteroids = []
        self.bullets = []
        self.bull_life = 0
        self.score = 0
        self.start = 0
        self.lose_a_life = False
        self.lost_lives = 0
        self.bull_life = BULLET_LIFE
        self.clock = 0
        self.clock_on = True
        self.total = 0
        self.gameOver = False
        # TODO: declare anything here you need the game class to track

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()
        # TODO: draw each object
        if self.gameOver == True: # Only display Game over window when gameOver conditions are true
            self.game_over()
        if self.ship.alive == True: # Only draw the ship if alive
            self.ship.draw()
            if self.lose_a_life == True: # Lose a life
                self.ship.lives -= 1
                self.lost_lives += 1
                self.ship.center.x = SCREEN_WIDTH /2
                self.ship.center.y = SCREEN_HEIGHT /2 # reset new ship with one less life
                self.ship.velocity.dx = 0
                self.ship.velocity.dy = 0
                self.lose_a_life = False
                if self.ship.lives < 1 : # if all lives are lost, no more ships
                   self.ship.alive = False
                   self.gameOver = True # gameOver conditions are now true
        else:
            self.clock_on = False # count how many times the frame changes (this will help with the score tally)
            self.play_again() # display the play again window and show the total score (different than the normal score)
            self.total_score()
        
        if self.start < INITIAL_ROCK_COUNT: # Draw 5 large asteroids
            self.asteroids.append(largeAsteroid())
            self.start += 1
            
        for a in self.asteroids: # draw the asteroids
            if a.alive == True:
                a.draw()
                a.angle.a += a.spin
            else:
                self.asteroids.remove(a)
        
        for bullet in self.bullets: # draw the bullets when added to the bullets list
            if bullet.alive == True:
                bullet.draw()
                
            else:
                self.bullets.remove(bullet)
        self.draw_lives_and_score()
        
        if len(self.asteroids) == 0: # When all asteroids are destroid, the game is won
            self.clock_on = False
            self.play_again() # ask if the user wants to play again
            self.total_score() # display the total score
            
            if randint(1, 10) == 1: # shoot fireworks at random positions
                self.firework(randint(20,SCREEN_WIDTH), randint(20, SCREEN_HEIGHT))
                
                
    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        if self.clock_on == True: # count the frames
            self.clock += 1
        self.check_keys()
        # TODO: Tell everything to advance or move forward one step in time
        for a in self.asteroids: # advance the asteroids each frame
            a.advance()
        if self.ship.alive == True: # adance the ship
            self.ship.advance()
        self.check_wrap_around()
        for bullet in self.bullets: # advance the bullets for 60 frames
            bullet.advance()
            bullet.life +=1
            if bullet.life == self.bull_life:
                bullet.alive = False
        # TODO: Check for collisions
        self.check_collisions()
        
    def firework(self, midx, midy): # One firework
        self.ship.alive = False # kill the ship
        rockets = randint(15, 45)
        if len(self.bullets) > 0: # use the bullets as firework makings
            for bullet in self.bullets:
                self.bullets.remove(bullet)
        fire_angle = 0
        while len(self.bullets) < rockets:   # each firework is different 
            self.bullets.append(Bullets(self.ship))            
            for bullet in self.bullets: # change the normal bullet behavior to fit the firework behavior
                self.bull_life = 45
                self.ship.center.x = midx
                self.ship.center.y = midy
                self.ship.angle.a = fire_angle
                fire_angle += (360 / rockets)
                self.ship.velocity.dx = -5
                self.ship.velocity.dy = -5
        for bullet in self.bullets:
                bullet.draw()
        

    def play_again(self): # prompt user to reset the board and play again
        score_text = "Press R to Play Again."
        start_x = SCREEN_WIDTH/5
        start_y = SCREEN_HEIGHT/2
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=25, color=arcade.color.WHITE
                        )
        
    def total_score(self): # self.clock//50 is about 1 second
        self.total = self.score*10 - (2 * self.clock//50) - (self.lost_lives*100)  # total score is determined by the number of 
        if self.total <= 0:                                                       # asteroids you hit, time it took you, and lives lost
            self.total = 0
        text = "Your Score: {}".format(self.total)
        start_x = SCREEN_WIDTH/5
        start_y = SCREEN_HEIGHT/1.5
        arcade.draw_text(text, start_x=start_x, start_y=start_y, font_size=25, color=arcade.color.WHITE
                        )
        self.total = 0
    
    def game_over(self): # Display the game over board
        text = "GAME OVER".format(self.total)
        start_x = SCREEN_WIDTH/6
        start_y = SCREEN_HEIGHT/1.2
        arcade.draw_text(text, start_x=start_x, start_y=start_y, font_size=50, color=arcade.color.WHITE
                        )
        
    def draw_lives_and_score(self): # This keeps track of your score and lives through out the game
        """
        Puts the current score on the screen
        """
        score_text = "Lives: {}        Score: {}".format(self.ship.lives, self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE
                        )

    def check_collisions(self):
        for a in self.asteroids:               # If the asteroid gets too close to the ship, take a life from the ship
            sa_too_close = self.ship.radius + a.radius # sa = Ship, asteroid
            if (abs(self.ship.center.x - a.center.x) <= sa_too_close) and (abs(self.ship.center.y - a.center.y) <= sa_too_close):
                    if self.ship.center.y <= a.center.y:
                        self.lose_a_life = True
                        a.center.x += a.velocity.dx*30 # Jump over the ship after colliding
                        a.center.y += a.velocity.dy*30# to prevent too many lost lives
            for bullet in self.bullets: # If the asteroid gets too close to a bullet, remove bullet and asteroid
                if bullet.alive and a.alive:
                    ba_too_close = bullet.radius + a.radius 
                    if (abs(bullet.center.x - a.center.x) <= ba_too_close) and (abs(bullet.center.y - a.center.y) <= ba_too_close):
                        bullet.alive = False
                        if a.type == 'large': # If a large asteroid gets hit, make 2 mid asteroids and a small one and add a point to the score
                            self.score += 1
                            a.velocity.dy = 2
                            self.asteroids.append(midAsteroid(a))
                            a.velocity.dy = -2
                            self.asteroids.append(midAsteroid(a))
                            a.velocity.dx = 5
                            self.asteroids.append(smallAsteroid(a))
                        elif a.type == 'medium': # If a medium asteroid gets hit, make 2 small asteroids, and add 3 points to the score
                            self.score += 3
                            a.velocity.dy = 1.5
                            a.velocity.dx = 1.5
                            self.asteroids.append(smallAsteroid(a))
                            a.velocity.dy = -1.5
                            a.velocity.dx = -1.5
                            self.asteroids.append(smallAsteroid(a))
                        elif a.type == 'small': # If a small asteroid gets hit, just change the score
                            self.score += 5 
                        a.alive = False # Now remove the asteroid hit
                        
    def check_wrap_around(self): # wrap all objects around the screen
        for asteroid in self.asteroids:
            self.wrap(asteroid)
        for bullet in self.bullets:
            self.wrap(bullet)
        self.wrap(self.ship)
        
    def wrap(self,obj):
            if obj.center.y >= SCREEN_HEIGHT+1:
                obj.center.y = 0
            if obj.center.y <= -1:
                obj.center.y = SCREEN_HEIGHT
            if obj.center.x >= SCREEN_WIDTH+1:
                obj.center.x = 0
            if obj.center.x <= -1:
                obj.center.x = SCREEN_WIDTH
        
    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys: # turn to the left
            self.ship.angle.a += 3
        
        if arcade.key.RIGHT in self.held_keys: # turn to the right
            self.ship.angle.a -= 3

        if arcade.key.UP in self.held_keys: # Dont accelorate, just have a steady velocity (helps the ship remain in control)
            self.ship.velocity.dy = math.cos(math.radians(self.ship.angle.a)) * 3
            self.ship.velocity.dx = -math.sin(math.radians(self.ship.angle.a)) * 3
       
        if arcade.key.DOWN in self.held_keys: # Back up ship
            self.ship.velocity.dy = -math.cos(math.radians(self.ship.angle.a)) * 3
            self.ship.velocity.dx = math.sin(math.radians(self.ship.angle.a)) * 3

        # Machine gun mode...
        if arcade.key.F in self.held_keys:
            if self.ship.alive:
                self.bullets.append(Bullets(self.ship))


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        
        self.held_keys.add(key)
        if self.ship.alive:
            if key == arcade.key.SPACE: # Fire a bullet by appending it to the bullets list
                # TODO: Fire the bullet here!
                self.bullets.append(Bullets(self.ship))
        self.held_keys.add(key)

        if self.ship.alive == False: #Only be able to reset when the ship is dead
            if key == arcade.key.R: # Reset the screen from the fireworks
                self.ship.lives = SHIP_LIVES # Reset the ship's lives 
                self.ship.center.x = SCREEN_WIDTH/2 # Reset the ship's position
                self.ship.center.y = SCREEN_HEIGHT/2
                self.ship.alive = True # Redraw the ship
                self.score = 0 # Reset the score
                while len(self.asteroids) > 0: # Clear the board of all asteroids
                    for a in self.asteroids:
                        self.asteroids.remove(a)
                for i in range(0,5): # Draw the new 5 asteroids
                    self.asteroids.append(largeAsteroid())
                self.bull_life = BULLET_LIFE  # Reset the bullet life
                self.ship.angle.a = 0 # Reset the ship
                self.ship.velocity.dx = 0
                self.ship.velocity.dy = 0
                self.total = 0
                self.lost_lives = 0
                self.gameOver = False
                for bullet in self.bullets: # clear the board of all firework bullets
                    bullet.alive = False
                self.clock_on = True
                self.clock = 0

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()
