import ev3dev.ev3 as ev3
import time

m1 = ev3.LargeMotor('outA')
m2 = ev3.LargeMotor('outD')
m3 = ev3.LargeMotor('outC')
cs = ev3.ColorSensor('in4')
us = ev3.UltrasonicSensor('in2')
gs = ev3.GyroSensor('in3')
us.mode='US-DIST-CM'

while True:
    print(gs.rate)
    print(gs.angle)
    time.sleep(1)