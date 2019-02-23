import ev3dev.ev3 as ev3
import time
from robot_holo2 import Robot
from line_follow_holo3 import LineFollower

robot = Robot()
lf = LineFollower()

# right angle
def turn_right(send_completion=True):
    robot.rotate_right_until_detected()
    robot.stop()
    #robot.rotate_by_degree(degrees = 85)


# right angle
def turn_left():
    robot.rotate_left_until_detected()
    robot.stop()
    #robot.rotate_by_degree(degrees = -85)

# follows white line until an intersection is discovered (to be replaced by pi vision)
def follow_line_until_intersection():
        found_intersection = False
        robot.straight_line_moving()
        while not found_intersection:
            if robot.color_detected('green'):
                found_intersection = True
            else:
                #if (not robot.line_detected()):
                #    #may have found intersection
                #    if (robot.color_detected('green')):
                #        found_intersection = True
                #    else:
                #        lf.find_line()
                #        robot.straight_line_moving()

                lf.iteration()

            #if robot.way_blocked():
            #    robot.stop()
            #    time.sleep(0.2)
            #else:
            #    robot.straight_line_moving()


        start = time.time()
        print("hello")
        end = time.time()
        sp = 300
        while (sp - 150 * (end - start) > 80):
            robot.straight_line_moving(speed = sp - 150 * (end - start)) #move into the intersection
            print(sp - 150 * (end - start))
            end = time.time()

        robot.straight_line_moving(speed = 80, duration = 1000)
        time.sleep(2)

# follows white line
	pass

# between -1 and 1, -1 is turn left, 1 is turn right
def turn(amount):
	pass

def stop():
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
        #robot.rotate_by_degree(degrees = 180)
        robot.rotate_by_degree(degrees = 90)
        robot.rotate_right_until_detected()
        robot.stop()
    else:
        #robot.rotate_by_degree(degrees = -180)
        robot.rotate_by_degree(degrees = -90)
        robot.rotate_left_until_detected()
        robot.stop()

def grab_cup():
    """
    After reaching an intersection (intersection A), the robot should then turn around and slowly approach the cup.
    After the robot reaches the cup it should grab the cup and lift it off the ground
    The robot should then go forwards towards intersection A and stop when it reaches the intersection
    """
    pass

def drop_cup():
    """
    After reaching an intersection, the robot should turn around, mvoe backwards, drop the cup and finally move forwards until it reaches the intersection again
    """
    pass

def dance():
    #robot.rotate_by_degree(degrees = 360)
    pass
