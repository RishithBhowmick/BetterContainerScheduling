import socket
from time import sleep 
from datetime import datetime
#HOST = socket.gethostbyname('busy_mclean')
HOST = "localhost"
PORT = 5000

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
	print(datetime.now())
	s.connect((HOST,PORT))
	s.sendall(b'Sent from client')
	data = s.recv(1024)
	print(datetime.now())
print('received data')
