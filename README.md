# SDLE Project 23/24

## Local-first Shopping List Application

### Overview
This project is a cloud-based application designed for collaborative shopping lists with real-time updates. It ensures fault tolerance and high availability by leveraging Amazon DynamoDB, consistent hashing, replication, sharding, and failover techniques. The system enables multiple users to manage shopping lists efficiently while maintaining data integrity and accessibility.

## Features
- **Real-time Collaboration**: Multiple users can modify shopping lists simultaneously.
- **Fault Tolerance**: Uses consistent hashing and replication to ensure system reliability.
- **High Availability**: DynamoDB and sharding techniques guarantee data accessibility even in case of failures.
- **Authentication and Security**: Implements JWT-based authentication to protect user data.

## Installation and Setup

### Prerequisites
Ensure you have the following dependencies installed:
- [BerkeleyDB](https://docs.oracle.com/cd/E17076_05/html/installation/build_unix.html)
- [sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [python-jose](https://pypi.org/project/python-jose/)
- [passlib](https://pypi.org/project/passlib/)
- [typing](https://docs.python.org/3/library/typing.html)
- [zmq](https://zeromq.org/languages/python/)
- [hashlib](https://docs.python.org/3/library/hashlib.html)
- [json](https://docs.python.org/3/library/json.html)
- [berkeleydb](https://docs.jcea.es/berkeleydb/latest/)
- [threading](https://docs.python.org/3/library/threading.html)
- [prettytable](https://pypi.org/project/prettytable/)
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/)

### Running the Application
The system consists of multiple services that must be started in separate terminal instances:

#### 1. Start the Flask Web Server
```bash
cd Client && flask --app __init__.py --debug run -p 6969
```

#### 2. Start the ZMQ Proxy
```bash
cd Server && python3 proxy.py
```

#### 3. Start the ZMQ Server
```bash
python3 Server_ZMQ.py
```

#### 4. Start the Authentication Server
```bash
python3 AuthenticationServer.py
```

Once all services are running, access the web interface at: [http://localhost:6000](http://localhost:6000)

## Database Management
The ZMQ Server terminal listens for the following commands to manage database instances:

```
Available Commands:

    help        - Displays a list of available commands with descriptions.
    list        - Lists all existing databases with their IDs, statuses (ONLINE/OFFLINE), request counts, and number of shopping lists.
    create      - Creates a new database instance with an automatically assigned ID.
    enable [id] - Enables a currently disabled database.
    disable [id]- Disables an existing database.
    printlists  - Displays all shopping lists stored in the databases (Use with caution).
    quit        - Shuts down the server and this management terminal.
```

*Note: Commands requiring arguments will notify you if an invalid or missing argument is provided.*

## Team
| Name            | Student ID  |
| -------------- | ----------- |
| Alexandre Nunes | 202005358  |
| André Filipe Sousa | 202005277  |
| Gonçalo Pinto   | 202004907  |
| Pedro Fonseca   | 202008307  |
