import threading
import requests
import zmq
import os
import sys
import json
import hashlib
import time
from prettytable import PrettyTable

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
            'GetListHash': self.get_list_hash,
            'Synchronize': self.synchronize,
            'GetListID': self.get_list_id
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

    def get_list_id(self, request):
        return DatabaseManagement.get_id(request['list_name'], request['email'])

    def get_list_hash(self, request):
        list_id = DatabaseManagement.get_id(request['list_name'], request['email'])
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        list_object = self.db_management.retrieve_list(main_database_id, list_id)
        if not list_object:
            print("List not Found")
            return ''

        dict_to_hash = {k: v for k, v in list_object.items() if k == 'list_name' or k == 'items'}
        list_str = json.dumps(dict_to_hash).replace(' ', '').replace('\"', '').encode('utf-8')
        return hashlib.md5(list_str).hexdigest()

    def synchronize(self, request):
        print(request)

        list_id = request['list_id']
        main_database_id = self.hashing_ring.find_main_database_id(list_id)

        offline_changelog = request['changelog']

        cloud_db = self.db_management.retrieve_list(main_database_id, list_id)
        if cloud_db == []: 
            print('list doesnt exists, create it')
            self.create_list(request)
        cloud_db = self.db_management.retrieve_list(main_database_id, list_id)

        print(cloud_db)
        changelogs = sorted(offline_changelog + cloud_db['changelog'], key=lambda x: x['timestamp'])
        self.db_management.apply_changelogs(cloud_db, offline_changelog)
        print(cloud_db)

        self.db_management.insert_list(main_database_id, cloud_db)

        print('sync request')
        return json.dumps(cloud_db)

    def add_item(self, request):
        list_id = request['list_id']
        print("ADD ITEM")
        print(list_id)
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        list_object = self.db_management.retrieve_list(main_database_id, list_id)
        if not list_object:
            print("List not Found")
            return

        log = {'timestamp': time.time(), 'operation': 'add', 'item': request['name'], 'quantity': request['quantity']}
        list_object['changelog'].append(log)

        self.db_management.replace_list(main_database_id, list_object)

    def buy_item(self, request):
        list_id = request['list_id']
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        list_object = self.db_management.retrieve_list(main_database_id, list_id)
        if not list_object:
            print("List not Found")
            return

        log = {'timestamp': time.time(), 'operation': 'buy', 'item': request['name'], 'quantity': request['quantity']}
        list_object['changelog'].append(log)

        self.db_management.replace_list(main_database_id, list_object)
        print("Success!")
        print(self.db_management.retrieve_list(main_database_id, list_id))

    # no caso do client adicionar uma shared list, o id da lista vem no list["name"]
    def create_list(self, request):
        existing_list = self.db_management.search_list(request['list_name'])
        if existing_list is None:
            list_id = DatabaseManagement.get_id(request['list_name'], request['email'])
            request["id"] = list_id
            request["items"] = []
            request['changelog'] = []
            main_database_id = self.hashing_ring.find_main_database_id(list_id)
            self.db_management.insert_list(main_database_id, request)
            print("Success!")
            print(self.db_management.retrieve_list(main_database_id, list_id))
            return {"status": "created", "data": {"list_id": list_id}}
        else:
            print("List Sharing!")
            return {"status": "existing", "data": existing_list}

    def delete_list(self, request):
        list_id = request['list_id']
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        self.db_management.delete_list(main_database_id, list_id)
        print("Success!")
        print(self.db_management.retrieve_list(main_database_id, list_id))

    def delete_item(self, request):
        list_id = request['list_id']
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        list_object = self.db_management.retrieve_list(main_database_id, list_id)
        if not list_object:
            print("List not Found")
            return

        log = {'timestamp': time.time(), 'operation': 'delete', 'item': request['name']}
        list_object['changelog'].append(log)

        self.db_management.replace_list(main_database_id, list_object)
        print("Success!")
        print(self.db_management.retrieve_list(main_database_id, list_id))

    def rename_item(self, request):
        list_id = request['list_id']
        main_database_id = self.hashing_ring.find_main_database_id(list_id)
        list_object = self.db_management.retrieve_list(main_database_id, list_id)
        if not list_object:
            print("List not Found")
            return

        log = {'timestamp': time.time(), 'operation': 'rename', 'item': request['name'], 'newItem': request['newName']}
        list_object['changelog'].append(log)

        self.db_management.replace_list(main_database_id, list_object)
        print("Success!")
        print(self.db_management.retrieve_list(main_database_id, list_id))

    def get_user_email(self, token):
        return self.authentication_management.decode_token(token)

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.connect("tcp://localhost:5560")

        global tm # checks if terminal manager is running
        while tm.is_alive():
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

class RequestsServer(threading.Thread):
    def __init__(self):
        super(RequestsServer, self).__init__(name="Requests Server Thread")
        self._stop_event = threading.Event()

    def run(self):
        global server
        server.run()

    def stop(self):
        self._stop_event.set()

class DBTerminalManagement(threading.Thread):
    def __init__(self):
        super(DBTerminalManagement, self).__init__(name="DB Terminal Management Thread")
        print('DB Terminal Management Online')

    def print_table(self, data_dict):
        table = PrettyTable()
        table.field_names = list(data_dict.keys())

        for i in range(len(data_dict[list(data_dict.keys())[0]])):
            row = [data_dict[key][i] for key in data_dict.keys()]
            table.add_row(row)

        print(table)

    def run(self):
        global server
        print("Welcome to the DB Management Terminal!")
        print("Write 'help' to get started")
        command = ""
        args = []
        while command.strip().lower() != "quit":
            received = input("> ")
            command = received.split(' ')[0]
            args = received.split(' ')[1:]

            if command == "help":
                print("Available Commands:")
                print("\n\thelp - Shows a list of the existing commands with a comprehensive explanation.\n")
                print("\tlist - Lists the current existing DBs. Shows their ids, current state (ONLINE, OFFLINE), number of requests and number of shopping lists.\n")
                print("\tcreate - Creates a new DB for the server. The id of this DB is automatically assigned.\n")
                print("\tenable [id]- Enables a currently disabled DB. Receives an argument id which represents the id of the DB.\n")
                print("\tdisable [id] - Disables an existing DB from the server. Receives an argument id which represents the id of the DB.\n")
                print("\tprintlists - Prints all the lists in the databases. WARNING: Only run when necessary.")
                print("\tquit - Turns off the server and this management terminal.")
                print("\nNotes:")
                print("\n\tArguments can always be passed in front of any command. The only arguments that will ever be used are for commands that ask for them. Any command will alert in the case of a nonexistent/invalid argument.")
            elif command == "create":
                new_db_id = server.db_management.create_database()
                server.hashing_ring = HashingRing(len(server.db_management.database_connections.keys()))
                print(f"Successfully created a new DB with the ID {new_db_id}")
            elif command in ["enable", "disable"]:
                if len(args) == 0:
                    print("You didn't provide any id")
                    continue
                try:
                    provided_id = int(args[0])
                except ValueError:
                    print("The id provided is not a valid number")
                    continue

                if provided_id not in server.db_management.database_connections_state:
                    print("The id you provided doesn't match any existent database id")
                    continue

                if command == "enable":
                    if server.db_management.database_connections_state[provided_id]:
                        print(f"The database with the ID {provided_id} was already enabled.")
                    else:
                        server.db_management.database_connections_state[provided_id] = True
                        print(f"Successfully enabled database with the ID {provided_id}")
                else:
                    if not server.db_management.database_connections_state[provided_id]:
                        print(f"The database with the ID {provided_id} was already disabled.")
                    else:
                        server.db_management.database_connections_state[provided_id] = False
                        print(f"Successfully disabled database with the ID {provided_id}.")
            elif command == "printlists":
                server.db_management.print_all_lists()
            elif command == "list":
                db_ids = list(server.db_management.database_connections.keys())
                db_states = ["ONLINE" if server.db_management.database_connections_state[key] else "OFFLINE" for key in db_ids]
                db_num_requests = [server.db_management.database_connections_num_requests[key] for key in db_ids]
                db_num_lists = [server.db_management.database_connections_num_lists[key] for key in db_ids]
                table_dict = {"Database ID": db_ids, "State": db_states, "Nº Requests": db_num_requests, "Nº Lists": db_num_lists}
                self.print_table(table_dict)
            elif command == "quit":
                pass
            else:

                suggestions = ["help", "create", "enable", "disable", "list", "printlists"]
                min_correspondence = 3  # Minimum correspondence to consider a suggestion

                suggestion = ""
                max_matches = 0

                for possible in suggestions:
                    matches = sum(a == b for a, b in zip(command, possible))

                    if matches > max_matches and matches >= min_correspondence:
                        suggestion = possible
                        max_matches = matches

                if suggestion != "":
                    print(f"The command '{command}' does not exist. Did you mean '{suggestion}'?")
                else:
                    print(f"The command '{command}' does not exist. Write 'help' for possible commands.")


        print("Thank you for using our system! Quitting.")


if __name__ == '__main__':
    server = Server()

    rs = RequestsServer()
    tm = DBTerminalManagement()

    print('Requests Server Online')
    rs.start()

    tm.start()

    while tm.is_alive():
        if not rs.is_alive():
            # if RequestsServer crashes - we start it up again
            rs = RequestsServer()
            rs.start()

    ## send a random request for RequestsServer to verify that tm is no longer running
    while rs.is_alive():
        pass

    print("Shutting Down...")