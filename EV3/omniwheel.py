import ev3dev.ev3 as ev3
import time
wheel1=ev3.LargeMotor('outA')
wheel2=ev3.LargeMotor('outD')
#s = int(input("Speed: "))
timeRotation = 300
timeMoving = 1000
speedRotation = -50
speedMoving = -200
while True:
        k=input()
        if (k=='w'):
            wheel1.run_timed(speed_sp=-speedMoving, time_sp=timeMoving)
            wheel2.run_timed(speed_sp=-speedMoving, time_sp=timeMoving)
        elif (k=='s'):
            wheel1.run_timed(speed_sp=speedMoving, time_sp=timeMoving)
            wheel2.run_timed(speed_sp=speedMoving, time_sp=timeMoving)
        elif (k=='a'):
            wheel1.run_timed(speed_sp=-speedRotation, time_sp=timeRotation)
            wheel2.run_timed(speed_sp=speedRotation, time_sp=timeRotation)
        elif (k=='d'):
            wheel1.run_timed(speed_sp=speedRotation, time_sp=timeRotation)
            wheel2.run_timed(speed_sp=-speedRotation, time_sp=timeRotation)
