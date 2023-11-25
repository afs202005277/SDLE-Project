import hashlib
import json
import os
import berkeleydb.db as bdb

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class DatabaseManagement:
    DATABASES_PATH = f"{ROOT_DIR}/../databases/berkeley/"

    def __init__(self):
        self.env = self.__initialize_environment()
        self.database_connections = {}
        self.database_connections_state = {}
        self.database_connections_num_requests = {}
        self.database_connections_num_lists = {}
        self.__new_initialize_databases()
        self.num_replicas = 2

    @staticmethod
    def get_id(list_name, user_email):
        md5 = hashlib.md5()
        md5.update((list_name + user_email).encode('utf-8'))
        return md5.hexdigest()

    def __find_real_main_db_id(self, given_database_id):
        original = given_database_id
        while not self.database_connections_state[given_database_id]:
            given_database_id += 1
            if given_database_id > max(self.database_connections.keys()):
                given_database_id = min(self.database_connections.keys())

            if given_database_id == original:
                return None

        return given_database_id

    def replace_list(self, main_database_id, list_object):
        main_database_id = self.__find_real_main_db_id(main_database_id)
        self.database_connections_num_requests[main_database_id] += 1
        self.__insert_list(main_database_id, list_object)

    def insert_list(self, main_database_id, list_object):
        main_database_id = self.__find_real_main_db_id(main_database_id)
        self.database_connections_num_requests[main_database_id] += 1
        dbs = self.__get_db_and_replicas(main_database_id)
        for db in dbs:
            self.__insert_list(db, list_object)

    def delete_list(self, main_database_id, list_id):
        main_database_id = self.__find_real_main_db_id(main_database_id)
        self.database_connections_num_requests[main_database_id] += 1
        dbs = self.__get_db_and_replicas(main_database_id)
        for db in dbs:
            self.__delete_list(db, list_id)

    def retrieve_list(self, main_database_id, list_id):
        main_database_id = self.__find_real_main_db_id(main_database_id)
        self.database_connections_num_requests[main_database_id] += 1
        res = self.merge_list(main_database_id, list_id)
        if res is None:
            return []
        return res

    def close_databases(self):
        # Close all the database connections
        for db_id, database in self.database_connections.items():
            database.close()
        self.env.close()

    def get_num_connections(self):
        return len(self.database_connections)

    def __new_initialize_databases(self):
        # Create connections to the databases inside the "databases" folder
        names = [str(x) + ".db" for x in range(9)]
        for name in names:
            file_path = os.path.join(self.DATABASES_PATH, name)
            db_id = int(file_path[:file_path.rindex(".")].split('/')[-1])
            db = bdb.DB(self.env)
            db.open(file_path, dbtype=bdb.DB_HASH, flags=(bdb.DB_CREATE | bdb.DB_AUTO_COMMIT))
            self.database_connections[db_id] = db
            self.database_connections_state[db_id] = True
            self.database_connections_num_requests[db_id] = 0
            self.database_connections_num_lists[db_id] = len(
                    self.__retrieve_lists(db_id))

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

    def __exists_list(self, database_id, list_id):
        return len([x for x in self.__retrieve_lists(database_id) if x[0].decode('utf-8') == list_id]) == 0

    def __insert_list(self, main_database_id, list_object):
        txn = self.__begin_transaction()
        database = self.database_connections[main_database_id]
        database.put(list_object['id'].encode('utf-8'), json.dumps(list_object).encode('utf-8'), txn=txn)
        txn.commit()

        if self.__exists_list(main_database_id, list_object['id']):
            self.database_connections_num_lists[main_database_id] += 1

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
        self.database_connections_num_lists[main_database_id] -= 1

    def __begin_transaction(self):
        txn = self.env.txn_begin()
        return txn

    def __initialize_environment(self):
        env = bdb.DBEnv()
        env.open(self.DATABASES_PATH, bdb.DB_INIT_MPOOL | bdb.DB_CREATE | bdb.DB_INIT_TXN | bdb.DB_INIT_LOG)
        return env

    def __next_db(self, curr_db):
        db_ids = list(self.database_connections.keys())
        next_db = db_ids[db_ids.index(curr_db) + 1] if db_ids.index(curr_db) + 1 != len(db_ids) else db_ids[0]
        return self.__find_real_main_db_id(next_db)

    def __in_a_row_dbs(self, list_dbs):
        db_ids = list(self.database_connections.keys())
        i = db_ids.index(list_dbs[0])
        for j in range(1, len(list_dbs)):
            if db_ids[(i + j) % len(db_ids)] != list_dbs[j % len(list_dbs)]:
                return False
        return True

    def __get_db_and_replicas(self, main_database_id):
        dbs = [main_database_id]
        for i in range(self.num_replicas):
            dbs.append(self.__next_db(dbs[-1]))
        return dbs

    def apply_changelogs(self, list_object, changelogs):
        for change in changelogs:
            if change['operation'] == 'add':
                items = list_object['items']
                for item in items:
                    if item['name'] == change['item']:
                        item['quantity'] += change['quantity']
                        break
                else:
                    items.append({'name': change['item'], 'quantity': change['quantity']})
            elif change['operation'] == 'buy':
                items = list_object['items']
                for item in items:
                    if item['name'] == change['item']:
                        item['quantity'] -= int(change['quantity'])
                        break
                else:
                    items.append({'name': change['item'], 'quantity': -int(change['quantity'])})
            elif change['operation'] == 'rename':
                items = list_object['items']
                renamed = {}
                for item in items:
                    if item['name'] == change['item']:
                        item['name'] = change['newItem']
                        renamed = item
                        items.remove(item)
                        break
                else:
                    continue

                for item in items:
                    if item['name'] == change['newItem']:
                        item['quantity'] += renamed['quantity']
                        break
                else:
                    items.append(renamed)
            elif change['operation'] == 'delete':
                items = list_object['items']
                for item in items:
                    if item['name'] == change['item']:
                        items.remove(item)

        for item in list_object['items']:
            if item['quantity'] <= 0:
                list_object['items'].remove(item)

    def add_changelogs(self, main_database_id, list_id, changelogs):
        main_database_id = self.__find_real_main_db_id(main_database_id)
        dbs = self.__get_db_and_replicas(main_database_id)

        for db in dbs:
            retrieved_temp = self.__retrieve_list(db, list_id)
            if retrieved_temp is not None:
                list_object = json.loads(retrieved_temp.decode('utf-8'))
                break
        else:
            return False

        if list_object is not None:
            list_object['changelog'] += changelogs
            for db in dbs:
                self.__insert_list(db, list_object)

        return True


    def merge_list(self, main_database_id, list_id):
        given_database_id = main_database_id
        main_database_id = self.__find_real_main_db_id(main_database_id)

        dbs = self.__get_db_and_replicas(main_database_id)

        list_object = None
        for db in dbs:
            retrieved_temp = self.__retrieve_list(db, list_id)
            if retrieved_temp is not None:
                list_object = json.loads(retrieved_temp.decode('utf-8'))
                break
        if list_object is not None:
            if not self.__in_a_row_dbs(dbs) or main_database_id != given_database_id:
                for db in dbs:
                    self.__insert_list(db, list_object)
            changelogs_together = []
            for db in dbs:
                l_obj_temp = json.loads(self.__retrieve_list(db, list_id).decode('utf-8')) if self.__retrieve_list(db,
                                                                                                                   list_id) is not None else None
                if l_obj_temp is not None:
                    changelogs_together += l_obj_temp['changelog']

            changelogs_t_temp = set(frozenset(d.items()) for d in changelogs_together)
            changelogs_together = [dict(f) for f in changelogs_t_temp]
            changelogs_together = sorted(changelogs_together, key=lambda x: x['timestamp'])
            self.apply_changelogs(list_object, changelogs_together)

            if self.__in_a_row_dbs(dbs) and main_database_id == given_database_id:
                list_object['changelog'] = []
                for db in dbs:
                    self.__insert_list(db, list_object)

        return list_object

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
    db_manager.insert_list(db_id_store_on + 1, data)

    db_manager.retrieve_list(db_id_store_on, data['id'])

    db_manager.print_all_lists()

    db_manager.close_databases()"""
