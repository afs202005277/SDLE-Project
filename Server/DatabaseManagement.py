import json
import os
import berkeleydb.db as bdb

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class DatabaseManagement:
    DATABASES_PATH = f"{ROOT_DIR}/../databases/berkeley/"

    def __init__(self):
        self.database_connections = self.__initialize_databases()
        self.next_id = self.__get_highest_id_across_databases()

    def replace_list(self, main_database_id, list_object):
        self.__insert_list(main_database_id, list_object, list_object["id"])

    def insert_list(self, main_database_id, list_object):
        self.__insert_list(main_database_id, list_object)

    def delete_list(self, main_database_id, list_id):
        self.__delete_list(main_database_id, list_id)

    def retrieve_list(self, main_database_id, list_id):
        res = self.__retrieve_list(main_database_id, list_id)
        if res is None:
            return []
        return json.loads(res.decode('utf-8'))

    def close_databases(self):
        # Close all the database connections
        for database in self.database_connections:
            database.close()

    def get_num_connections(self):
        return len(self.database_connections)

    def __get_highest_id_across_databases(self):
        highest_id = 1

        for database in self.database_connections:
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
        database_connections = []
        for file_name in os.listdir(self.DATABASES_PATH):
            file_path = os.path.join(self.DATABASES_PATH, file_name)
            if os.path.isfile(file_path):
                db = bdb.DB()
                db.open(file_path, dbtype=bdb.DB_HASH, flags=bdb.DB_CREATE)
                database_connections.append(db)
        return database_connections

    # saves in all 3 databases of the folder
    def __insert_list(self, main_database_id, list_object, id_to_use=None):
        database = self.database_connections[main_database_id]
        if id_to_use is None:
            id_to_use = self.__get_id()
        list_object["id"] = id_to_use
        id_to_use = str(id_to_use)
        database.put(id_to_use.encode('utf-8'), json.dumps(list_object).encode('utf-8'))
        database.sync()

    def __retrieve_list(self, main_database_id, list_id):
        list_id = str(list_id)
        # Retrieve a JSON data object from the specified database by ID
        database = self.database_connections[main_database_id]
        res = database.get(list_id.encode('utf-8'), None)
        if res is not None:
            return res
        return None

    def __delete_list(self, main_database_id, list_id):
        list_id = str(list_id)
        database = self.database_connections[main_database_id]
        try:
            database.delete(list_id.encode('utf-8'))
        except:
            print("Couldn't delete list")


if __name__ == '__main__':
    db_manager = DatabaseManagement()

    data = {
        "id": "30",  # this id will be ignored and replaced by a computed id
        "name": "Object 1",
        "items": [{"name": "Item 2", "quantity": 30}]
    }

    db_manager.insert_list(0, data)

    data = {
        "id": "2",
        "name": "Object 1",
        "items": [{"name": "Item 2", "quantity": 2}]
    }

    db_manager.insert_list(1, data)

    obj = db_manager.retrieve_list(0, "1")
    print(obj)
    obj = db_manager.retrieve_list(1, "2")
    print(obj)
    obj = db_manager.retrieve_list(0, "2")
    print(obj)

    db_manager.close_databases()
