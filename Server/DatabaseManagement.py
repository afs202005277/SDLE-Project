import hashlib
import json
import os
import berkeleydb.db as bdb

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class DatabaseManagement:
    DATABASES_PATH = f"{ROOT_DIR}/../databases/berkeley/"

    def __init__(self):
        self.env = self.__initialize_environment()
        self.database_connections, self.database_connections_state, self.database_connections_num_requests, self.database_connections_num_lists = self.__new_initialize_databases()

    @staticmethod
    def get_id(list_name, user_email):
        md5 = hashlib.md5()
        md5.update((list_name + user_email).encode('utf-8'))
        return md5.hexdigest()

    def find_real_main_db_id(self, given_database_id):
        original = given_database_id
        while not self.database_connections_state[given_database_id]:
            given_database_id += 1
            if given_database_id > max(self.database_connections.keys()):
                given_database_id = min(self.database_connections.keys())

            if given_database_id == original:
                return None

        return given_database_id

    def replace_list(self, main_database_id, list_object):
        main_database_id = self.find_real_main_db_id(main_database_id)
        self.database_connections_num_requests[main_database_id] += 1
        self.__insert_list(main_database_id, list_object)

    def insert_list(self, main_database_id, list_object):
        main_database_id = self.find_real_main_db_id(main_database_id)
        self.database_connections_num_requests[main_database_id] += 1
        self.__insert_list(main_database_id, list_object)
        self.database_connections_num_lists[main_database_id] += 1

    def delete_list(self, main_database_id, list_id):
        main_database_id = self.find_real_main_db_id(main_database_id)
        self.database_connections_num_requests[main_database_id] += 1
        self.__delete_list(main_database_id, list_id)
        self.database_connections_num_lists[main_database_id] -= 1

    def retrieve_list(self, main_database_id, list_id):
        main_database_id = self.find_real_main_db_id(main_database_id)
        self.database_connections_num_requests[main_database_id] += 1
        self.merge_list(main_database_id, list_id)
        res = self.__retrieve_list(main_database_id, list_id)
        if res is None:
            return []
        return json.loads(res.decode('utf-8'))

    def close_databases(self):
        # Close all the database connections
        for database in self.database_connections:
            database.close()
        self.env.close()

    def get_num_connections(self):
        return len(self.database_connections)

    def __initialize_databases(self):
        # Create connections to the databases inside the "databases" folder
        database_connections = {}
        database_connections_state = {}
        database_connections_num_requests = {}
        database_connections_num_lists = {}
        for file_name in os.listdir(self.DATABASES_PATH):
            file_path = os.path.join(self.DATABASES_PATH, file_name)
            if os.path.isfile(file_path) and file_path[file_path.rindex(".") + 1:] == 'db':
                db = bdb.DB(self.env)
                db.open(file_path, dbtype=bdb.DB_HASH, flags=(bdb.DB_CREATE | bdb.DB_AUTO_COMMIT))
                database_connections[int(file_path[:file_path.rindex(".")])] = db
                database_connections_state[int(file_path[:file_path.rindex(".")])] = True
                database_connections_num_requests[int(file_path[:file_path.rindex(".")])] = 0
                database_connections_num_lists[int(file_path[:file_path.rindex(".")])] = len(self.__retrieve_lists(int(file_path[:file_path.rindex(".")])))
        return database_connections, database_connections_state, database_connections_num_requests, database_connections_num_lists

    def __new_initialize_databases(self):
        # Create connections to the databases inside the "databases" folder
        database_connections = {}
        database_connections_state = {}
        database_connections_num_requests = {}
        database_connections_num_lists = {}
        names = [str(x) + ".db" for x in range(9)]
        for name in names:
            file_path = os.path.join(self.DATABASES_PATH, name)
            db = bdb.DB(self.env)
            db.open(file_path, dbtype=bdb.DB_HASH, flags=(bdb.DB_CREATE | bdb.DB_AUTO_COMMIT))
            database_connections[int(name.split('.db')[0])] = db
            database_connections_state[int(name.split('.db')[0])] = True
            database_connections_num_requests[int(name.split('.db')[0])] = 0
            database_connections_num_lists[int(name.split('.db')[0])] = 0
        return database_connections, database_connections_state, database_connections_num_requests, database_connections_num_lists

    def create_database(self):
        new_db_id = max(self.database_connections.keys()) + 1
        name = str(new_db_id) + ".db"
        file_path = os.path.join(self.DATABASES_PATH, name)
        db = bdb.DB(self.env)
        db.open(file_path, dbtype=bdb.DB_HASH, flags=(bdb.DB_CREATE | bdb.DB_AUTO_COMMIT))
        self.database_connections[new_db_id] = db
        self.database_connections_state[new_db_id] = True
        self.database_connections_num_requests[new_db_id] = 0
        self.database_connections_num_lists[new_db_id] = 0
        return new_db_id

    def __insert_list(self, main_database_id, list_object):
        txn = self.__begin_transaction()
        database = self.database_connections[main_database_id]
        database.put(list_object['id'].encode('utf-8'), json.dumps(list_object).encode('utf-8'), txn=txn)
        txn.commit()

    def __retrieve_list(self, database_id, list_id):
        list_id = str(list_id)
        # Retrieve a JSON data object from the specified database by ID
        txn = self.__begin_transaction()
        database = self.database_connections[database_id]
        res = database.get(list_id.encode('utf-8'), None, txn=txn)
        txn.commit()
        if res is not None:
            return res
        return None

    def print_all_lists(self):
        for db_id in range(self.get_num_connections()):
            print(f"DB {db_id}:")
            print(self.__retrieve_lists(db_id))

    def __retrieve_lists(self, main_database_id):
        txn = self.__begin_transaction()
        database = self.database_connections[main_database_id]
        res = database.items()
        txn.commit()
        if res is not None:
            return res
        return None

    def __delete_list(self, main_database_id, list_id):
        list_id = str(list_id)
        txn = self.__begin_transaction()
        database = self.database_connections[main_database_id]
        try:
            database.delete(list_id.encode('utf-8'), txn=txn)
        except:
            print("Couldn't delete list")
        txn.commit()

    def __begin_transaction(self):
        txn = self.env.txn_begin()
        return txn

    def __initialize_environment(self):
        env = bdb.DBEnv()
        env.open(self.DATABASES_PATH, bdb.DB_INIT_MPOOL | bdb.DB_CREATE | bdb.DB_INIT_TXN | bdb.DB_INIT_LOG)
        return env

    def __next_db(self, curr_db):
        return (curr_db + 1 if curr_db < self.get_num_connections() - 1 else 0)

    def merge_list(self, main_database_id, list_id, num_replicas=2):
        changelogs_together = []
        for offset in range(num_replicas+1):
            list_object = json.loads(self.__retrieve_list(main_database_id+offset, list_id).decode('utf-8')) if self.__retrieve_list(main_database_id+offset, list_id) != None else None
            if list_object != None:
                changelogs_together += list_object['changelog']

        changelogs_together = list(set(changelogs_together))
        main_list_object = json.loads(self.__retrieve_list(main_database_id, list_id).decode('utf-8'))

        """for log in changelogs_together:
            if log['operation'] == 'add':
                for item in main_list_object['items']:
                    if item['name'] == log['item']:
                        edit_item = item.copy()
                        main_list_object['items'].remove(item)
                        edit_item['quantity'] += log['quantity']
                        main_list_object['items'].remove(edit_item)
                        break
                else:
                    main_list_object['items'].remove(edit_item)
                if log['item'] in main_list_object['items']
                #main_list_object['items']['']"""


        print("a")


    def search_list(self, list_id):
        # list_id = int(list_id, 16 if hexadecimal else 10)
        for i in range(self.get_num_connections()):
            res = self.retrieve_list(i, list_id)
            if len(res) > 0:
                return res
        return None


def search_list(manager, list_id, hexadecimal):
    list_id = int(list_id, 16 if hexadecimal else 10)
    for i in range(manager.get_num_connections()):
        res = manager.retrieve_list(i, list_id)
        if len(res) > 0:
            return res
    return "Not found"


def serialize_list(list, db_manager):
    from HashingRing import HashingRing
    hashing_ring = HashingRing(db_manager.get_num_connections())

    list_id = DatabaseManagement.get_id(list['name'], list['email'])
    list['id'] = list_id

    return list, hashing_ring.find_main_database_id(list_id)


if __name__ == '__main__':
    import time

    db_manager = DatabaseManagement()
    db_manager.print_all_lists()
    """data = {
        "name": "Object 1",
        "items": [{"name": "Item 2", "quantity": 30}],
        "email": "johndoe@example.com",
        "changelog": [{'timestamp': time.time(), 'operation': 'add', 'item': "Item 2", 'quantity': 30}]
    }
    data, db_id_store_on = serialize_list(data, db_manager)
    db_manager.insert_list(db_id_store_on, data)

    data = {
        "name": "buhbhbjh",
        "items": [{"name": "Item 1", "quantity": 8}, {"name": "Item 2", "quantity": 2}],
        "email": "hbib@uhbuy.com",
        "changelog": [{'timestamp': time.time(), 'operation': 'add', 'item': "Item 1", 'quantity': 8},
                      {'timestamp': time.time(), 'operation': 'add', 'item': "Item 2", 'quantity': 30}]
    }
    data, db_id_store_on = serialize_list(data, db_manager)
    db_manager.insert_list(db_id_store_on, data)

    data = {
        "name": "buhbhbjh",
        "items": [{"name": "Item 1", "quantity": 11}, {"name": "Item 2", "quantity": 2}],
        "email": "hbib@uhbuy.com",
        "changelog": [{'timestamp': time.time(), 'operation': 'add', 'item': "Item 1", 'quantity': 3},
                      {'timestamp': time.time(), 'operation': 'add', 'item': "Item 2", 'quantity': 30},
                      {'timestamp': time.time(), 'operation': 'add', 'item': "Item 1", 'quantity': 8}]
    }
    data, db_id_store_on = serialize_list(data, db_manager)
    db_manager.insert_list(db_id_store_on+1, data)

    db_manager.retrieve_list(db_id_store_on, data['id'])

    db_manager.print_all_lists()

    db_manager.close_databases()"""
