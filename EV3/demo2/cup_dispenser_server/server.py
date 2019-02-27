print ("server starting...")

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
        self.lift_reset()
        self.grab_reset()
        self.grab_open()
        time.sleep(1)
        self.lift_up()
        time.sleep(2)
    
    # calibrate, close the grabber
    def grab_reset(self):
        while not grab_sensor.is_pressed:
            grab_motor.run_timed(duty_cycle_sp=-100, time_sp=100)
        grab_motor.stop()

    # lift goes down
    def lift_reset(self):
        while not lift_sensor.is_pressed:
            lift_motor.run_timed(speed_sp=600, time_sp=80)
        lift_motor.stop()

    # open the grabber
    def grab_open(self):
        grab_motor.run_timed(duty_cycle_sp=100, time_sp=800)
        
    # close the grabber but pose more force in order to grab the cup
    def grab_close(self):
        grab_motor.run_timed(duty_cycle_sp=-100, time_sp=1300)
        time.sleep(0.9)
        if grab_sensor.is_pressed:
            grab_motor.stop()

    # lift goes up
    def lift_up(self):
        lift_motor.run_timed(speed_sp=-300, time_sp=1250)

    # grab an empty cup
    def grab_and_down(self):
        self.grab_close()
        time.sleep(2)
        self.lift_reset()
        time.sleep(2)
        self.grab_open()
        time.sleep(2)
        self.lift_up()
        time.sleep(2)

class EchoRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # Echo the back to the client
        data = self.request.recv(1024)
        st = data.decode('utf8')
        print(st)
        cp = cup_dispenser()
        cp.grab_and_down()
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

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True) # don't hang on exit
    t.start()

    while True:
        time.sleep(1)
