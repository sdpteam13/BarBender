import ev3dev.ev3 as ev3
import time

# reference to structure on:
# https://github.com/mahbubiftekhar/RoboTour/blob/master/EV3/robot.py

class Robot():
    def __init__(self):
        self.setup_hardware()

    def setup_hardware(self):
        # setup I/O connecting to EV3
        self.motorR = ev3.LargeMotor('outA')
        self.motorL = ev3.LargeMotor('outD')

    def stop(self):
        self.motorR.stop()
        self.motorL.stop()

    def straight_line_moving(self, speed = 300):
        self.motorR.run_forever(speed_sp = speed)
        self.motorL.run_forever(speed_sp = speed)

    def rotate_left(self, speed = 200):
        self.motorR.run_forever(speed_sp = -speed)
        self.motorL.run_forever(speed_sp = speed)

    def rotate_right(self, speed = 200):
        self.motorR.run_forever(speed_sp = -speed)
        self.motorL.run_forever(speed_sp = speed)

    # for first deemo these should be enough

    def rotate_by_degree(self, degrees, time_taken):
        # TODO: need to related to wheel size
