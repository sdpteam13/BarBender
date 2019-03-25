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
        
        
        #TODO: implement using the DC motor if need
        #self.grabberArms = ev3.MediumMotor('outC')
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

    def rotate_right(self, speed, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = speed)
            self.motorL.run_forever(speed_sp = -speed)
        else:
            self.motorR.run_timed(speed_sp = speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = -speed, time_sp = duration)

    def rotate_left(self, speed, duration = -1):
        if (duration < 0):
            self.motorR.run_forever(speed_sp = -speed)
            self.motorL.run_forever(speed_sp = speed)
        else:
            self.motorR.run_timed(speed_sp = -speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = speed, time_sp = duration)

    def steer_left(self, speed, duration = -1):
        speed = speed + 50
        if (duration < 0):
            self.motorR.run_forever(speed_sp = 0.7*speed)
            self.motorL.run_forever(speed_sp = speed)
        else:
            self.motorR.run_timed(speed_sp = 0.7*speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = speed, time_sp = duration)

    def steer_right(self, speed, duration = -1):
        speed = speed + 50
        if (duration < 0):
            self.motorR.run_forever(speed_sp = speed)
            self.motorL.run_forever(speed_sp = 0.7*speed)
        else:
            self.motorR.run_timed(speed_sp = speed, time_sp = duration)
            self.motorL.run_timed(speed_sp = 0.7*speed, time_sp = duration)

    def line_detected(self):
        return self.line_detected_middle() or self.line_detected_right() or self.line_detected_left()

    def line_detected_middle(self):
        #table is about 60, white paper is about 90
	    # black is below 10
        return self.csM.reflected_light_intensity > 30

    def line_detected_right(self):
        return self.csR.reflected_light_intensity > 30

    def line_detected_left(self):
        return self.csL.reflected_light_intensity > 30

    def color_detected(self, c = "red"):
        colours = ["none", "black", "blue", "green",
		"yellow", "red", "white", "brown"]
        #print(colours[self.csM.color])
        #return colours[self.csR.color] == c or colours[self.csL.color] == c or colours[self.csM.color] == c
        #print (colours[self.csM.color])
        #print (c)
        return colours[self.csM.color] == c

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
        self.reset_gyro()

    def rotate_left_until_detected(self, speed = env.rotation_speed_normal):
            
        self.rotate_by_degree(-60)
        self.line_detected_middle() #Fixes wrongly detecting line
        self.rotate_left(speed)
        #while (not self.line_detected_middle() or self.line_detected_left()):
        while (not self.line_detected_middle()):
            pass
        #self.stop()
        self.reset_gyro()
        
    def rotate_right_until_detected(self, speed = env.rotation_speed_normal):
            
        self.rotate_by_degree(60)
        self.line_detected_middle() #Fixes wrongly detecting line
        self.rotate_right(speed)
        #while (not self.line_detected_middle() or self.line_detected_right()):
        while (not self.line_detected_middle()):
            pass
        #self.stop()
        self.reset_gyro()

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
