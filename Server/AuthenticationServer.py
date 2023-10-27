import zmq
import os, sys
import hashlib
import uuid
import datetime
import env

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(f'{ROOT_DIR}/')

from AuthenticationManagement import AuthenticationManagement


class AuthenticationServer:

    def __init__(self):
        self.expiration_date_days = 30
        self.authentication_management = AuthenticationManagement()
        self.request_handlers = {'Login': self.login, 'Register': self.register}

    def login(self, request):
        email = request["email"]
        password = request["password"]
        if self.authentication_management.check_user_exists(email):
            new_token = self.authentication_management.create_access_token_expires(email)
            return {"token": str(new_token)}
        else:
            return {"error": "Invalid credentials"}
    
    def register(self, request):
        email = request["email"]
        password = request["password"]
        if not self.authentication_management.check_user_exists(email):
            self.authentication_management.create_user(email, password)
            return {"success": "User created"}
        else:
            return {"error": "User already exists"}

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(f'tcp://*:{env.AUTHENTICATION_SERVER_PORT}')

        while True:
            request = socket.recv_json()
            response = self.request_handlers[request['type']](request)
            socket.send_json(response)


if __name__ == '__main__':
    server = AuthenticationServer()
    server.run()

