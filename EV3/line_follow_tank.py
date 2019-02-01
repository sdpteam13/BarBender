#import curses
import ev3dev.ev3 as ev3
import time

m1 = ev3.LargeMotor('outA')
m2 = ev3.LargeMotor('outD')
cs = ev3.ColorSensor('in4')
us = ev3.UltrasonicSensor('in2')
us.mode='US-DIST-CM'

speed = 4
motortime = 1000 #ms

def turnright():
    m1.run_timed(speed_sp = -speed * 100, time_sp=motortime)
    m2.run_timed(speed_sp = speed * 100, time_sp=motortime)

def turnleft():
    m1.run_timed(speed_sp = speed * 100, time_sp=motortime)
    m2.run_timed(speed_sp = -speed * 100, time_sp=motortime)

def forward():
    m1.run_timed(speed_sp = -speed * 100, time_sp=motortime)
    m2.run_timed(speed_sp = -speed * 100, time_sp=motortime)

def detect_line():
    if (cs.reflected_light_intensity > 47): #table is about 60, white paper is about 90
        return True
    return False

lookduration = 10
lookingleft = True #previous/current direction to look

def turn():
    #go in the direction of lookingleft
    if (lookingleft):
        turnleft()
    else:
        turnright()

def find_line(attempts = 1):
    global lookingleft
    global motortime
    #Turn right briefly, turn left briefly while running detect_line
    turn()
    for i in range(1, attempts * lookduration):
        time.sleep(0.05)
        if (detect_line()):
            #found line, exit
            motortime = 1000 #reset motortime
            return
    #didn't find it on the right, try left
    lookingleft = not lookingleft
    turn()
    time.sleep(0.1 * attempts * lookduration) #reverse progress from before
    turn() #remind the motors to keep running
    for i in range(1, attempts * lookduration):
        time.sleep(0.05)
        if (detect_line()):
            #found line, exit
            motortime = 1000 #reset motortime
            return
    #didn't find it, increase sweep
    motortime = (attempts + 1) * 1000 #increase motor time to search longer
    find_line(attempts + 1)

def sense():
    distance = us.value()/10  # convert mm to cm
    print(str(distance))
    if(distance<6):
        return False        
    else:
        return True


def main():
    while(sense()):
        try:
            if (not detect_line()):
                find_line()
            forward()
            
        except Exception as e:
           print(e)
           pass

main()
#curses.wrapper(main)
