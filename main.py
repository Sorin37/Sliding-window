import threading
import random
from time import sleep
from queue import Queue
import null as null

message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae libero purus. Ut in ex lorem. Quisque sit amet volutpat mi. Ut eu nibh eu dolor tempus feugiat. Fusce placerat nulla eros, eu sollicitudin nulla porta eget. Integer lacinia, diam vel pellentesque pellentesque, libero velit aliquet odio, sed iaculis neque dolor sed risus. Donec quis ultrices lorem. Etiam risus justo, ullamcorper at ornare et, pretium ultricies ligula. Maecenas suscipit varius varius. Duis viverra nisl et elit pharetra, vitae auctor velit malesuada. Nullam finibus ut sem sed porttitor. Nam egestas nisi nec metus rhoncus consequat."
initial_message_length = len(message) // 2


class myThread(threading.Thread):
    def __init__(self, name, queue):
        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue
        self.message_received = ""

    def run(self):
        send(ip_package, self.name, self.queue, self.message_received)


def send(pack, name, queue, message_received):
    global message
    while pack.fin != 1:
        sleep(random.random() * 5)
        pack.ack = 1
        print(name)
        print("x:", pack.x, "syn:", pack.syn, "ack:", pack.ack, "fin:", pack.fin, "f:", pack.f)
        if name == "Source" and pack.f != 0 and queue.empty():
            pack.x += 1
            print("Message sent:", message[:pack.f])
            queue.put(message[:pack.f])
            message = message[pack.f:]
        if name == "Destination":
            if not queue.empty():
                pop = queue.get()
                print("Message received:", pop)
                message_received = message_received + pop[:]
            pack.f = random.randint(0, initial_message_length)
            pack.x = len(message_received)
        pack.syn = 1
        if len(message) == 0:
            pack.fin = 1
            if name == "Destination":
                print("Final message:", message_received)
        print()


class Ip_package:
    def __init__(self, x, syn, ack, fin, f):
        self.x = x
        self.syn = syn
        self.ack = ack
        self.fin = fin
        self.f = f


ip_package = Ip_package(0, 0, 0, 0, 0)

if __name__ == '__main__':
    q = Queue()
    source = myThread("Source", q)
    destination = myThread("Destination", q)

    source.start()
    destination.start()
