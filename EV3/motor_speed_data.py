import ev3dev.ev3 as ev3
import time

m1 = ev3.LargeMotor('outA')
m2 = ev3.LargeMotor('outD') #right motor

test_time = 10000
speed = 300

m1.run_timed(speed_sp = -speed, time_sp = test_time)
m2.run_timed(speed_sp = -speed, time_sp = test_time)

for i in range(0, test_time // 100):
    print(m1.speed, m2.speed)
    time.sleep(0.1)