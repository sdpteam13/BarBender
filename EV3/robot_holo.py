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
        self.motorBack = ev3.LargeMotor('outC')
        self.cs = ev3.ColorSensor('in4')
        self.us = ev3.UltrasonicSensor('in2')

    def stop(self):
        self.motorR.stop()
        self.motorL.stop()
        self.motorBack.stop()

    def straight_line_moving(self, speed = 300):
        self.motorR.run_forever(speed_sp = -speed)
        self.motorL.run_forever(speed_sp = -speed)
        self.motorBack.stop()

    def rotate_left(self, speed = 200):
        self.motorR.run_forever(speed_sp = -speed)
        self.motorL.run_forever(speed_sp = speed)
        self.motorBack.run_forever(speed_sp = -speed)

    def rotate_right(self, speed = 200):
        self.motorR.run_forever(speed_sp = speed)
        self.motorL.run_forever(speed_sp = -speed)
        self.motorBack.run_forever(speed_sp = speed)

    def line_detected(self):
        #table is about 60, white paper is about 90
        return self.cs.reflected_light_intensity > 75

    def way_blocked(self):
        distance = self.us.value() / 10  # convert mm to cm
        return distance < 6

    def rotate_by_degree(self, degrees, time_taken):
        # TODO: need to related to wheel size
        pass
