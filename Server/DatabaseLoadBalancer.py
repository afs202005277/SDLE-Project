from HashingRing import HashingRing


# Round Robin load balancer among groups of databases
# The hashing ring returns the main database identifier to route the request
# This class routes the request to the specific database instance of the group
class DatabaseLoadBalancer:
    def __init__(self, num_connections, num_replicas_in_group):
        self.last_ids = dict((x, 0) for x in range(num_connections))
        self.num_replicas_in_group = num_replicas_in_group

    def route_to_database(self, main_target_id):
        self.last_ids[main_target_id] = (self.last_ids[main_target_id] + 1) % self.num_replicas_in_group[main_target_id]
        destination = self.last_ids[main_target_id]
        return destination


if __name__ == '__main__':
    from DatabaseManagement import DatabaseManagement
    database_management = DatabaseManagement()
    load_balancer = DatabaseLoadBalancer(database_management.get_num_primary_connections(),
                                         database_management.get_num_replicas_connections())
    hashing_ring = HashingRing(database_management.get_num_primary_connections())

    results = dict()
    for main_connection, db_list in database_management.get_num_replicas_connections().items():
        for replica in range(db_list):
            results[(main_connection, replica)] = 0
    for i in range(10000):
        main_connection_id = hashing_ring.find_main_database_id(HashingRing.compute_md5_hash(i))
        replica_id = load_balancer.route_to_database(main_connection_id)
        results[(main_connection_id, replica_id)] += 1
    print(results)
