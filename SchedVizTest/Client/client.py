import socket
from time import sleep 

HOST = socket.gethostbyname('ipc_server_dns_name')
PORT = 4000

while True:
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
		sleep(0.1)
		s.connect((HOST,PORT))
		s.sendall(b'Sent from client')
		data = s.recv(1024)
	print('received data')
