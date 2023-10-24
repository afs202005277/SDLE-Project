import zmq

from DatabaseManagement import DatabaseManagement
from HashingRing import HashingRing


class Server:

    def __init__(self):
        self.db_management = DatabaseManagement()
        num_primary_cons = self.db_management.get_num_primary_connections()
        self.hashing_ring = HashingRing(num_primary_cons)
        self.request_handlers = {'AddItem': self.add_item, 'BuyItem': self.buy_item, 'CreateList': self.create_list,
                                 'DeleteList': self.delete_list}
        self.db_forbidden_parameters = ['token', 'type']

    def remove_attributes(self, json_obj):
        if isinstance(json_obj, dict):
            # Remove dictionary keys
            for key in list(json_obj.keys()):
                if key in self.db_forbidden_parameters:
                    json_obj.pop(key)
            for key, value in json_obj.items():
                json_obj[key] = self.remove_attributes(value)
        elif isinstance(json_obj, list):
            # Remove attributes from list items (recursively)
            json_obj = [self.remove_attributes(item) for item in json_obj]
        return json_obj

    def add_item(self, request):
        list_id = request["list_id"]
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        list_object = self.db_management.retrieve_list(main_database_id, list_id)
        items = list_object['items']
        items.append({'name': request['name'], 'quantity': request['quantity']})
        list_object['items'] = items
        self.db_management.replace_list(main_database_id, list_object)
        print("Success!")
        print(self.db_management.retrieve_list(main_database_id, list_id))

    def buy_item(self, request):
        list_id = request["list_id"]
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        list_object = self.db_management.retrieve_list(main_database_id, list_id)
        items = list_object['items']
        new_items = []
        for item in items:
            if item['name'] == request['name']:
                item['quantity'] = 0
            new_items.append(item)
        list_object['items'] = new_items
        self.db_management.replace_list(main_database_id, list_object)
        print("Success!")
        print(self.db_management.retrieve_list(main_database_id, list_id))

    def create_list(self, request):
        list_id = self.db_management.next_id
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        self.db_management.insert_list(main_database_id, request)
        print("Success!")
        print(self.db_management.retrieve_list(main_database_id, list_id))

    def delete_list(self, request):
        main_database_id = self.hashing_ring.find_main_database_id(request["list_id"])
        self.db_management.delete_list(main_database_id, request["list_id"])
        print("Success!")
        print(self.db_management.retrieve_list(main_database_id, request["list_id"]))

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.connect("tcp://localhost:5560")

        while True:
            request = socket.recv_json()
            response = self.request_handlers[request['type']](self.remove_attributes(request))
            socket.send_json(response)


if __name__ == '__main__':
    server = Server()
    server.run()

