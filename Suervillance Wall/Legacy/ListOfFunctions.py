def print_apple():
    print("apple")

def print_banana():
    print("banana")

def print_cherry():
    print("cherry")

thislist = [print_apple, print_banana, print_cherry]

thislist[2]()

start_index = 0
end_index = len(thislist)
while True:
    thislist[start_index]()
    start_index = start_index + 1
    if(start_index == end_index):
        start_index = 0