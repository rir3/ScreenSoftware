from queue import Queue

q = Queue()
q.put(1)
q.put(2)
q.put(3)

for i in q.queue:
    print(i)


while not q.empty():
            print(q.get())

print(q.empty())