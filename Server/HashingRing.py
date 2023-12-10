import random


class HashingRing:

    def __init__(self, num_databases):
        """
            Initializes a HashingRing instance.

            Args:
                num_databases (int): The number of databases (nodes) in the hashing ring.
        """
        self.nodes_positions = dict()
        self.num_databases = num_databases
        random.seed(100)  # best seed to balanced loads
        self.divide_hash_ring_into_segments()

    """
        Divides the hash ring into segments for each database, assigning random positions to virtual nodes.

        Returns:
            dict: A dictionary mapping each database identifier to a list of random positions.
    """
    def divide_hash_ring_into_segments(self):
        for database_id in range(self.num_databases):
            positions = [random.randint(1, 2 ** 128 - 1) for _ in range(3)]  # adding virtual nodes
            self.nodes_positions[database_id] = positions

        return self.nodes_positions

    def get_main_nodes_positions(self):
        """
            Gets the positions of the main nodes (original, not virtual) for each database.

            Returns:
                list: A list of tuples containing the database identifier and the position of its main node.
        """
        res = []
        for db_id, positions_list in self.nodes_positions.items():
            res.append((db_id, positions_list[0]))
        return sorted(res, key=lambda x: x[1])

    def find_main_database_id(self, request_id_hash):
        """
            Finds the main database identifier responsible for a given hashed request identifier.

            Args:
                request_id_hash: The hashed request identifier.

            Returns:
                int: The identifier of the main database responsible for the given hash.
        """
        smallest_greater = None
        database_identifier = None
        request_id_hash = int(request_id_hash, 16)

        for identifier, values in self.nodes_positions.items():
            for value in values:
                if value > request_id_hash:
                    if smallest_greater is None or value < smallest_greater:
                        smallest_greater = value
                        database_identifier = identifier

        if database_identifier is None:
            smallest_value = 2 ** 128 - 1
            for identifier, values in self.nodes_positions.items():
                tmp_smallest = min(values)
                if tmp_smallest < smallest_value:
                    smallest_value = tmp_smallest
                    database_identifier = identifier
        return database_identifier
