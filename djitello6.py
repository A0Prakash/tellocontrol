import cv2
import socket

tello_address = ("", 8890)

sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock1.bind(tello_address)

def recieve():
	bytes, address = sock1.recvfrom(1024)
	bytes = bytes.decode("utf-8")
	if address == tello_address:
		print("message from tello:" + bytes)
	else:
		print("msg from" + address + ":" + bytes)	


try:
	video = cv2.VideoCapture("udp://0.0.0.0:11111")
except Exception as err:
	print(err)
while True:
	try:
		ret, frame = video.read()
		if ret:
			cv2.imshow("stream", frame)
			cv2.waitKey(1)
	except Exception as err:
		cv2.destroyAllWindows()
		video.release()
		print(err)
		break
		
