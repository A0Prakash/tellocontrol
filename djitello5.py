import signal
import pygame
import time
import socket
import cv2
import subprocess
import os
import keyboard

tello_address = ("192.168.10.1", 8889)
pc_address = ("", 8080)
pc_server_address = ("", 11111)

def setupserver(address):
	try:
		sname = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sname.bind(address)
	except socket.error as msg:
		print("Failed to bind: " + str(msg))
	return sname

def setupfile(filename, mode):
	try:
		file = open(filename, mode)
	except IOError:
		print("Could not open file.")
	return file


def setupsocket(address):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		sock.bind(address)
	except socket.error as msg:
		print("Binding error: " + str(msg))
	return sock

def sendcommand(command, s, addr):
	try:
		command = command.encode()
		sent = s.sendto(command, addr)
	except socket.error as msg:
		print("Error sending message: " + str(msg))
		print(str(sent))

def recieve(s):
	bytes, address = s.recvfrom(1024)
	bytes = bytes.decode('utf-8')
	if address == tello_address:
		print("Recieved message from tello: " + bytes)
	else:
		print("Message from: " + str(address) + bytes)

def recieve_video():
	try:
		video = cv2.VideoCapture("udp://0.0.0.0:11111")
	except Exception as err:
		pass
	while True:
		try:
			ret, frame = video.read()
			if ret:
				cv2.imshow("stream", frame)
				cv2.waitKey(1)
		except Exception as err:
			cv2.destroyAllWindows()
			video.release()
			break

def thread_test():
	while True:
		print("Hi, my name is therad")
		time.sleep(5)

s = setupsocket(pc_address)

sendcommand("command", s, tello_address)
print("sent command")
recieve(s)
#sendcommand("streamon", s, tello_address)
#print("sent streamon")
#recieve(s)
#sendcommand("takeoff", s, tello_address)



while True:
	message = input()
	if message == "quit":
		os.killpg(os.getpgid(child.pid), signal.SIGTERM)
		break
	elif message == "streamon":
		#open djitello6.py
		sendcommand(message, s, tello_address)
		recieve(s)
		child = subprocess.Popen("python3 djitello6.py",stdout = subprocess.PIPE, shell = True, preexec_fn=os.setsid)
		
	if message == "rcgo":
		break
	sendcommand(message, s, tello_address)
	recieve(s)

#command_thread()

i = False

while True:
	in1 = input()
	keyboard.press("enter")
	if in1 == "a":
		sendcommand("rc -100 0 0 0", s, tello_address)
		i = True
	elif in1 == "s":
		sendcommand("rc 0 -100 0 0", s, tello_address)
		i = True
	elif in1 == "d":
		sendcommand("rc 100 0 0 0", s, tello_address)
		i = True
	elif in1 == "w":
		sendcommand("rc 0 100 0 0", s, tello_address)
		i = True				
	elif in1 == "e":
		sendcommand("emergency", s, tello_address)
	elif in1 == "q":
		break
	elif in1 == ";":
		sendcommand("rc 0 0 50 0", s, tello_address)
		i = True
	elif in1 == ".":
		sendcommand("rc 0 0 -50 0", s, tello_address)
		i = True
	elif in1 == "]":
		sendcommand("rc 0 0 0 100", s, tello_address)
		i = True
	elif in1 == "[":
		sendcommand("rc 0 0 0 -100", s, tello_address)
		i = True					
	elif in1 == "l":
		sendcommand("land", s, tello_address)
	elif in1 == "t":
		sendcommand("takeoff", s, tello_address)
	else:
		if i == True:
			sendcommand("rc 0 0 0 0", s, tello_address)
			i = False
		else:
			pass
	time.sleep(0.075)
