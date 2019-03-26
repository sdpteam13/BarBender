import ev3dev.ev3 as ev3
import time
from environment import Environment

env = Environment()

# reference to structure on:
# https://github.com/mahbubiftekhar/RoboTour/blob/master/EV3/robot.py

class Robot():
    def __init__(self):
        self.setup_hardware()

    def setup_hardware(self):
        # setup I/O connecting to EV3
        self.motorR = ev3.LargeMotor('outA')
        self.motorL = ev3.LargeMotor('outD')
        self.csR = ev3.ColorSensor('in2')
        self.csM = ev3.ColorSensor('in3')
        self.csL = ev3.ColorSensor('in4')
        
        # mode set up (right and left senor only used for light intensity)
        self.csR.reflected_light_intensity
        self.csL.reflected_light_intensity
        
        self.port = ev3.LegoPort('outB')
        assert self.port.connected
        self.port.mode = 'dc-motor'
        time.sleep(5)
        self.grabberArms = ev3.DcMotor("outB")
        print("DcMotor connected")

        self.grabberLift = ev3.MediumMotor('outC')
        self.gy = ev3.GyroSensor('in1')
        self.reset_gyro()
        self.up_pos = self.grabberLift.position

    def reset_gyro(self):
        self.gy.mode = "GYRO-RATE"
        self.gy.mode = "GYRO-ANG" #should reset angle to zero

    def stop(self):
        self.motorR.stop()
        self.motorL.stop()

    def straight_line_moving(self, speed = env.moving_speed_slow, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = speed)
            self.motorL.run_forever(speed_sp = speed)
        else:
            self.motorR.run_timed(speed_sp = speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = speed, time_sp = duration)
    
    def straight_line_moving_backwards(self, speed = env.moving_speed_slow, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = -speed)
            self.motorL.run_forever(speed_sp = -speed)
        else:
            self.motorR.run_timed(speed_sp = -speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = -speed, time_sp = duration)

    def rotate_right(self, speed = env.rotation_speed_normal, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = speed)
            self.motorL.run_forever(speed_sp = -speed)
        else:
            self.motorR.run_timed(speed_sp = speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = -speed, time_sp = duration)

    def rotate_left(self, speed = env.rotation_speed_normal, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = -speed)
            self.motorL.run_forever(speed_sp = speed)
        else:
            self.motorR.run_timed(speed_sp = -speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = speed, time_sp = duration)

    def steer_left(self, speed = env.moving_speed_normal, duration = -1, steer_rate = env.steer_rate_normal):
        r_speed = (1 - steer_rate) * speed
        l_speed = (1 + steer_rate) * speed
        if (duration < 0):
            self.motorR.run_forever(speed_sp = r_speed)
            self.motorL.run_forever(speed_sp = l_speed)
        else:
            self.motorR.run_timed(speed_sp = r_speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = l_speed, time_sp = duration)

    def steer_right(self, speed = env.moving_speed_normal, duration = -1, steer_rate = env.steer_rate_normal):
        r_speed = (1 + steer_rate) * speed
        l_speed = (1 - steer_rate) * speed
        if (duration < 0):
            self.motorR.run_forever(speed_sp = r_speed)
            self.motorL.run_forever(speed_sp = l_speed)
        else:
            self.motorR.run_timed(speed_sp = r_speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = l_speed, time_sp = duration)

    def line_detected(self):
        return self.line_detected_middle() or self.line_detected_right() or self.line_detected_left()

    def line_detected_middle(self):
        #table is about 60, white paper is about 90
	    # black is below 10
        return self.csM.reflected_light_intensity > env.light_intensity_threshold

    def line_detected_right(self):
        return self.csR.value(0) > env.light_intensity_threshold

    def line_detected_left(self):
        return self.csL.value(0) > env.light_intensity_threshold
    
    def line_detected_middle_special(self):
        # https://github.com/ev3dev/ev3dev-lang-python/blob/ev3dev-stretch/ev3dev2/sensor/lego.py
        return self.csM.value(0) > env.light_intensity_threshold

    def color_detected(self, c = env.corner_color):
        return self.csM.color == c

    def way_blocked(self):
    #    distance = self.us.value() / 10  # convert mm to cm
    #    print(distance)
        return False #distance < 6 or distance > 250

    def rotate_by_degree(self, degrees, time_taken=-1, speed = env.rotation_speed_normal):
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

    def rotate_left_until_detected(self, speed = env.rotation_speed_normal, slow_end = False):
            
        self.rotate_by_degree(-60)
        self.line_detected_middle() #Fixes wrongly detecting line
        if slow_end:
            self.rotate_left(speed = env.rotation_speed_slow)
        else:
            self.rotate_left(speed = speed)
        while (not self.line_detected_middle() or self.line_detected_left()):
        #while (not self.line_detected_middle_special()):
            pass
        #self.stop()
        
    def rotate_right_until_detected(self, speed = env.rotation_speed_normal, slow_end = False):
            
        self.rotate_by_degree(60)
        self.line_detected_middle() #Fixes wrongly detecting line
        if slow_end:
            self.rotate_right(speed = env.rotation_speed_slow)
        else:
            self.rotate_right(speed = speed)
        while (not self.line_detected_middle() or self.line_detected_right()):
        #while (not self.line_detected_middle_special()):
            pass

    # TODO: unused method, delete?
    # def steer_by_degree(self, degrees, time_taken = -1, speed = env.moving_speed_normal):
    #     # time_taken need to related to rotation speed, not implement for now
    #     self.reset_gyro()
    #     # positive degree - right rotation; negetive degree - left rotation
    #     if (degrees > 0):
    #         self.steer_right(speed)
    #         while self.gy.angle < degrees:
    #             pass
    #     else:
    #         self.steer_left(speed)
    #         while self.gy.angle > degrees:
    #             pass
    #     #self.stop()
    #     self.reset_gyro()

    def close_grabber(self, blocking = True):
        self.grabberArms.run_timed(duty_cycle_sp = -100, time_sp = 800)
        if blocking:
            time.sleep(0.8)

    def open_grabber(self):
        self.grabberArms.run_timed(duty_cycle_sp = 100, time_sp = 800)
        time.sleep(0.8)

    def lift_up(self, blocking = True):
        self.grabberLift.run_to_abs_pos(speed_sp = -300,
            position_sp = self.up_pos, stop_action = 'brake')
        if blocking:
            time.sleep(1.7)

    def lift_down(self, position_offset = 400):
        self.grabberLift.run_to_abs_pos(speed_sp = 300,
            position_sp = self.up_pos+position_offset,
            stop_action = 'brake')
        time.sleep(1.7)
    
    def stop_grabber(self):
        self.grabberArms.stop()

    def stop_lift(self):
        self.grabberLift.stop()

    def beep(self):
        ev3.Sound.beep()
