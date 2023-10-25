import json
import os
import berkeleydb.db as bdb
from DatabaseLoadBalancer import DatabaseLoadBalancer

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class DatabaseManagement:
    DATABASES_PATH = f"{ROOT_DIR}/../databases"

    def __init__(self):
        self.database_connections = self.__initialize_databases()
        self.next_id = self.__get_highest_id_across_databases()
        self.load_balancer = DatabaseLoadBalancer(self.get_num_primary_connections(),
                                                  self.get_num_replicas_connections())

    def replace_list(self, main_database_id, list_object):
        replica_id = self.load_balancer.route_to_database(main_database_id)
        self.__insert_list(main_database_id, replica_id, list_object, list_object["id"])

    def insert_list(self, main_database_id, list_object):
        replica_id = self.load_balancer.route_to_database(main_database_id)
        self.__insert_list(main_database_id, replica_id, list_object)

    def delete_list(self, main_database_id, list_id):
        replica_id = self.load_balancer.route_to_database(main_database_id)
        self.__delete_list(main_database_id, replica_id, list_id)

    def retrieve_list(self, main_database_id, list_id):
        replica_id = self.load_balancer.route_to_database(main_database_id)
        res = self.__retrieve_list(main_database_id, replica_id, list_id)
        if res is None:
            return []
        return json.loads(res.decode('utf-8'))

    def close_databases(self):
        # Close all the database connections
        for database_list in self.database_connections.values():
            for database in database_list:
                database.close()

    def get_num_primary_connections(self):
        return len(self.database_connections.keys())

    def get_num_replicas_connections(self):
        return dict((x, len(y)) for x, y in self.database_connections.items())

    def __get_highest_id_across_databases(self):
        highest_id = 1

        for database_list in self.database_connections.values():
            for database in database_list:
                cursor = database.cursor()
                record = cursor.last()
                if record is not None:
                    id_in_bytes, _ = record
                    current_id = int(id_in_bytes.decode('utf-8'))
                    highest_id = max(highest_id, current_id)

        return highest_id

    def __get_id(self):
        res = str(self.next_id)
        self.next_id += 1
        return res

    def __initialize_databases(self):
        # Create connections to the databases inside the "databases" folder
        database_connections = {}

        for folder_name in os.listdir(self.DATABASES_PATH):
            folder_path = os.path.join(self.DATABASES_PATH, folder_name)

            if folder_name.isalpha(): continue

            if os.path.isdir(folder_path):
                database_connections[int(folder_name)] = []
                for file_name in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file_name)
                    if os.path.isfile(file_path):
                        db = bdb.DB()
                        db.open(file_path, dbtype=bdb.DB_HASH, flags=bdb.DB_CREATE)
                        database_connections[int(folder_name)].append(db)

        return database_connections

    # saves in all 3 databases of the folder
    def __insert_list(self, main_database_id, replica_id, list_object, id_to_use=None):
        database_list = self.database_connections.get(main_database_id, [])
        if id_to_use is None:
            id_to_use = self.__get_id()
        list_object["id"] = id_to_use
        id_to_use = str(id_to_use)
        for database in database_list:
            database.put(id_to_use.encode('utf-8'), json.dumps(list_object).encode('utf-8'))
            database.sync()

    def __retrieve_list(self, main_database_id, replica_id, list_id):
        list_id = str(list_id)
        # Retrieve a JSON data object from the specified database by ID
        database_list = self.database_connections.get(main_database_id, [])
        for database in database_list:
            res = database.get(list_id.encode('utf-8'), None)
            if res is not None:
                return res
        return None

    def __delete_list(self, main_database_id, replica_id, list_id):
        list_id = str(list_id)
        database_list = self.database_connections.get(main_database_id, [])
        for database in database_list:
            try:
                database.delete(list_id.encode('utf-8'))
            except:
                print("Couldn't delete list")
        return None


if __name__ == '__main__':
    db_manager = DatabaseManagement()

    data = {
        "id": "30",  # this id will be ignored and replaced by a computed id
        "name": "Object 1",
        "items": [{"name": "Item 2", "quantity": 30}]
    }

    # db_manager.insert_list(0, data)

    data = {
        "id": "2",
        "name": "Object 1",
        "items": [{"name": "Item 2", "quantity": 2}]
    }

    # db_manager.insert_list(0, data)

    obj = db_manager.retrieve_list(0, "1")
    print(obj)
    obj = db_manager.retrieve_list(0, "30")
    print(obj)
    obj = db_manager.retrieve_list(0, "2")
    print(obj)

    db_manager.close_databases()
