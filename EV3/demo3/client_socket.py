import socket

def send(message):
    try:
        s = socket.socket()
        s.connect(('192.168.105.91',25565))
        s.send(message.encode())
        s.close()
    except:
        print ('[ERROR] can\'t connect to cup dispenser')

def send_and_receive(message):
    try:
        s = socket.socket()
        s.connect(('192.168.105.91', 25566))
        s.send(message.encode())
        result = s.recv(1024)
        s.close()
        return result.decode('utf8')
    except:
        print ('[ERROR] can\'t connect to fluid dispenser')
        return ""