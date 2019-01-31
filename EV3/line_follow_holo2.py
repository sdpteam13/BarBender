import ev3dev.ev3 as ev3
import time

m1 = ev3.LargeMotor('outA')
m2 = ev3.LargeMotor('outD')
m3 = ev3.LargeMotor('outC')
cs = ev3.ColorSensor('in4')
us = ev3.UltrasonicSensor('in2')
#gs = ev3.GyroSensor('in3')
us.mode='US-DIST-CM'

speed = 2.2
motortime = 1000 #ms

def forward():
    for i in range(int(motortime / 100)):
        if way_blocked():
            m1.stop()
            m2.stop()
            time.sleep(0.2)
            i = i - 1
        else:
            m1.run_timed(speed_sp = -speed * 100, time_sp=120)
            m2.run_timed(speed_sp = -speed * 100, time_sp=120)
            m3.stop()

def line_detected():
    #table is about 60, white paper is about 90
    return cs.reflected_light_intensity > 75
    
def left_turn(speed, time):
    m1.run_timed(speed_sp = -speed * 100, time_sp=time)
    m2.run_timed(speed_sp = speed * 100, time_sp=time)
    m3.run_timed(speed_sp = -speed * 100, time_sp=time)

def right_turn(speed, time):
    m1.run_timed(speed_sp = speed * 100, time_sp=time)
    m2.run_timed(speed_sp = -speed * 100, time_sp=time)
    m3.run_timed(speed_sp = speed * 100, time_sp=time)

def find_line(attempts = 0):
    # Determine iteration number
    # If first attempt, set iteration to 3
    # for minor changes on a straight line
    if attempts == 0:
        iterations = 3
        attempts = 0.5
    else:
        iterations = int(attempts * 10)

    # Turn left first
    for i in range(iterations):
        while way_blocked():
            m1.stop()
            m2.stop()
            m3.stop()
        if (line_detected()):
            motortime = 1000
            return
        left_turn(speed + 2 * attempts, 120)
        time.sleep(0.1)

    # Back to original angle and then turn right
    for i in range(iterations * 2):
        while way_blocked():
            m1.stop()
            m2.stop()
            m3.stop()
        if (line_detected()):
            motortime = 1000
            return
        right_turn(speed + 2 * attempts, 120)
        time.sleep(0.1)

    # Back to original angle
    for i in range(iterations):
        while way_blocked():
            m1.stop()
            m2.stop()
            m3.stop()
        if (line_detected()):
            motortime = 1000
            return
        left_turn(speed + 2 * attempts, 120)
        time.sleep(0.1)

    # Increase search space
    find_line(attempts + 0.5)

def way_blocked():
    distance = us.value() / 10  # convert mm to cm
    return distance < 6
    

def main():
    while True:
        try:
            if (not line_detected()):
                find_line()
            forward()
            
        except Exception as e:
            print(e)
            pass

main()
