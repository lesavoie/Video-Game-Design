class Global(): # This makes it easy to call children classes. 
    def __init__(self):
        self.SCREEN_WIDTH = 400
        self.SCREEN_HEIGHT = 300
        self.BALL_RADIUS = 10

        self.PADDLE_WIDTH = 10
        self.PADDLE_HEIGHT = 50
        self.MOVE_AMOUNT = 5

        self.SCORE_HIT = 1
        self.SCORE_MISS = 5