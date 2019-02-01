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
        self.cs = ev3.ColorSensor('in4')
        self.us = ev3.UltrasonicSensor('in2')
        self.us.mode='US-DIST-CM'

    def stop(self):
        self.motorR.stop()
        self.motorL.stop()

    def straight_line_moving(self, speed = 300, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = -speed)
            self.motorL.run_forever(speed_sp = -speed)
        else:
            self.motorR.run_timed(speed_sp = -speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = -speed, time_sp = duration)

    def rotate_left(self, speed = 200, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = speed)
            self.motorL.run_forever(speed_sp = -speed)
        else:
            self.motorR.run_timed(speed_sp = speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = -speed, time_sp = duration)

    def rotate_right(self, speed = 200, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = -speed)
            self.motorL.run_forever(speed_sp = speed)
        else:
            self.motorR.run_timed(speed_sp = -speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = speed, time_sp = duration)

    # for first deemo these should be enough
    def line_detected(self):
        #table is about 60, white paper is about 90
        return self.cs.reflected_light_intensity > 47

    def way_blocked(self):
        distance = self.us.value() / 10  # convert mm to cm
        return distance < 6

    def rotate_by_degree(self, degrees, time_taken):
        # TODO: need to related to wheel size
        pass
