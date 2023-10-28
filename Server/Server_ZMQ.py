import zmq
import os
import sys
import json
import hashlib

from jwt import InvalidSignatureError

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(f'{ROOT_DIR}/')

from DatabaseManagement import DatabaseManagement
from AuthenticationManagement import AuthenticationManagement
from HashingRing import HashingRing


class Server:

    def __init__(self):
        self.expiration_date_days = 30
        self.db_management = DatabaseManagement()
        self.authentication_management = AuthenticationManagement()
        num_primary_cons = self.db_management.get_num_connections()
        self.hashing_ring = HashingRing(num_primary_cons)
        self.request_handlers = {
            'AddItem': self.add_item, 
            'BuyItem': self.buy_item, 
            'CreateList': self.create_list,
            'DeleteList': self.delete_list, 
            'DeleteItem': self.delete_item,
            'RenameItem': self.rename_item,
            'GetListHash': self.get_list_hash
        }
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

    def get_list_hash(self, request):
        list_id = DatabaseManagement.get_id(request['list_name'], request['email'])
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        list_object = self.db_management.retrieve_list(main_database_id, list_id)
        if not list_object:
            print("List not Found")
            return
        del list_object['id']
        del list_object['email']

        list_str = json.dumps(list_object).replace(' ', '').replace('\"', '').encode('utf-8')
        return hashlib.md5(list_str).hexdigest()

    def add_item(self, request):
        list_id = DatabaseManagement.get_id(request['list_name'], request['email'])
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        list_object = self.db_management.retrieve_list(main_database_id, list_id)
        if not list_object:
            print("List not Found")
            return
        items = list_object['items']
        found = False
        for item in items:
            if item['name'] == request['name']:
                item['quantity'] += request['quantity']
                found = True
                break

        if not found:
            items.append({'name': request['name'], 'quantity': request['quantity']})

        list_object['items'] = items
        self.db_management.replace_list(main_database_id, list_object)
        print("Success!")
        print(self.db_management.retrieve_list(main_database_id, list_id))

    def buy_item(self, request):
        list_id = DatabaseManagement.get_id(request['name'], request['email'])
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        list_object = self.db_management.retrieve_list(main_database_id, list_id)
        if not list_object:
            print("List not Found")
            return
        items = list_object['items']
        for item in items:
            if item['name'] == request['name']:
                item['quantity'] -= 1

        list_object['items'] = items
        self.db_management.replace_list(main_database_id, list_object)
        print("Success!")
        print(self.db_management.retrieve_list(main_database_id, list_id))

    def create_list(self, request):
        list_id = DatabaseManagement.get_id(request['list_name'], request['email'])
        request["id"] = list_id
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        self.db_management.insert_list(main_database_id, request)
        print("Success!")
        print(self.db_management.retrieve_list(main_database_id, list_id))

    def delete_list(self, request):
        list_id = DatabaseManagement.get_id(request['list_name'], request['email'])
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        self.db_management.delete_list(main_database_id, list_id)
        print("Success!")
        print(self.db_management.retrieve_list(main_database_id, list_id))

    def delete_item(self, request):
        list_id = DatabaseManagement.get_id(request['list_name'], request['email'])
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        list_object = self.db_management.retrieve_list(main_database_id, list_id)
        if not list_object:
            print("List not Found")
            return
        items = list_object['items']
        for item in items:
            if item['name'] == request['name']:
                items.remove(item)

        list_object['items'] = items
        self.db_management.replace_list(main_database_id, list_object)
        print("Success!")
        print(self.db_management.retrieve_list(main_database_id, list_id))

    def rename_item(self, request):
        list_id = DatabaseManagement.get_id(request['list_name'], request['email'])
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        list_object = self.db_management.retrieve_list(main_database_id, list_id)
        if not list_object:
            print("List not Found")
            return
        items = list_object['items']
        renamed = {}
        for item in items:
            if item['name'] == request['name']:
                item['name'] = request['newName']
                renamed = item
                items.remove(item)
                break
        found = False
        for item in items:
            if item['name'] == request['newName']:
                item['quantity'] += renamed['quantity']
                found = True
                break
        if not found:
            items.append(renamed)
        list_object['items'] = items
        self.db_management.replace_list(main_database_id, list_object)
        print("Success!")
        print(self.db_management.retrieve_list(main_database_id, list_id))

    def get_user_email(self, token):
        return self.authentication_management.decode_token(token)

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.connect("tcp://localhost:5560")

        while True:
            request = socket.recv_json()
            response = None
            try:
                payload = self.get_user_email(request['token'])
            except KeyError:
                response = {'error': 'No token provided.'}
            except InvalidSignatureError:
                response = {'error': 'Invalid token provided.'}
            if response is not None:
                socket.send_json(response)
                continue
            request['email'] = payload['email']
            response = self.request_handlers[request['type']](self.remove_attributes(request))
            socket.send_json(response)


if __name__ == '__main__':
    server = Server()
    server.run()
