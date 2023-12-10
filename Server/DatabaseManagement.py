import hashlib
import json
import os
import berkeleydb.db as bdb

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class DatabaseManagement:
    DATABASES_PATH = f"{ROOT_DIR}/../databases/berkeley/"

    def __init__(self):
        """
            Initializes an instance of the DatabaseManagement class.
        """
        # Initialize Berkeley DB environment
        self.env = self.__initialize_environment()

        # Databases and related state variables
        self.database_connections = {}  # Dictionary to store Berkeley DB connections
        self.database_connections_state = {}  # Dictionary to track the state of each database connection (True if online, False otherwise)
        self.database_connections_num_requests = {}  # Dictionary to track the number of requests for each database connection
        self.database_connections_num_lists = {}  # Dictionary to track the number of lists for each database connection

        # Initialize databases and related state
        self.__new_initialize_databases()

        # Number of replicas for each database
        self.num_replicas = 2

    def startup_merge_sync(self, db_id):
        """
            Performs the startup merge synchronization for the specified database.

            During startup of a database, this method is called to search through the other databases and find out which
            lists should be moved to this database instance.
            When the moving is complete, the lists that were moved are erased from their sources.

            Args:
                db_id (int): The identifier of the target database.
        """
        from HashingRing import HashingRing
        hashing_ring = HashingRing(self.get_num_connections())
        for i in self.database_connections.keys():
            if i != db_id and self.database_connections_state[i]:
                for l in self.__retrieve_lists(i):
                    list_id = l[0].decode('utf-8')
                    list_object = json.loads(l[1].decode('utf-8'))
                    main_db_id = hashing_ring.find_main_database_id(list_id)

                    if db_id in self.__get_db_and_replicas(main_db_id):
                        self.__insert_list(db_id, list_object)
                        self.merge_list(db_id, list_id)
                    if self.database_connections_state[main_db_id]:
                        self.merge_list(main_db_id, list_id)

        for i in self.database_connections.keys():
            if i != db_id and self.database_connections_state[i]:
                for l in self.__retrieve_lists(i):
                    list_id = l[0].decode('utf-8')
                    main_db_id = hashing_ring.find_main_database_id(list_id)
                    if i not in self.__get_db_and_replicas(main_db_id) and db_id in self.__get_db_and_replicas(
                            main_db_id):
                        self.__delete_list(i, list_id)

    def update_num_lists(self):
        """
            Updates the number of lists for each database connection.
            Iterates through all database connections and retrieves the current number of lists for each database.
        """
        for i in self.database_connections.keys():
            self.database_connections_num_lists[i] = len(self.__retrieve_lists(i))

    @staticmethod
    def get_id(list_name, user_email):
        """
            Generates a unique identifier (hash) for a list based on its name and user email.

            Args:
                list_name (str): The name of the list.
                user_email (str): The email of the user associated with the list.

            Returns:
                str: The unique identifier (hash) for the list.
        """
        md5 = hashlib.md5()
        md5.update((list_name + user_email).encode('utf-8'))
        return md5.hexdigest()

    def __find_real_main_db_id(self, given_database_id):
        """
            Finds the real main database ID in a series when the given database ID is not in an online state.

            Args:
                given_database_id (int): The given database ID.

            Returns:
                int or None: The real main database ID or None if not found.

        """
        original = given_database_id
        while not self.database_connections_state[given_database_id]:
            given_database_id += 1
            if given_database_id > max(self.database_connections.keys()):
                given_database_id = min(self.database_connections.keys())

            if given_database_id == original:
                return None

        return given_database_id

    def insert_list(self, main_database_id, list_object):
        """
            Inserts a list into the specified main database and its replicas.

            Args:
                main_database_id (int): The identifier of the main database.
                list_object (dict): The JSON representation of the list to be inserted.
        """
        main_database_id = self.__find_real_main_db_id(main_database_id)
        self.database_connections_num_requests[main_database_id] += 1
        dbs = self.__get_db_and_replicas(main_database_id)
        for db in dbs:
            self.__insert_list(db, list_object)

    def delete_list(self, main_database_id, list_id):
        """
            Deletes a list from the specified main database and its replicas.

            Args:
                main_database_id (int): The identifier of the main database.
                list_id (str): The identifier of the list to be deleted.
        """
        main_database_id = self.__find_real_main_db_id(main_database_id)
        self.database_connections_num_requests[main_database_id] += 1
        dbs = self.__get_db_and_replicas(main_database_id)
        for db in dbs:
            self.__delete_list(db, list_id)

    def retrieve_list(self, main_database_id, list_id):
        """
            Retrieves a list from the specified main database and its replicas,
            merging the list objects from multiple databases.

            Args:
                main_database_id (int): The identifier of the main database.
                list_id (str): The identifier of the list to be retrieved.

            Returns:
                list: The merged list object or an empty list if not found.
        """
        original_db_id = main_database_id
        main_database_id = self.__find_real_main_db_id(main_database_id)
        self.database_connections_num_requests[main_database_id] += 1
        res = self.merge_list(original_db_id, list_id)
        if res is None:
            return []
        return res

    def close_databases(self):
        """
            Closes all the database connections and the environment.
        """
        # Close all the database connections
        for db_id, database in self.database_connections.items():
            database.close()
        self.env.close()

    def get_num_connections(self):
        """
            Returns the number of active database connections.

            Returns:
                int: The number of active database connections.
        """
        return len(self.database_connections)

    def __new_initialize_databases(self):
        """
            Initializes new connections to databases inside the "databases" folder.
        """
        names = [str(x) + ".db" for x in range(9)]
        for name in names:
            file_path = os.path.join(self.DATABASES_PATH, name)
            db_id = int(file_path[:file_path.rindex(".")].split('/')[-1])
            db = bdb.DB(self.env)
            db.open(file_path, dbtype=bdb.DB_HASH, flags=(bdb.DB_CREATE | bdb.DB_AUTO_COMMIT))
            self.database_connections[db_id] = db
            self.database_connections_state[db_id] = True
            self.database_connections_num_requests[db_id] = 0

    def create_database(self):
        """
            Creates a new database and initializes a connection to it.

            Returns:
                int: The identifier of the newly created database.
        """
        new_db_id = max(self.database_connections.keys()) + 1
        name = str(new_db_id) + ".db"
        file_path = os.path.join(self.DATABASES_PATH, name)
        db = bdb.DB(self.env)
        db.open(file_path, dbtype=bdb.DB_HASH, flags=(bdb.DB_CREATE | bdb.DB_AUTO_COMMIT))
        self.database_connections[new_db_id] = db
        self.database_connections_state[new_db_id] = True
        self.database_connections_num_requests[new_db_id] = 0
        return new_db_id

    def __insert_list(self, main_database_id, list_object):
        """
            Inserts a list object into the specified main database.

            Args:
                main_database_id (int): The identifier of the main database.
                list_object (dict): The list object to be inserted.
        """
        txn = self.__begin_transaction()
        database = self.database_connections[main_database_id]
        database.put(list_object['id'].encode('utf-8'), json.dumps(list_object).encode('utf-8'), txn=txn)
        txn.commit()

    def __retrieve_list(self, database_id, list_id):
        """
            Retrieves a JSON data object from the specified database by ID.

            Args:
                database_id (int): The identifier of the database.
                list_id (str): The identifier of the list to be retrieved.

            Returns:
                bytes or None: The retrieved JSON data object or None if not found.

        """
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
        """
            Prints all lists from each connected database.
        """
        for db_id in range(self.get_num_connections()):
            print(f"DB {db_id}:")
            print(self.__retrieve_lists(db_id))

    def __retrieve_lists(self, main_database_id):
        """
            Retrieves all items from the specified main database.

            Args:
                main_database_id (int): The identifier of the main database.

            Returns:
                list or None: A list of items or None if not found.
        """
        txn = self.__begin_transaction()
        database = self.database_connections[main_database_id]
        res = database.items()
        txn.commit()
        if res is not None:
            return res
        return None

    def __delete_list(self, main_database_id, list_id):
        """
            Deletes a list from the specified main database by ID.

            Args:
                main_database_id (int): The identifier of the main database.
                list_id (str): The identifier of the list to be deleted.
        """
        list_id = str(list_id)
        txn = self.__begin_transaction()
        database = self.database_connections[main_database_id]
        try:
            database.delete(list_id.encode('utf-8'), txn=txn)
        except:
            print("Couldn't delete list")
        txn.commit()

    def __begin_transaction(self):
        """
            Begins a transaction using the environment.

            Returns:
                bdb.DB_TXN: The transaction object.
        """
        txn = self.env.txn_begin()
        return txn

    def __initialize_environment(self):
        """
            Initializes the Berkeley DB environment.

            Returns:
                bdb.DBEnv: The Berkeley DB environment.
        """
        env = bdb.DBEnv()
        env.open(self.DATABASES_PATH, bdb.DB_INIT_MPOOL | bdb.DB_CREATE | bdb.DB_INIT_TXN | bdb.DB_INIT_LOG)
        return env

    def __next_db(self, curr_db):
        """
            Finds the next database in the sequence of database IDs.
            Args:
                curr_db (int): The current database ID.
            Returns:
                int: The next database ID in sequence.
        """
        db_ids = list(self.database_connections.keys())
        next_db = db_ids[db_ids.index(curr_db) + 1] if db_ids.index(curr_db) + 1 != len(db_ids) else db_ids[0]
        return self.__find_real_main_db_id(next_db)

    def __in_a_row_dbs(self, list_dbs):
        """
            Checks if the given list of databases is in a sequential order.
            Args:
                list_dbs (list): List of database IDs.
            Returns:
                bool: True if the databases are in sequential order; otherwise, False.
        """
        db_ids = list(self.database_connections.keys())
        i = db_ids.index(list_dbs[0])
        for j in range(1, len(list_dbs)):
            if db_ids[(i + j) % len(db_ids)] != list_dbs[j % len(list_dbs)]:
                return False
        return True

    def __get_db_and_replicas(self, main_database_id):
        """
            Retrieves the main database and its replicas.
            Args:
                main_database_id (int): The identifier of the main database.
            Returns:
                list: List of database IDs including the main database and its replicas.
        """
        dbs = [main_database_id]
        for i in range(self.num_replicas):
            dbs.append(self.__next_db(dbs[-1]))
        return dbs

    def apply_changelogs(self, list_object, changelogs):
        """
            Applies a series of changelogs to the given list_object.
            Args:
                list_object (dict): The list object to be modified.
                changelogs (list): List of changelogs to be applied.
            Returns:
                None
        """
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

    def add_changelogs(self, main_database_id, list_id, changelogs):
        """
            Add a set of changelogs to the specified list in the given database and its replicas.
            Args:
                main_database_id (int): The main database ID.
                list_id (str): The ID of the list to which changelogs are added.
                changelogs (list): List of changelogs to be added.
            Returns:
                bool: True if the operation is successful, False otherwise.
        """
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
        """
            Merge the specified list across databases and apply the accumulated changelogs.
            Args:
                main_database_id (int): The main database ID.
                list_id (str): The ID of the list to be merged.
            Returns:
                dict: The merged list object.
        """
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
        """
            Search for a list with the given ID across databases.
            Args:
                list_id (str): The ID of the list to search for.
            Returns:
                dict or None: The list object if found, None otherwise.
        """
        for i in range(self.get_num_connections()):
            if self.database_connections_state[i]:
                for l in self.__retrieve_lists(i):
                    if l[0].decode('utf-8') == list_id:
                        res = json.loads(l[1].decode('utf-8'))
                        return res
        return None
