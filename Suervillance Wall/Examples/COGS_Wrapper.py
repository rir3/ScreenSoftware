import threading
import COGS_Communication
import time


arduinoPort = '/dev/tty.usbmodem14201'
status = "Show Login"

def serialRead(arduinoPort, status):
	while True:
		#print("donkey")
		foundStatus = COGS_Communication.read(arduinoPort, status)
		#print(foundStatus)
		if foundStatus:
			print("Found: " + status)
			break

def setup():
	thread = threading.Thread(target=loop)
	thread.start()

	if thread.is_alive():
		return False
	else:
		return True

print("Hello1")
print(setup())
print("Hello2")