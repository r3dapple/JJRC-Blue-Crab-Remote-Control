# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 21:10:10 2018

Project: JJRC Blue Crab Control
@author: r3dapple
"""

import socket
import binascii
import time
import sys
from pynput.keyboard import Key, Listener
from _thread import *

#Uncomment for Linux
#from signal import signal, SIGPIPE, SIG_DFL
#signal(SIGPIPE,SIG_DFL)


CALIBRAION = binascii.unhexlify(b'ff087e3f403fd0121200cb') # ff08 7e3f 403f d012 1200 cb

IP = '172.16.10.1'
IP2 = 'localhost'
UDPPORT = 8080
TCPPORT = 8888
UDPPORT2 = 5555
UDPPORT3 = 1234
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

#Windows pipeline
#gst-launch-1.0 udpsrc port=5555 ! h264parse ! avdec_h264 ! videoconvert ! autovideosink sync=false

#Linux pipeline
#python3 drone.py | gst-launch-1.0 fdsrc fd=0 ! h264parse ! avdec_h264 ! videoconvert ! xvimagesink sync=false

while 1:
	try:
		s3.connect((IP2, UDPPORT2))
		#Uncomment for Windows
		#s4.bind((IP2, UDPPORT3))
		s.connect((IP, UDPPORT))
		s2.connect((IP, TCPPORT))
		print("connected")
		break
	except:
		continue
	
def stream(x):
	while 1:
		try:
			s2.send(binascii.unhexlify(b'000102030405060708092828'))
			#Uncomment for Windows
			#s3.send(s2.recv(1024))
			#Uncomment for Linux
			#print(s2.recv(1024))
		except:
			continue
	
	
data = b'ff087e3f403f9012120007' # CALIBRATED IDLE PACKAGE

def keylistener(c):
	def on_press(key):
		global data
		inp = str(key)[1:2]
		data = b'ff087e3f403f9012120007'
		if inp == "q": #arm
			data = b'ff087e3f403f90121240c7'
			return
		if inp == "e": #up
			data = b'ff08fc3f403f9012120089'
			return
		if inp == "r": #down
			data = b'ff08003f403f9012120085'
			return
		if inp == "w": #forwards
			data = b'ff087e3f013f9012120046'
			return
		if inp == "s": #backwards
			data = b'ff087e3f7f3f90121200c8'
			return
		if inp == "a": #left
			data = b'ff087e3f40009012120046'
			return
		if inp == "d": #right
			data = b'ff087e3f407e90121200c8'
			return
		if inp == "z": #stop
			data = b'ff087e3f403f901212a069'
			return
		if inp == "y": #disarm
			data = b'ff087e3f403f9012128087'
			return
		if inp == "1": #left turn
			data = b'ff087e00403f9012120046'
			return
		if inp == "3": #right turn
			data = b'ff087e7e403f90121200c8'
			        
			return
		
	with Listener(on_press=on_press) as listener:
		listener.join()
		

def sendPackage():
	while 1:
		global data
		for n in range(0,100):
			#print("Sending PACKAGE: " + data.decode())
			#print(binascii.unhexlify(data))
			s.send(binascii.unhexlify(data))
			#print("\n\n")
			time.sleep(0.03)
		data = b'ff087e3f403f9012120007'


# Send calibration first
for n in range(0,100):
	print("Sending CALIBRAION...ff087e3f403fd0101000cb")
	s.send(CALIBRAION)
	time.sleep(0.05)

start_new_thread(keylistener,("",))
start_new_thread(stream,("",))
start_new_thread(control,("",))
sendPackage()
	

s.close()
