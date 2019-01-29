import curses
import ev3dev.ev3 as ev3
import time

m1 = ev3.LargeMotor('outA')
m2 = ev3.LargeMotor('outD')

go = 0
turn = 0

def main(win):
    win.nodelay(True)
    key=""
    #win.clear()
    #win.addstr("Detected key:")
    go = 1.0
    status = ' '
    while 1:
        try:
           key = win.getkey()
           win.clear()
           win.addstr("Detected key:")
           win.addstr(str(key))

           if (key == 'r'):
               # speedup
               if (go < 9):
                   go += 0.5
           elif(key == 'f'):
               # speeddown
               if (go > 0):
                   go -= 0.5
           else:
               status = key

           if (status == 'w'):
               m1.run_forever(speed_sp = go * 100)
               m2.run_forever(speed_sp = go * 100)
           elif(status == 's'):
               m1.run_forever(speed_sp = -go * 100)
               m2.run_forever(speed_sp = -go * 100)
           elif(status == 'a'):
               m1.run_forever(speed_sp = 200)
               m2.run_forever(speed_sp = -200)
           elif(status == 'd'):
               m1.run_forever(speed_sp = -200)
               m2.run_forever(speed_sp = 200)
           else:
               m1.stop()
               m2.stop()

        except Exception as e:
           # No input
           pass

curses.wrapper(main)
