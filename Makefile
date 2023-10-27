.PHONY: databases

default: all

# Define the targets for running the processes
all: run-client run-proxy run-server

# Define the commands for running the Flask web app client
run-client:
	cd Client && flask --app __init__.py --debug run &

# Define the commands for running the proxy process
run-proxy:
	cd Server && python3 proxy.py &

# Define the commands for running the server
run-server:
	cd Server && python3 Server_ZMQ.py &

# Define a target for stopping all running processes
stop:
	pkill -f "flask --app __init__.py --debug run" && echo "done1" ; true
	pkill -f "python3 proxy.py" && echo "done2" ; true
	pkill -f "python3 Server_ZMQ.py" && echo "done3" ; true

databases:
	@echo "Creating the 'databases' directory and subdirectories with files..."
	rm -rf databases/berkeley
	mkdir -p databases/berkeley
	touch databases/berkeley/0.db
	touch databases/berkeley/1.db
	touch databases/berkeley/2.db
	touch databases/berkeley/3.db
	touch databases/berkeley/4.db
	touch databases/berkeley/5.db
	touch databases/berkeley/6.db
	touch databases/berkeley/7.db
	touch databases/berkeley/8.db
	@echo "Finished creating the 'databases' directory and subdirectories with files."

