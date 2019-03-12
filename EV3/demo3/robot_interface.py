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
def turn_right(speed = 100):
    robot.rotate_right_until_detected(speed)
    robot.stop()
    #robot.rotate_by_degree(degrees = 85)


# right angle
def turn_left(speed = 100):
    robot.rotate_left_until_detected(speed)
    robot.stop()
    #robot.rotate_by_degree(degrees = -85)

# follows white line until an intersection is discovered (to be replaced by pi vision)
def follow_line_until_intersection(slow = False, slow_duration = 1500):
        found_intersection = False
        robot.straight_line_moving()
        while not found_intersection:
            if robot.color_detected('red'):
                found_intersection = True
            else:
                lf.iteration()
        if slow:
            slowdown(slow_duration)
        else:
            robot.stop()
        
def backwards_until_intersection():
    found_intersection = False
    robot.straight_line_moving_backwards()
    while not found_intersection:
        if robot.color_detected(env.corner_color):
            found_intersection = True
        # else:
        #     lf.iteration_backwards()

def slowdown(duration = 1500):
    #start = time.time()
    #end = time.time()
    #sp = 300
    #while (sp - 150 * (end - start) > 80):
    #    robot.straight_line_moving(speed = sp - 150 * (end - start)) #move into the intersection
    #    #print(sp - 150 * (end - start))
    #    end = time.time()
    #robot.straight_line_moving(speed = 80, duration = 1000)
    #time.sleep(2)
    robot.straight_line_moving(duration = duration)
    time.sleep(duration / 1000.0)

def get_drink_A():
    # use after grab cup
    # turn_left()
    
    #follow_line_until_intersection()
    turn_right(speed = 50)
    robot.straight_line_moving_backwards(duration = 600)
    time.sleep(0.6)
    
    # TODO replace sleep by server
    time.sleep(10)
    
    robot.straight_line_moving(duration = 600)
    time.sleep(0.6)
    turn_right()

    
def get_drink_B():
    # use after get first drink
    
    
    #follow_line_until_intersection(slow = True, slow_duration = 500)
    
    #follow_line_until_intersection()
    turn_left(speed = 50)
    robot.straight_line_moving_backwards(duration = 600)
    time.sleep(0.6)
    
    # TODO replace sleep by server
    time.sleep(10)
    
    robot.straight_line_moving(duration = 600)
    time.sleep(0.6)
    turn_left()
    
    #follow_line_until_intersection(slow=True)
    #turn_right()
    
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
    backwards_until_intersection()
    #robot.straight_line_moving_backwards(duration = 2000)
    #time.sleep(2)
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
