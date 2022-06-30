from Global import *
from flyingObject import flyingObject
import math

class Bullets(flyingObject):
    def __init__(self, ship):
        super().__init__()
        self.speedx = BULLET_SPEED + ship.velocity.dx # add the bullet's normal speed with
        self.speedy = BULLET_SPEED + ship.velocity.dy # the ship's speed
        self.velocity.dx = -math.sin(math.radians(ship.angle.a)) * self.speedx # as well as
        self.velocity.dy = math.cos(math.radians(ship.angle.a)) * self.speedy # the angle of the ship
        self.center.x = ship.center.x # Fire from the ship's current location
        self.center.y = ship.center.y
        self.radius = BULLET_RADIUS
        self.life = 0
        self.angle.a = ship.angle.a + 90
        
    def draw(self):
        image = "images/laserBlue01.png"#"images/Poooooooooop.png"
        super().draw(image)