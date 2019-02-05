import ev3dev.ev3 as ev3
import time
import os
from robot_holo import Robot
from line_follow_holo3 import LineFollower

robot = Robot()
lf = LineFollower()

# right angle
def turn_right(send_completion=True):
        robot.reset_gyro()
        robot.rotate_right()
        while robot.gy.angle < 90:
         pass
        robot.stop()
        completed()


# right angle
def turn_left():
    robot.reset_gyro()
    robot.rotate_left()
    while robot.gy.angle > -90:
     pass
    robot.stop()
    completed()

# follows white line until an intersection is discovered (to be replaced by pi vision)
def follow_line_until_intersection():
        blue_iter = 0
        iter_threshold = 1
        while True:
            if blue_iter == iter_threshold:
                robot.stop()
                break
            elif robot.color_detected('green'):
                blue_iter += 1
            else:
                blue_iter = 0
                if (not robot.line_detected()):
                    lf.find_line()
                lf.forward()
        robot.straight_line_moving(duration = 550)
        time.sleep(0.8)
        robot.stop()
        completed()

# follows white line (to be replaced by pi vision)
def follow_line():
	pass

# between -1 and 1, -1 is turn left, 1 is turn right
def turn(amount):
	pass

def stop():
	motorR.stop()
	motorL.stop()

# go forward in straight line
def go():
	pass

# set speed to x, 0 <= x <= 1
def set_speed(x):
	pass

# 180 degree turn
def turn_around(direction='right'):
        robot.reset_gyro()
        robot.rotate_right()
        while robot.gy.angle < 90:
                pass
        robot.stop()
        robot.reset_gyro()
        robot.rotate_right()
        while robot.gy.angle < 90:
                pass
        robot.stop()
        completed()

# send post request to server showing success
def completed():
        #os.system("wget http://192.168.105.142/EV3/ &")
        #print ("finished!")
	pass
