import socketserver
import time
from robot import Robot

class EchoRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self):
        self.robot = Robot()
        self.motor_speed = 100
        self.status = ' '

    def handle(self):
        # Echo the back to the client
        data = self.request.recv(1024)
        st = data.decode('utf8')
        print (st)
        if st == "close":
            self.socket.close()
            self.robot.stop()
            exit()

        if (st == 'r'):
            # speed up
            if (self.motor_speed < 900):
                self.motor_speed += 50
        elif(st == 'f'):
            # speed down
            if (self.motor_speed > 0):
                self.motor_speed -= 50
        else:
            self.status = st

        if (self.status == 'w'):
            self.robot.straight_line_moving(speed = motor_speed)
        elif(self.status == 's'):
            self.robot.straight_line_moving(speed = -motor_speed)
        elif(self.status == 'a'):
            self.robot.rotate_left()
        elif(self.status == 'd'):
            self.robot.rotate_right()
        else:
            self.robot.stop()

        self.request.send(data)

if __name__ == '__main__':
    import socket
    import threading

    address = ('0.0.0.0', 12345) # let the kernel give us a port
    server = socketserver.TCPServer(address, EchoRequestHandler)
    ip, port = server.server_address # find out what port we were given
    print ("ip: " + str(ip))
    print ("port: " + str(port))

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True) # don't hang on exit
    t.start()

    while True:
        time.sleep(1)
