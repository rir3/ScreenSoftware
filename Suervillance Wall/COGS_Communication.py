import serial
import time

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


#arduinoPort = '/dev/tty.usbmodem14201'	    
#write(arduinoPort, "3")
#arduinoPort = 'COM3'
#ser = serial.Serial(arduinoPort, 9600)
#foo = write(arduinoPort, "4", "Good Ending", ser)

#while(foo == False):
#	foo = write(arduinoPort, "4", "Good Ending", ser)
