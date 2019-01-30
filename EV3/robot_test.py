import curses
import robot

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

           win.clear()
           win.addstr("Detected key:")
           win.addstr(str(key))

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

           if (status == 'w'):
               robot.straight_line_moving(speed = motor_speed)
           elif(status == 's'):
               robot.straight_line_moving(speed = -motor_speed)
           elif(status == 'a'):
               robot.rotate_left()
           elif(status == 'd'):
               robot.rotate_right()
           else:
               robot.stop()

        except Exception as e:
           # No input
           pass

curses.wrapper(main)
