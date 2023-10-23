import json
import os
import berkeleydb.db as bdb


class DatabaseManagement:
    DATABASES_PATH = "./databases"

    def __init__(self):
        self.database_connections = self.initialize_databases()

    def initialize_databases(self):
        # Create connections to the databases inside the "databases" folder
        database_connections = {}

        for folder_name in os.listdir(self.DATABASES_PATH):
            folder_path = os.path.join(self.DATABASES_PATH, folder_name)

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
    def insert_object(self, main_database_id, replica_id, data_object):
        database_list = self.database_connections.get(main_database_id, [])
        if replica_id < len(database_list):
            for database in database_list:
                database.put(data_object["id"].encode('utf-8'), json.dumps(data_object).encode('utf-8'))

    def retrieve_object(self, main_database_id, replica_id, object_id):
        # Retrieve a JSON data object from the specified database by ID
        database_list = self.database_connections.get(main_database_id, [])
        for database in database_list:
            if replica_id < len(database_list):
                res = database.get(object_id.encode('utf-8'), None)
                if res is not None:
                    return res
        return None

    def close_databases(self):
        # Close all the database connections
        for database_list in self.database_connections.values():
            for database in database_list:
                database.close()

    def get_num_primary_connections(self):
        return len(self.database_connections.keys())

    def get_num_replicas_connections(self):
        return dict((x, len(y)) for x, y in self.database_connections.items())


if __name__ == '__main__':
    db_manager = DatabaseManagement()

    db_manager.insert_object(0, 0, {
        "id": "1",
        "name": "Object 1",
        "contents": [{"name": "Item 2", "quantity": 10}]
    })

    obj = db_manager.retrieve_object(0, 0, "1")
    print(obj)

    db_manager.close_databases()
