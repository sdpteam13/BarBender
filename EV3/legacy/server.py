import socketserver
import time
import requests
import robot_interface as rob
exit()
class EchoRequestHandler(socketserver.BaseRequestHandler):

    def process_commands(self,c):
        commands = c.split(',')
        return commands

    def handle(self):
        # Echo the back to the client
        data = self.request.recv(1024)
        st = data.decode('utf8')
        st = self.process_commands(st)
        print(st)
        for c in st:
            if (c == 'r'):
                rob.turn_right()
            elif(c == 'l'):
                rob.turn_left()
            elif (c == 'follow_line'):
                rob.follow_line()
            elif c == 'f':
                rob.follow_line_until_intersection()
            elif c[:4] == 'turn':
                rob.turn(float(st[4:]))
            elif c == 'go':
                rob.go()
            elif st[:9] == 'set_speed':
                rob.set_speed(int(st[9:]))
            elif c == 't':
                rob.turn_around()
            elif c == 'stop':
                rob.stop()
            else:
                rob.stop()
        requests.post('http://192.168.105.142/EV3/')
        return

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
