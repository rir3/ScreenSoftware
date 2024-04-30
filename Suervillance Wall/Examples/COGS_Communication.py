import serial #pyserial
from queue import Queue
import threading
import serial.tools.list_ports
#virtualserialports -l 1

def find_arduino(port=None):
    """Get the name of the port that is connected to Arduino."""
    if port is None:
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if p.manufacturer is not None and "Arduino" in p.manufacturer:
                port = p.device
    return port

def comms(tasks, statuses):
	port = "/dev/ttys016"
	common_status = "N/A"
	ser = serial.Serial(port, 9600, timeout=1)#Maybe try/catch here

	while True:
		if tasks.empty():
			response = ser.readline().decode('utf-8').strip()
			if response:
				print("RES:", response)
				statuses.put(response)
		else:
			while not tasks.empty():
				to_write = tasks.get()
				print("SENT:", to_write)
				ser.write(str.encode(to_write))

def comms_helper(tasks, statuses):
	comms_thread = threading.Thread(target=comms, args=(tasks, statuses))
	comms_thread.start()

tasks = Queue()
statuses = Queue()
comms(tasks,statuses)