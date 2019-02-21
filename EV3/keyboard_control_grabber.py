import curses
import ev3dev.ev3 as ev3
import time

hand = ev3.MediumMotor('outA')
arm = ev3.MediumMotor('outD')

def main(win):
    win.nodelay(True)
    key=""
    status = " "
    while 1:
        if (arm.is_overloaded or hand.is_overloaded):
            #state = " "
            #hand.stop()
            #arm.stop()
            pass

        try:
           key = win.getkey()
           win.clear()
           win.addstr("Detected key:")
           win.addstr(str(key))

           status = key

           if (status == 'q'):
               arm.run_forever(speed_sp = 100)
           elif(status == 'a'):
               arm.run_forever(speed_sp = -100)
           elif(status == 'w'):
               hand.run_forever(speed_sp = 50)
           elif(status == 's'):
               hand.run_forever(speed_sp = -50)
           else:
               hand.stop()
               arm.stop()

        except Exception as e:
           # No input
           pass

curses.wrapper(main)
