#!/usr/bin/env python3
from os import getpid
from subprocess import call
import socket
from sys import stdout
import time
from uptime import uptime

call(["renice","-n","-20","-p",str(getpid())])
#call(["ps","-l",str(getpid())])
print(socket.gethostname())
HOST = socket.gethostname()
PORT = 4000
  
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
	s.bind((HOST,PORT))
	s.listen()
	a=1
	while True:
		conn,addr = s.accept()
		x=uptime()
		print()
		print(a,")")
		a=a+1
		print("received at:", x)
		try:
			call(["insmod","trace.ko"])
		except:
			call(["rmmod","trace.ko"])
			call(["insmod","trace.ko"])
		with conn:
			data = conn.recv(1024)
			for i in range(0,1000):
				for j in range(0,1000):
					for k in range(0,100):
						i*j*k
			if not data:
				break
			conn.sendall(b'acknowledged')
			y = uptime()
			print("sent at: ", y)
			print("diff: ",y-x)
			call(["rmmod","trace.ko"])
			stdout.flush()

			

