import hashlib
import random


class HashingRing:

    def __init__(self, num_databases):
        self.nodes_positions = dict()
        self.num_databases = num_databases
        random.seed(100)  # best seed to balanced loads
        self.divide_hash_ring_into_segments()

    @staticmethod
    def compute_md5_hash(identifier):
        id_str = str(identifier)
        hash_obj = hashlib.md5(id_str.encode())
        return int(hash_obj.hexdigest(), 16)

    def divide_hash_ring_into_segments(self):
        for database_id in range(self.num_databases):
            positions = [random.randint(1, 2 ** 128 - 1) for _ in range(3)]  # adding virtual nodes
            self.nodes_positions[database_id] = positions

        return self.nodes_positions

    def get_main_nodes_positions(self):
        res = []
        for db_id, positions_list in self.nodes_positions.items():
            res.append((db_id, positions_list[0]))
        return sorted(res, key=lambda x: x[1])


    def find_main_database_id(self, request_id_hash):
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


if __name__ == '__main__':
    from DatabaseManagement import DatabaseManagement

    database_management = DatabaseManagement()
    hashing_ring = HashingRing(database_management.get_num_connections())
    print(hashing_ring.get_main_nodes_positions())
    results = dict((x, 0) for x in range(database_management.get_num_connections()))
    for i in range(10000):
        results[hashing_ring.find_main_database_id(HashingRing.compute_md5_hash(i))] += 1
    print(results)
