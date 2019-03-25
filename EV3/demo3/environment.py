# reference to structure on:
# https://github.com/mahbubiftekhar/RoboTour/blob/master/EV3/environment.py

class Environment():
    def __init__(self):
        self.line_threshold = 20
        self.corner_color = "red"
        self.moving_speed_normal = 500
        self.moving_speed_slow = 250
        self.rotation_speed_normal = 100
        self.rotation_speed_slow = 50
