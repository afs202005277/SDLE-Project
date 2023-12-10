# SDLE Project 23/24

## Local-first shopping list application

## How to run

Note: It's needed to install the BerkeleyDB.

https://docs.oracle.com/cd/E17076_05/html/installation/build_unix.html

Required packages:
- [sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [jose](https://pypi.org/project/python-jose/)
- [passlib](https://pypi.org/project/passlib/)
- [typing](https://docs.python.org/3/library/typing.html)
- [zmq](https://zeromq.org/languages/python/)
- [hashlib](https://docs.python.org/3/library/hashlib.html)
- [json](https://docs.python.org/3/library/json.html)
- [berkeleydb](https://docs.jcea.es/berkeleydb/latest/)
- [threading](https://docs.python.org/3/library/threading.html)
- [prettytable](https://pypi.org/project/prettytable/)
- [jwt](https://pyjwt.readthedocs.io/en/stable/)

In 4 different terminal instances run the following services:

- Flask webserver

```bash
cd Client && flask --app __init__.py --debug run -p 6000
```

- ZMQ Proxy

```bash
cd Server && python3 proxy.py
```

- ZMQ Server

```bash
python3 Server_ZMQ.py
```

- Authentication Server

```bash
python3 AuthenticationServer.py
```

Access the web interface in http://localhost:6000

## How to disable/enable databases instances

The terminal that runs the ZMQ Server listens to commands:

```
Available Commands:

    **help** - Shows a list of the existing commands with a comprehensive explanation.

    **list** - Lists the current existing DBs. Shows their ids, current state (ONLINE, OFFLINE), number of requests and number of shopping lists.

    **create** - Creates a new DB for the server. The id of this DB is automatically assigned.

    **enable [id]** - Enables a currently disabled DB. Receives an argument id which represents the id of the DB.

    **disable [id]** - Disables an existing DB from the server. Receives an argument id which represents the id of the DB.

    **printlists** - Prints all the lists in the databases. WARNING: Only run when necessary.
    quit - Turns off the server and this management terminal.

Notes:
        Arguments can always be passed in front of any command. The only arguments that will ever be used are for commands that ask for them. Any command will alert in the case of a nonexistent/invalid argument.
```

## Team

| Name            | Number    |
| --------------- | --------- |
| Alexandre Nunes | 202005358 |
| André Filipe Sousa     | 202005277 |
| Gonçalo Pinto   | 202004907 |
| Pedro Fonseca   | 202008307 |
