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
#overrun = do overrun after intersection
#fast = line following speed increase
def follow_line_until_intersection(overrun = False, overrun_short = False, fast = False):
        found_intersection = False
        
        lf_speed = None
        if fast:
            lf_speed = 500
            
        #robot.straight_line_moving()
        while not found_intersection:
            if robot.color_detected('red'):
                found_intersection = True
            else:
                lf.iteration(a_speed = lf_speed)
        if overrun:
            if overrun_short:
                slowdown_short(speed = lf_speed)
            else:
                slowdown(speed = lf_speed)
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

def slowdown(speed = None):
    if speed is None:
        speed = 250
        duration = 1400
    else:
        #run the same distance regardless of speed
        duration = 1400 * 250 / speed
        
    robot.straight_line_moving(duration = duration, speed = speed)
    time.sleep(duration / 1000.0 - 0.1)
    
def slowdown_short(speed = None):
    if speed is None:
        speed = 250
        duration = 600
    else:
        #run the same distance regardless of speed
        duration = 600 * 250 / speed
        
    robot.straight_line_moving(duration = duration, speed = speed)
    time.sleep(duration / 1000.0 - 0.15)
    print(robot.csM.reflected_light_intensity)
    
def get_drink(drink='A'):
    if drink == 'A':
        turn_left(speed = 50)
    else:
        turn_right(speed = 50)


    #turn_left(speed = 50)
    robot.straight_line_moving_backwards(duration = 650)
    time.sleep(0.7)
    
    robot.beep()
    client_socket.send_and_receive(drink)
    robot.beep()
    
    robot.straight_line_moving(duration = 650)
    time.sleep(0.7)
    if drink == 'A':
        turn_left(speed=50)
    else:
        turn_right(speed=50)
    
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
def turn_around(direction='right', speed = None):
    if (direction == 'right'):
        #robot.rotate_by_degree(degrees = 180)
        robot.rotate_by_degree(degrees = 80)
        robot.rotate_right_until_detected(speed)
        robot.stop()
    else:
        #robot.rotate_by_degree(degrees = -180)
        robot.rotate_by_degree(degrees = -80)
        robot.rotate_left_until_detected(speed)
        robot.stop()
    

def grab_cup():
    """
    After reaching the cup intersection, the robot should turn around and go backwards until it reaches he intersection again,
    the robot should then pickup a cup.
    """
    turn_around(direction='right', speed = 50)
    #lift down a bit less so the grabber clears the stand
    robot.lift_down(position_offset = 285)
    backwards_until_intersection()
    robot.stop()
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
    After reaching an intersection, the robot should turn around, move backwards
    drop the cup and finally move forwards until it reaches the intersection again
    """
    robot.lift_down()
    robot.open_grabber()
    robot.open_grabber()
    robot.lift_up(blocking = False)
    robot.close_grabber(blocking = False)

def dance():
    for i in range(5):
        robot.beep()
        time.sleep(1)