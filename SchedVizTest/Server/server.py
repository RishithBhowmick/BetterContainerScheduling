#!/usr/bin/env python3
from os import getpid
from subprocess import call
import socket
from sys import stdout
import time
from uptime import uptime

print(socket.gethostname())
HOST = socket.gethostname()
PORT = 4000
  
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
	s.bind((HOST,PORT))
	s.listen()
	a=1
	while True:
		conn,addr = s.accept()
		print("recieved at: ", uptime())
		print(a,')')
		a=a+1
		with conn:
			data = conn.recv(1024)
			
			#for i in range(0,1000):
			#	for j in range(0,1000):
			#		for k in range(0,100):
			#			i*j*k
			
			i=10*20*30

			if not data:
				break
			conn.sendall(b'acknowledged')
			print("sent at: ", uptime())
			print()
			stdout.flush()

			

