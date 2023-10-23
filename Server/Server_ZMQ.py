import zmq

from Server.DatabaseLoadBalancer import DatabaseLoadBalancer
from Server.DatabaseManagement import DatabaseManagement
from Server.HashingRing import HashingRing


class Server:

    def __init__(self):
        self.db_management = DatabaseManagement()
        num_primary_cons = self.db_management.get_num_primary_connections()
        num_replicas_per_group = self.db_management.get_num_replicas_connections()
        self.hashing_ring = HashingRing(num_primary_cons)
        self.db_load_balancer = DatabaseLoadBalancer(num_primary_cons, num_replicas_per_group)
        self.request_handlers = {'AddItem': self.add_item, 'BuyItem': self.buy_item, 'CreateList': self.create_list,
                                 'DeleteList': self.delete_list}

    def add_item(self, request):
        pass

    def buy_item(self, request):
        pass

    def create_list(self, request):
        pass

    def delete_list(self, request):
        pass

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.connect("tcp://localhost:5560")

        while True:
            request = socket.recv_json()
            response = self.request_handlers[request['type']](request)
            socket.send_json(response)


if __name__ == '__main__':
    server = Server()
    server.run()
