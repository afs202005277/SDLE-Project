from time import sleep

import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5559")
i = 0
while True:
    i += 1
    socket.send(b"Hello")
    message = socket.recv()
    print(f"Received reply {i} [{message}]")
    sleep(1)
