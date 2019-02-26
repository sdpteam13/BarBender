import ev3dev.ev3 as ev3
import time

# DC motor
p = ev3.LegoPort('outB')
assert p.connected
p.mode = 'dc-motor'
time.sleep(1)

# motors and sensors
lift_motor = ev3.LargeMotor('outA')
grab_motor = ev3.DcMotor('outB')
lift_sensor = ev3.TouchSensor('in1')
grab_sensor = ev3.TouchSensor('in2')
robot_sensor = ev3.UltrasonicSensor('in3')
robot_sensor.mode='US-DIST-CM'


class cup_dispenser:

    def __init__(self):
        self.initialise()

    # go to the initialisation spot
    def initialise(self):
        self.grab_reset()
        self.lift_reset()
    
    # close the grabber
    def grab_reset(self):
        while not grab_sensor.is_pressed:
            grab_motor.run_timed(duty_cycle_sp=75, time_sp=100)
        grab_motor.stop()

    # lift goes down
    def lift_reset(self):
        while not lift_sensor.is_pressed:
            lift_motor.run_timed(speed_sp=250, time_sp=100)
        lift_motor.stop()

    # open the grabber
    def grab_open(self):
        grab_motor.run_timed(duty_cycle_sp=-100, time_sp=800)
        
    # close the grabber but pose more force in order to grab the cup
    def grab_close(self):
        grab_motor.run_timed(duty_cycle_sp=100, time_sp=870)
        time.sleep(0.9)
        if grab_sensor.is_pressed:
            grab_motor.stop()

    # lift goes up
    def lift_up(self):
        lift_motor.run_timed(speed_sp=-300, time_sp=1350)

    # grab an empty cup
    def lift_and_grab(self):
        self.grab_open()
        time.sleep(2)
        self.lift_up()
        time.sleep(2)
        self.grab_close()
        time.sleep(2)
        self.lift_reset()
        time.sleep(2)
        self.grab_open()
        time.sleep(5)
    
    def run(self):
        self.lift_and_grab()

if __name__ == '__main__':
    c = cup_dispenser()
    '''while True:
        if robot_sensor.value() / 10 > 6:
            c.initialise()
            c.run()
        time.sleep(2)'''
    c.run()
    c.initialise()
