import hashlib
import json
import os
import berkeleydb.db as bdb

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class DatabaseManagement:
    DATABASES_PATH = f"{ROOT_DIR}/../databases/berkeley/"

    def __init__(self):
        self.env = self.__initialize_environment()
        self.database_connections = self.__new_initialize_databases()

    @staticmethod
    def get_id(list_name, user_email):
        md5 = hashlib.md5()
        md5.update((list_name + user_email).encode('utf-8'))
        return md5.hexdigest()

    def replace_list(self, main_database_id, list_object):
        self.__insert_list(main_database_id, list_object)

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
        self.env.close()

    def get_num_connections(self):
        return len(self.database_connections)

    def __initialize_databases(self):
        # Create connections to the databases inside the "databases" folder
        database_connections = []
        for file_name in os.listdir(self.DATABASES_PATH):
            file_path = os.path.join(self.DATABASES_PATH, file_name)
            if os.path.isfile(file_path) and file_path[file_path.rindex(".")+1:] == 'db':
                db = bdb.DB(self.env)
                db.open(file_path, dbtype=bdb.DB_HASH, flags=(bdb.DB_CREATE | bdb.DB_AUTO_COMMIT))
                database_connections.append(db)
        return database_connections

    def __new_initialize_databases(self):
        # Create connections to the databases inside the "databases" folder
        database_connections = []
        names = [str(x) + ".db" for x in range(9)]
        for name in names:
            file_path = os.path.join(self.DATABASES_PATH, name)
            db = bdb.DB(self.env)
            db.open(file_path, dbtype=bdb.DB_HASH, flags=(bdb.DB_CREATE | bdb.DB_AUTO_COMMIT))
            database_connections.append(db)
        return database_connections

    # saves in all 3 databases of the folder
    def __insert_list(self, main_database_id, list_object):
        txn = self.__begin_transaction()
        database = self.database_connections[main_database_id]
        database.put(list_object['id'].encode('utf-8'), json.dumps(list_object).encode('utf-8'), txn=txn)
        database.sync()
        txn.commit()

    def __retrieve_list(self, main_database_id, list_id):
        list_id = str(list_id)
        # Retrieve a JSON data object from the specified database by ID
        txn = self.__begin_transaction()
        database = self.database_connections[main_database_id]
        res = database.get(list_id.encode('utf-8'), None, txn=txn)
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


if __name__ == '__main__':
    db_manager = DatabaseManagement()

    data = {
        "id": "30",
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

    obj = db_manager.retrieve_list(0, "30")
    print(obj)
    obj = db_manager.retrieve_list(1, "2")
    print(obj)
    obj = db_manager.retrieve_list(0, "2")
    print(obj)

    db_manager.close_databases()
