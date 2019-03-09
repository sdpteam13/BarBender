import ev3dev.ev3 as ev3
import time
import client_socket
from robot_holo2 import Robot
from line_follow_holo3 import LineFollower
from environment import Environment

robot = Robot()
env = Environment()
lf = LineFollower(robot,env)

def start():
    """
    pre setup for robot state
    """
    robot.lift_up()

def end():
    #robot.lift_down()
    robot.stop()

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
def follow_line_until_intersection(slow = False):
        found_intersection = False
        robot.straight_line_moving()
        while not found_intersection:
            if robot.color_detected('red'):
                found_intersection = True
            else:
                lf.iteration()
        if slow:
            slowdown()
        else:
            robot.stop()
        
def follow_line_backwards_until_intersection():
    found_intersection = False
    robot.straight_line_moving_backwards()
    while not found_intersection:
        if robot.color_detected(env.corner_color):
            found_intersection = True
        # else:
        #     lf.iteration_backwards()

def slowdown():
    #start = time.time()
    #end = time.time()
    #sp = 300
    #while (sp - 150 * (end - start) > 80):
    #    robot.straight_line_moving(speed = sp - 150 * (end - start)) #move into the intersection
    #    #print(sp - 150 * (end - start))
    #    end = time.time()
    #robot.straight_line_moving(speed = 80, duration = 1000)
    #time.sleep(2)
    robot.straight_line_moving(duration = 1700)
    time.sleep(1.7)
    
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
        robot.rotate_by_degree(degrees = 70)
        robot.rotate_right_until_detected()
        robot.stop()
    else:
        #robot.rotate_by_degree(degrees = -180)
        robot.rotate_by_degree(degrees = -70)
        robot.rotate_left_until_detected()
        robot.stop()

def grab_cup():
    """
    After reaching the cup intersection, the robot should turn around and go backwards until it reaches he intersection again,
    the robot should then pickup a cup.
    """
    turn_around(direction='right')
    #robot.open_grabber()
    robot.lift_down_less()
    #follow_line_backwards_until_intersection()
    robot.straight_line_moving_backwards(duration = 2000)
    time.sleep(2)
    robot.stop()
    #robot.lift_down_less()
    #robot.close_grabber()
    robot.close_grabber()
    robot.lift_up()
    robot.straight_line_moving(duration = 1000)
    time.sleep(1)
    try:
        client_socket.send('X')
    except:
        pass


def drop_cup():
    """
    After reaching an intersection, the robot should turn around, mvoe backwards, drop the cup and finally move forwards until it reaches the intersection again
    """
    robot.lift_down()
    robot.open_grabber()
    robot.open_grabber()
    robot.lift_up()
    robot.straight_line_moving(duration=500)
    time.sleep(0.5)
    robot.close_grabber()

def dance():
    for i in range(5):
        ev3.Sound.beep()
        time.sleep(1)
