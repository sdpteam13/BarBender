import curses
import ev3dev.ev3 as ev3
from robot_holo2 import Robot

def main(win):
    win.nodelay(True)
    key=""
    status = " "
    robot = Robot()

    while 1:
        try:
           key = win.getkey()
           win.clear()
           win.addstr("Detected key:")
           win.addstr(str(key))

           status = key

           if (status == 'q'):
               robot.lift_up()
           elif(status == 'a'):
               robot.lift_down()
           elif(status == 'w'):
               robot.open_grabber()
           elif(status == 's'):
               robot.close_grabber()
           else:
               robot.stop_grabber()
               robot.stop_lift()

        except Exception as e:
           # No input
           pass

curses.wrapper(main)
