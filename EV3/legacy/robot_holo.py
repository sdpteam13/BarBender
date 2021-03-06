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
        self.csR = ev3.ColorSensor('in2')
        self.csM = ev3.ColorSensor('in3')
        self.csL = ev3.ColorSensor('in4')
        #self.us = ev3.UltrasonicSensor('in1')
        self.gy = ev3.GyroSensor('in1')
        self.reset_gyro()
        #self.us.mode='US-DIST-CM'

    def reset_gyro(self):
        self.gy.mode = "GYRO-RATE"
        self.gy.mode = "GYRO-ANG" #should reset angle to zero

    def stop(self):
        self.motorR.stop()
        self.motorL.stop()
        self.motorBack.stop()

    def straight_line_moving(self, speed = 300, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = -speed)
            self.motorL.run_forever(speed_sp = -speed)
            self.motorBack.stop()
        else:
            self.motorR.run_timed(speed_sp = -speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = -speed, time_sp = duration)
            self.motorBack.stop()

    def rotate_left(self, speed = 150, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = speed)
            self.motorL.run_forever(speed_sp = -speed)
            self.motorBack.run_forever(speed_sp = 1.2 * -speed)
        else:
            self.motorR.run_timed(speed_sp = speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = -speed, time_sp = duration)
            self.motorBack.run_timed(speed_sp = 1.2 * -speed, time_sp = duration)

    def rotate_right(self, speed = 150, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = -speed)
            self.motorL.run_forever(speed_sp = speed)
            self.motorBack.run_forever(speed_sp = 1.2 * speed)
        else:
            self.motorR.run_timed(speed_sp = -speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = speed, time_sp = duration)
            self.motorBack.run_timed(speed_sp = 1.2 * speed, time_sp = duration)

    def steer_right(self, speed = 500, speed_back = 150, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = -speed)
            self.motorL.run_forever(speed_sp = -0.3*speed)
            self.motorBack.run_forever(speed_sp = speed_back)
        else:
            self.motorR.run_timed(speed_sp = -speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = -0.3*speed, time_sp = duration)
            self.motorBack.run_timed(speed_sp = speed_back, time_sp = duration)

    def steer_left(self, speed = 500, speed_back = 150, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = -0.3*speed)
            self.motorL.run_forever(speed_sp = -speed)
            self.motorBack.run_forever(speed_sp = -speed_back)
        else:
            self.motorR.run_timed(speed_sp = -0.3*speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = -speed, time_sp = duration)
            self.motorBack.run_timed(speed_sp = -speed_back, time_sp = duration)

    def line_detected(self):
        return self.line_detected_middle() or self.line_detected_right() or self.line_detected_left()

    def line_detected_middle(self):
        #table is about 60, white paper is about 90
	    # black is below 10
        return self.csM.reflected_light_intensity > 20

    def line_detected_right(self):
        return self.csR.reflected_light_intensity > 20

    def line_detected_left(self):
        return self.csL.reflected_light_intensity > 20

    def color_detected(self, c):
        colours = ["none", "black", "blue", "green",
		"yellow", "red", "white", "brown"]
        #print(colours[self.csM.color])
        #return colours[self.csR.color] == c or colours[self.csL.color] == c or colours[self.csM.color] == c
        return colours[self.csM.color] == c

    def way_blocked(self):
    #    distance = self.us.value() / 10  # convert mm to cm
    #    print(distance)
        return False #distance < 6 or distance > 250

    def rotate_by_degree(self, degrees, time_taken=-1, speed = 300):
        # time_taken need to related to rotation speed, not implement for now
        self.reset_gyro()
        # positive degree - right rotation; negetive degree - left rotation
        if (degrees > 0):
            self.rotate_right(speed)
            while self.gy.angle < degrees:
                pass
        else:
            self.rotate_left(speed)
            while self.gy.angle > degrees:
                pass
        #self.stop()
        self.reset_gyro()

    def rotate_left_until_detected(self, speed = 300):
        self.rotate_by_degree(-45)
        while (not self.line_detected_middle() or self.line_detected_right() or self.line_detected_left()):
            self.rotate_left(speed)
        #self.stop()
        self.reset_gyro()


    def rotate_right_until_detected(self, speed = 300):
        self.rotate_by_degree(45)
        while (not self.line_detected_middle() or self.line_detected_right() or self.line_detected_left()):
            self.rotate_right(speed)
        #self.stop()
        self.reset_gyro()


    def steer_by_degree(self, degrees, time_taken = -1, speed = 300):
        # time_taken need to related to rotation speed, not implement for now
        self.reset_gyro()
        # positive degree - right rotation; negetive degree - left rotation
        if (degrees > 0):
            self.steer_right(speed)
            while self.gy.angle < degrees:
                pass
        else:
            self.steer_left(speed)
            while self.gy.angle > degrees:
                pass
        #self.stop()
        self.reset_gyro()
