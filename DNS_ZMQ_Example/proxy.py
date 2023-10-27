import zmq


def main():
    context = zmq.Context()

    # Socket facing clients
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:5559")

    # Socket facing services
    backend = context.socket(zmq.DEALER)
    backend.bind("tcp://*:5560")

    zmq.proxy(frontend, backend)

    frontend.close()
    backend.close()
    context.term()


if __name__ == "__main__":
    main()
