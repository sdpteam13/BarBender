import socket

def send(message):
    s = socket.socket()
    s.connect(('192.168.105.91',25565))
    s.send(message.encode())
    s.close()