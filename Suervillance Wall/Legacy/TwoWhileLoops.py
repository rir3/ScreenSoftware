import threading

def loop1():
    while True:
        # Code for loop 1 goes here
        print("Loop 1")

def loop2():
    while True:
        # Code for loop 2 goes here
        print("Loop 2")

# Create and start the first thread
thread1 = threading.Thread(target=loop1)
thread1.start()

# Create and start the second thread
thread2 = threading.Thread(target=loop2)
thread2.start()
