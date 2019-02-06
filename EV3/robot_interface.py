import ev3dev.ev3 as ev3
import time
from robot_holo import Robot
from line_follow_holo3 import LineFollower

robot = Robot()
lf = LineFollower()

# right angle
def turn_right(send_completion=True):
    robot.rotate_by_degree(degrees = 90)


# right angle
def turn_left():
    robot.rotate_by_degree(degrees = -90)

# follows white line until an intersection is discovered (to be replaced by pi vision)
def follow_line_until_intersection():
        found_intersection = False
        robot.straight_line_moving()
        while not found_intersection:
            if robot.color_detected('green'):
                found_intersection = True
            else:
                if (not robot.line_detected()):
                    #may have found intersection
                    if (robot.color_detected('green')):
                        found_intersection = True
                    else:
                        lf.find_line()
                        robot.straight_line_moving()

            if robot.way_blocked():
                robot.stop()
                time.sleep(0.2)
            else:
                robot.straight_line_moving()

        robot.straight_line_moving(duration = 550) #move into the intersection
        time.sleep(0.8)

# follows white line (to be replaced by pi vision)
def follow_line():
	pass

# between -1 and 1, -1 is turn left, 1 is turn right
def turn(amount):
	pass

def stop():
	robot.stop()
	robot.stop()

# go forward in straight line
def go():
	pass

# set speed to x, 0 <= x <= 1
def set_speed(x):
	pass

# 180 degree turn
def turn_around(direction='right'):
    if (direction == 'right'):
        robot.rotate_by_degree(degrees = 180)
    else:
        robot.rotate_by_degree(degrees = -180)
