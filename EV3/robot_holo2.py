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

    def reset_gyro(self):
        #self.gy.mode = "GYRO-RATE"
        #self.gy.mode = "GYRO-ANG" #should reset angle to zero
        pass

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

    def rotate_right(self, speed = 300, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = speed)
            self.motorL.run_forever(speed_sp = -speed)
        else:
            self.motorR.run_timed(speed_sp = speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = -speed, time_sp = duration)

    def rotate_left(self, speed = 300, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = -speed)
            self.motorL.run_forever(speed_sp = speed)
        else:
            self.motorR.run_timed(speed_sp = -speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = speed, time_sp = duration)

    def steer_left(self, speed = 300, speed_back = 100, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = -speed)
            self.motorL.run_forever(speed_sp = -0.5*speed)
        else:
            self.motorR.run_timed(speed_sp = -speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = -0.5*speed, time_sp = duration)

    def steer_right(self, speed = 300, speed_back = 100, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = -0.5*speed)
            self.motorL.run_forever(speed_sp = -speed)
        else:
            self.motorR.run_timed(speed_sp = -0.5*speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = -speed, time_sp = duration)

    # for first deemo these should be enough
    def line_detected(self):
        #return self.line_detected_middle() or self.line_detected_right() or self.line_detected_left()
        return False

    def line_detected_middle(self):
        #table is about 60, white paper is about 90
	    # black is below 10
        #return self.csM.reflected_light_intensity > 20
        return False

    def line_detected_right(self):
        #return self.csR.reflected_light_intensity > 20
        return False

    def line_detected_left(self):
        #return self.csL.reflected_light_intensity > 20
        return False

    def color_detected(self, c):
        colours = ["none", "black", "blue", "green",
		"yellow", "red", "white", "brown"]
        #print(colours[self.csM.color])
        #return colours[self.csR.color] == c or colours[self.csL.color] == c or colours[self.csM.color] == c
        return False

    def way_blocked(self):
    #    distance = self.us.value() / 10  # convert mm to cm
    #    print(distance)
        return False #distance < 6 or distance > 250

    def rotate_by_degree(self, degrees, time_taken=-1, speed = 300):
        # time_taken need to related to rotation speed, not implement for now
        #self.reset_gyro()
        # positive degree - right rotation; negetive degree - left rotation
        #if (degrees > 0):
        #    self.rotate_right(speed)
        #    while self.gy.angle < degrees:
        #        pass
        #else:
        #    self.rotate_left(speed)
        #    while self.gy.angle > degrees:
        #        pass
        #self.stop()
        pass
