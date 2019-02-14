#touch sensor on in1
#DC grabber motor on outB
#lift motor on outD

#commands:
#up, down, grab, release, stop

#vars:
liftspeed = 300
lifttimemax = 2000 #ms
grabtime = 500 #ms


import ev3dev.ev3 as ev3
import time

p = ev3.LegoPort('outB')
assert p.connected
p.mode = 'dc-motor'
 
time.sleep(1)

lift = ev3.LargeMotor("outD")
grab = ev3.DcMotor("outB")
touch = ev3.TouchSensor("in1")

lift.stop_action = "brake" #Stop the lift as fast as possible

print("started")

while True:
    cmd = input()
    if (cmd == "up"):
        #lift until overloaded
        lift.run_timed(speed_sp = -liftspeed, time_sp = lifttimemax)
        time.sleep(0.1) #Motor is overloaded while ramping
        lift.wait_until("overloaded", timeout = lifttimemax)
        lift.stop()
        
    elif (cmd == "down"):
        #down until button pressed, overloaded, or timeout
        lift.run_timed(speed_sp = liftspeed, time_sp = lifttimemax)
        time.sleep(0.1) #Motor is overloaded while ramping
        while not (touch.is_pressed or "overloaded" in lift.state or not "running" in lift.state):
            pass
        lift.stop()
        
    elif (cmd == "grab"):
        #Grab for a little longer than release
        grab.run_timed(duty_cycle_sp = 100, time_sp = grabtime * 1.5)
        time.sleep(grabtime * 1.5 / 1000)
    
    elif (cmd == "release"):
        grab.run_timed(duty_cycle_sp = -100, time_sp = grabtime)
        time.sleep(grabtime / 1000)
    