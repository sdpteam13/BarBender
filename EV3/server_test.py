import socketserver
import time
from robot import Robot

robot = Robot()

class EchoRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # Echo the back to the client
        data = self.request.recv(1024)
        st = data.decode('utf8')
        print (st)
        if st == "close":
            self.socket.close()
            exit()
        if st == "w":
            robot.straight_line_moving()
        if st == "s":
            robot.stop()
        self.request.send(data)
        return

if __name__ == '__main__':
    import socket
    import threading

    address = ('0.0.0.0', 0) # let the kernel give us a port
    server = socketserver.TCPServer(address, EchoRequestHandler)
    ip, port = server.server_address # find out what port we were given
    print ("ip: " + str(ip))
    print ("port: " + str(port))

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True) # don't hang on exit
    t.start()
    
    while True:
        time.sleep(1)
