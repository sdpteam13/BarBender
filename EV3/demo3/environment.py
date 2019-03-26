# reference to structure on:
# https://github.com/mahbubiftekhar/RoboTour/blob/master/EV3/environment.py

class Environment():
    def __init__(self):
        self.colours = ["none", "black", "blue", "green",
        "yellow", "red", "white", "brown"]
        self.light_intensity_threshold = 30
        self.corner_color = 5 # red
        self.moving_speed_normal = 500
        self.moving_speed_slow = 250
        self.rotation_speed_normal = 200
        self.rotation_speed_slow = 50
        self.steer_rate_normal = 0.15 # between 0 and 1
