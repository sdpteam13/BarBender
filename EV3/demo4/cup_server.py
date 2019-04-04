print ("Cup dispenser server starting...")

import socketserver
import ev3dev.ev3 as ev3
import time

# DC motor
p = ev3.LegoPort('outB')
assert p.connected
p.mode = 'dc-motor'
time.sleep(1)

# motors and sensors
lift_motor = ev3.LargeMotor('outD')
grab_motor = ev3.DcMotor('outB')
lift_sensor = ev3.TouchSensor('in1')
grab_sensor = ev3.TouchSensor('in2')

lift_motor.stop_action='brake'

class cup_dispenser:

    '''def __init__(self):
        self.initialise()'''

    # go to the initialisation spot
    def initialise(self):
        self.lift_down()
        self.grab_reset()
        self.grab_open()
        self.lift_up()
    
    # calibrate, close the grabber
    def grab_reset(self):
        while not grab_sensor.is_pressed:
            grab_motor.run_timed(duty_cycle_sp=100, time_sp=100)
        grab_motor.stop()

    # lift goes down
    def lift_down(self):
        while not lift_sensor.is_pressed:
            lift_motor.run_timed(speed_sp=450, time_sp=80)
        lift_motor.stop()
        time.sleep(0.2)

    # open the grabber
    def grab_open(self):
        grab_motor.run_timed(duty_cycle_sp=-100, time_sp=450)
        time.sleep(1)
        
    # close the grabber but pose more force in order to grab the cup
    def grab_close(self):
        grab_motor.run_timed(duty_cycle_sp=100, time_sp=1100)
        time.sleep(1.5)

    # open the grab more to avoid robot collision
    def grab_open_more(self):
        grab_motor.run_timed(duty_cycle_sp=-100, time_sp=300)
        print('a')
        time.sleep(1)

    # return to previous position after grab_open_more()
    def grab_close_more(self):
        grab_motor.run_timed(duty_cycle_sp=100, time_sp=300)
        print('b')
        time.sleep(1)

    # lift goes up
    def lift_up(self):
        lift_motor.run_timed(speed_sp=-450, time_sp=850)
        time.sleep(1)

    def cup_grab_fail(self):
        grab_motor.run_timed(duty_cycle_sp=100, time_sp=400)
        time.sleep(.4)
        return grab_sensor.is_pressed
    
    # grab an empty cup
    def grab_and_down(self):
        self.grab_close()
        self.lift_down()
        #time.sleep(1)
        # grab to check if there is a cup grabbed
        if self.cup_grab_fail():
            #no cup, try again
            self.grab_open()
            self.lift_up()
            self.grab_and_down()
            return
        
        self.grab_open()
        self.lift_up()

class EchoRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # Echo the back to the client
        data = self.request.recv(1024)
        st = data.decode('utf8')
        print(st)
        cp = cup_dispenser()
        cp.grab_close_more()
        cp.grab_and_down()
        cp.grab_open_more()
        return

if __name__ == '__main__':
    import socket
    import threading

    address = ('0.0.0.0', 25565) # that'SSSsss a nice port you have there
    server = socketserver.TCPServer(address, EchoRequestHandler)
    ip, port = server.server_address # find out what port we were given
    print ("server started!")
    print ("ip: " + str(ip))
    print ("port: " + str(port))

    cp = cup_dispenser()
    cp.initialise()
    cp.grab_and_down()
    cp.grab_open_more()

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True) # don't hang on exit
    t.start()

    while True:
        time.sleep(1)
