import ev3dev.ev3 as ev3
import time

m1 = ev3.LargeMotor('outA')
m2 = ev3.LargeMotor('outD')

speed_m1 = 100
speed_m2 = 100
go = 0
turn = 0

while True:
    direction = input()
    if (direction == 'w' and go < 9):
        go = go + 1
    elif (direction == 's' and go > -9):
        go = go - 1
    elif (direction == 'a' and turn != -1):
        turn = turn - 1
    elif (direction == 'd' and turn != 1):
        turn = turn + 1
    elif (direction == 'x'):
        m1.stop()
        m2.stop()
        go = 0
        turn = 0

    if (turn == 0):
        m1.run_forever(speed_sp=go * 100)
        m2.run_forever(speed_sp=go * 100)
    elif (turn == -1):
        m1.run_forever(speed_sp=-400)
        m2.run_forever(speed_sp=400)
    elif (turn == 1):
        m1.run_forever(speed_sp=400)
        m2.run_forever(speed_sp=-400)
