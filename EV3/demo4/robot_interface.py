import time
import client_socket
from robot import Robot
from line_follower import LineFollower
from environment import Environment

robot = Robot()
env = Environment()
lf = LineFollower(robot)

# right angle
def turn_right(slow_end = False):
    robot.rotate_right_until_detected(slow_end = slow_end)
    robot.stop()
    #robot.rotate_by_degree(degrees = 85)


# right angle
def turn_left(slow_end = False):
    robot.rotate_left_until_detected(slow_end = slow_end)
    robot.stop()
    #robot.rotate_by_degree(degrees = -85)

# follows white line until an intersection is discovered (to be replaced by pi vision)
#overrun = do overrun after intersection
#fast = line following speed increase
def follow_line_until_intersection(overrun = False, overrun_short = False, fast = False):
        found_intersection = False
        
        if fast:
            lf_speed = env.moving_speed_normal
        else:
            lf_speed = env.moving_speed_slow
            
        while not robot.color_detected():
            lf.iteration(a_speed = lf_speed)
            
        if overrun:
            if overrun_short:
                slowdown_short(speed = lf_speed)
            else:
                slowdown(speed = lf_speed)
        else:
            robot.stop()
            
def follow_line_with_gyro_recorded():
    robot.reset_gyro()
    iteration = 1
    value = robot.gy.angle
    while not robot.color_detected():
        lf.iteration(a_speed = env.moving_speed_slow)
        iteration = iteration + 1.0
        value = value + robot.gy.angle
    return value / iteration
        
def backwards_until_intersection():
    robot.straight_line_moving_backwards()
    while not robot.color_detected():
        pass
    
def backwards_moving_using_gyro(value):
    while not robot.color_detected():
        diff = (robot.gy.angle - value)
        if (diff > 3 or diff < -3):
            robot.rotate_by_degree_special(target = value)
            robot.stop()
        else:
            robot.straight_line_moving_backwards()

def backwards_adjust():
    robot.straight_line_moving_backwards(speed = 50)
    while robot.color_detected():
        pass
    robot.stop()
    
def forward_adjust():
    robot.straight_line_moving(speed = 100)
    while robot.color_detected():
        pass
    robot.stop()

def slowdown(speed = env.moving_speed_slow):
    #run the same distance regardless of speed
    duration = 1400 * env.moving_speed_slow / speed
    robot.straight_line_moving(duration = duration, speed = speed)
    time.sleep(duration / 1000.0 - 0.1)
    
def slowdown_short(speed = env.moving_speed_slow):
    #run the same distance regardless of speed
    duration = 600 * env.moving_speed_slow / speed
    robot.straight_line_moving(duration = duration, speed = speed)
    time.sleep(duration / 1000.0 - 0.15)
    
def get_drink(drink='A'):
    backwards_adjust()
    
    if drink == 'A':
        turn_left(slow_end = True)
    else:
        turn_right(slow_end = True)


    robot.straight_line_moving_backwards(duration = 690)
    time.sleep(0.7)
    
    robot.beep()
    client_socket.send_and_receive(drink)
    robot.beep()
    
    robot.straight_line_moving(duration = 690)
    time.sleep(0.7)
    if drink == 'A':
        turn_left(slow_end = True)
    else:
        turn_right(slow_end = True)

def stop():
	robot.stop()

# go forward in straight line
def go():
	pass

# set speed to x, 0 <= x <= 1
def set_speed(x):
	pass

def turn(amount):	
	pass

# 180 degree turn
def turn_around(direction='right', slow_end = False):
    if (direction == 'right'):
        #robot.rotate_by_degree(degrees = 180)
        robot.rotate_by_degree(degrees = 80)
        robot.rotate_right_until_detected(slow_end = slow_end)
        robot.stop()
    else:
        #robot.rotate_by_degree(degrees = -180)
        robot.rotate_by_degree(degrees = -80)
        robot.rotate_left_until_detected(slow_end = slow_end)
        robot.stop()
    

def grab_cup():
    """
    After reaching the cup intersection, the robot should turn around and go backwards until it reaches he intersection again,
    the robot should then pickup a cup.
    """
    value = follow_line_with_gyro_recorded()
    forward_adjust()
    robot.rotate_by_degree_special(target = value + 180)
    robot.stop()
    
    #lift down a bit less so the grabber clears the stand
    robot.lift_down(position_offset = 285, blocking = False)
    
    backwards_moving_using_gyro(value + 180)
    
    robot.stop()
    robot.close_grabber(long = True)
    robot.lift_up()
    robot.straight_line_moving(duration = 800)
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
    #robot.open_grabber()
    robot.lift_up(blocking = False)
    #robot.close_grabber(blocking = False)

def dance():
    for i in range(5):
        robot.beep()
        time.sleep(1)