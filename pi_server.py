from socket import *
from time import ctime
import RPi.GPIO as GPIO

ctrCmd = [] #commands

#TCP-IP communication initialization
HOST = '' # Need to be empty --> all client can communicate with the server
PORT = #should be the same in client port
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
	print("Waiting for connection")
	tcpCliSock.addr = tcpSerSock.accept()
	print("...connected from : {}").format(addr)
	try:
		while True:
			data = ''
			data = tcpCliSock.recv(BUFSIZE)
			if not data:
				break
			# place for commands
	except KeyboardInterrupt:
		GPIO.cleanup()
tcpSerSock.close()