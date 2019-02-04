import ev3dev.ev3 as ev3
import time
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
	pass

# follows white line until an intersection is discovered (to be replaced by pi vision)
def follow_line_until_intersection():
	pass

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
	turn_right(False)
	turn_right(False)
	completed()

# send post request to server showing success
def completed():
	pass
