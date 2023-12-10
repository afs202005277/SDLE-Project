#!/bin/bash

cd Client && flask --app __init__.py --debug run -p 6000 &
flask_pid=$!
echo "$flask_pid" > process_pids.txt

cd Server && python3 proxy.py &
proxy_pid=$!
echo "$proxy_pid" >> process_pids.txt

cd Server && python3 Server_ZMQ.py &
backend_pid=$!
echo "$backend_pid" >> process_pids.txt

cd Server && python3 AuthenticationServer.py &
auth_pid=$!
echo "$auth_pid" >> process_pids.txt

wait

