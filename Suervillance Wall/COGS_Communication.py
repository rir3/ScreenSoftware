import serial
import time
from queue import Queue
import threading
import serial.tools.list_ports

def both():
	while True:
		val = input("Enter a value (0/1): ")
		ser.write(str.encode(val))     #send the value as integer to the Arduino
		print(f"Sent value: {val}")

		#read the response from the Arduino
		response = ser.readline().decode('utf-8').strip()
		print(f"Received response: {response}")

def write(serialPort, action, status, ser):
	#ser = serial.Serial(serialPort, 9600)# open serial port, change the port name as per your system

	#val = input("Enter a value (0/1): ")
	ser.write(str.encode(action))#send the value as integer to the Arduino
	#time.sleep(.25)
	
	print(f"Sent value: {action}")

	response = ser.readline().decode('utf-8').strip()
	print(f"Received response: {response}")
	if response == status:
		#ser.close() 
		return True
	else:
		return False
	#response = ser.readline().decode('utf-8').strip()
	#print(f"Received response: {response}")
    #response = ser.readline().decode('utf-8').strip()
    #print(f"Received response: {response}")

def read(serialPort, status, ser):
	#ser = serial.Serial(serialPort, 9600)  # open serial port, change the port name as per your system

	# read the response from the Arduino	
	response = ser.readline().decode('utf-8').strip()
	#print(f"Received response: {response}")
	
	if response == status:
		#print(response)
		#ser.close()  # close the serial port
		return True
	else:
		#ser.close()
		return False

def find_arduino(port=None):
    """Get the name of the port that is connected to Arduino."""
    if port is None:
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if p.manufacturer is not None and "Arduino" in p.manufacturer:
                port = p.device
    return port

def comms(tasks, statuses):
	port = find_arduino()
	common_status = "N/A"
	ser = serial.Serial(port, 9600)#Maybe try/catch here

	while True:
		time.sleep(0.05) #(20 fps)

		if tasks.empty():
			response = ser.readline().decode('utf-8').strip()
			if response !=  common_status:
				print("RES:", response)
				statuses.put(response)
		else:
			while not tasks.empty():
				ser.write(str.encode(tasks.get()))

def comms_helper(tasks, statuses):
	comms_thread = threading.Thread(target=comms, args=(tasks, statuses))
	comms_thread.start()





#arduinoPort = '/dev/tty.usbmodem14201'	    
#write(arduinoPort, "3")
#arduinoPort = 'COM3'
#ser = serial.Serial(arduinoPort, 9600)
#foo = write(arduinoPort, "4", "Good Ending", ser)

#while(foo == False):
#	foo = write(arduinoPort, "4", "Good Ending", ser)
