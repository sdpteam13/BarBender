print ("Drink dispenser server starting...")

import socketserver
import ev3dev.ev3 as ev3
import time

# motors and sensors

class drink_dispenser:
    
    def __init__(self, start_up):
        self.drink_motor_1 = ev3.LargeMotor('outC')
        self.drink_motor_2 = ev3.LargeMotor('outA')

        self.drink_motor_1.stop_action='brake'
        self.drink_motor_2.stop_action='brake'
        
        self.start_up = start_up
        if start_up:
            self.initialise()
            time.sleep(4)
        self.pos_drink_motor_1 = self.drink_motor_1.position
        self.pos_drink_motor_2 = self.drink_motor_2.position
    
    def initialise(self):
        while not self.drink_motor_1.is_overloaded:
            self.drink_motor_1.run_timed(speed_sp=100, time_sp=15)
        while not self.drink_motor_2.is_overloaded:
            self.drink_motor_2.run_timed(speed_sp=100, time_sp=15)
    
    def open(self, motor):
        if motor == self.drink_motor_1:
            motor.run_to_abs_pos(speed_sp=-400, position_sp=self.pos_drink_motor_1 - 80)
        elif motor == self.drink_motor_2:
            motor.run_to_abs_pos(speed_sp=-400, position_sp=self.pos_drink_motor_2 - 80)
    
    def close(self, motor):
        if motor == self.drink_motor_1:
            motor.run_to_abs_pos(speed_sp=-800, position_sp=self.pos_drink_motor_1 + 15)
        elif motor == self.drink_motor_2:
            motor.run_to_abs_pos(speed_sp=-800, position_sp=self.pos_drink_motor_2 + 15)
        time.sleep(2)
        motor.stop()
    
    def drink(self, motor):
        self.open(motor)
        if motor == self.drink_motor_1:
            time.sleep(1)
            #time.sleep(1.8)
        elif motor == self.drink_motor_2:
            time.sleep(1.7)
        self.close(motor)

class EchoRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # Echo the back to the client
        data = self.request.recv(1024)
        st = data.decode('utf8')
        print(st)
        dd = drink_dispenser(start_up=False)
        if st == 'A':
            dd.drink(dd.drink_motor_1)
        elif st == 'B':
            dd.drink(dd.drink_motor_2)
        return

if __name__ == '__main__':
    import socket
    import threading

    address = ('0.0.0.0', 25566) # that'SSSsss a nice port you have there
    server = socketserver.TCPServer(address, EchoRequestHandler)
    ip, port = server.server_address # find out what port we were given
    print ("server started!")
    print ("ip: " + str(ip))
    print ("port: " + str(port))
    
    dd = drink_dispenser(start_up=True)

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True) # don't hang on exit
    t.start()

    while True:
        time.sleep(1)
