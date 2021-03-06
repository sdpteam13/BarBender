import curses
from robot_holo2 import Robot
# can use: "from robot import Robot" if using track version

# should have same effect as keyboard_control3.py
def main(win):
    win.nodelay(True)
    key=""

    # speed received from server/app side?
    motor_speed = 100

    status = ' '
    robot = Robot()

    while 1:
        try:
           key = win.getkey()



           if (key == 'r'):
               # speed up
               if (motor_speed < 900):
                   motor_speed += 50
           elif(key == 'f'):
               # speed down
               if (motor_speed > 0):
                   motor_speed -= 50
           else:
               status = key

           win.clear()
           win.addstr("Speed: ")
           win.addstr(str(motor_speed))
           win.addstr("; Detected key:")
           win.addstr(str(key))

           if (status == 'w'):
               robot.straight_line_moving(speed = motor_speed)
           elif(status == 's'):
               robot.straight_line_moving(speed = -motor_speed)
           elif(status == 'a'):
               robot.rotate_left()
           elif(status == 'd'):
               robot.rotate_right()
           elif(status == 'q'):
               robot.steer_left()
           elif(status == 'e'):
               robot.steer_right()
           else:
               robot.stop()

        except Exception as e:
           # No input
           pass

curses.wrapper(main)
