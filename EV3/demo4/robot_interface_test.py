from robot_interface import *
import time
#Test visiting the cup dispenser
# for i in range(2):
#     follow_line_until_intersection()
#     grab_cup()

#     drop_cup()
#     follow_line_until_intersection()
#     turn_around()
def do(st):
    for i in range(len(st)):
        c = st[i]
        
        print ("Executing " + str(c))
        if (c == 'r'):
            turn_right()
        elif(c == 'l'):
            turn_left()
        elif (c == 'follow_line'):
            follow_line()
        elif c == 'f':
            follow_line_until_intersection(overrun=True)
        elif c == 'F':
            # do short overrun when the next command is fast line following
            follow_line_until_intersection(overrun=True, overrun_short = (len(st) == i+1 or st[i+1] == 'F'), fast=True)
        elif c[:4] == 'turn':
            turn(float(st[4:]))
        elif c == 'g':
            go()
        elif c == 'd':
            dance()
        elif st[:9] == 'set_speed':
            set_speed(int(st[9:]))
        elif c == 't':
            turn_around()
        elif c == 'stop':
            stop()
        elif c == 'c':
            grab_cup()
        elif c == 'x':
            drop_cup()
        elif c == 's':
            follow_line_until_intersection(overrun=False)
        elif c == 'a':
            get_drink('A')
        elif c == 'b':
            get_drink('B')
        elif c == '0':
            change_gif('0')
        elif c == '1':
            change_gif('1')
        elif c == '2':
            change_gif('2')
        else:
            stop()
            
times = []
init_time = time.time()
print (lf.offline)
for i in range(1):
    do(['c','F','F','t','x','F'])
    #do(['c','l','s','b','f', 's','a', 'f', 'r','F','F','t','x','F'])
    start = time.time()
    #do(['2','c','l','s','b','f', 's','a', 'f', 'r','F','F','l','f','0','t','x','1','f','2','r','F'])
    #do(['2','c','l','s','b','f', 'l','F','F','F','l','f','0','t','x','1','f','2','r','F','F'])
    times.append(time.time() - start)
    
print ("times: " + str(times))
print ("total: " + str(time.time() - init_time))
print ("offline: " + str(lf.offline))

#do(['c','l','s','b','f', 's','a', 'f', 'r','F','F','F','F','l','f','t','x','f','r','F','F','F'])
#do(['c','l','s','b','f', 's','a', 'f', 'r','F','F','l','f','t','x','f','r','F'])
#do(['c','l','s','b','f', 's','a', 'f', 'r','F','F','t','x','F'])