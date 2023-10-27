import zmq
import os, sys
import hashlib
import uuid
import datetime

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
        num_primary_cons = self.db_management.get_num_primary_connections()
        self.hashing_ring = HashingRing(num_primary_cons)
        self.request_handlers = {'AddItem': self.add_item, 'BuyItem': self.buy_item, 'CreateList': self.create_list,
                                 'DeleteList': self.delete_list, 'DeleteItem': self.delete_item, 'RenameItem': self.rename_item, 'Login': self.login}
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


    def login(self, request):
        email = request["email"]
        password = request["password"]
        password = hashlib.sha256(password.encode()).hexdigest()
        if self.authentication_management.check_user_exists(email, password):
            user_id = self.authentication_management.get_user(email)[0]
            new_token = uuid.uuid4()
            expiration_date = datetime.datetime.now() + datetime.timedelta(days=self.expiration_date_days)
            self.authentication_management.create_token(user_id, new_token, expiration_date)
            return {"token": str(new_token)}
        else:
            return {"error": "Invalid credentials"}
    
    def register(self, request):
        email = request["email"]
        password = request["password"]
        password = hashlib.sha256(password.encode()).hexdigest()
        if not self.authentication_management.check_user_exists(email, password):
            self.authentication_management.create_user(email, password)
            return {"success": "User created"}
        else:
            return {"error": "User already exists"}

    def is_authenticated(self, request):
        token = request["token"]
        if self.authentication_management.verify_user_token(token):
            return True
        else:
            return False
        
    def add_item(self, request):
        #if not self.is_authenticated(request):
        #    return {"error": "Invalid token"}
        list_id = request["list_id"]
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
        #if not self.is_authenticated(request):
        #    return {"error": "Invalid token"}
        list_id = request["list_id"]
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
        #if not self.is_authenticated(request):
        #    return {"error": "Invalid token"}
        list_id = self.db_management.next_id
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        self.db_management.insert_list(main_database_id, request)
        print("Success!")
        print(self.db_management.retrieve_list(main_database_id, list_id))

    def delete_list(self, request):
        #if not self.is_authenticated(request):
        #    return {"error": "Invalid token"}
        main_database_id = self.hashing_ring.find_main_database_id(request["list_id"])
        self.db_management.delete_list(main_database_id, request["list_id"])
        print("Success!")
        print(self.db_management.retrieve_list(main_database_id, request["list_id"]))

    def delete_item(self, request):
        #if not self.is_authenticated(request):
        #    return {"error": "Invalid token"}
        list_id = request["list_id"]
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
        #if not self.is_authenticated(request):
        #    return {"error": "Invalid token"}
        list_id = request["list_id"]
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

