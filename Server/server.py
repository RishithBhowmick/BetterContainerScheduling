#!/usr/bin/env python3
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
	while True:
		conn,addr = s.accept()
		print("received at: uptime()")
		stdout.flush()
		call(["insmod","trace.ko"])
		with conn:
			print("connected by",addr)
			data = conn.recv(1024)
			time.sleep(5)
			if not data:
				break
			conn.sendall(b'acknowledged')
			print("sent at: uptime()")
			stdout.flush()
			call(["rmmod","trace.ko"])
			

