from flask import Blueprint, render_template, redirect, request, session
import requests
from time import sleep
import zmq


def if_token(return_good, return_bad):
    if "token" in session:
        return return_good
    return return_bad


def login_token_request(email, password):
    url = "http://localhost:8000/token"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "email": email,
        "password": password,
    }

    return requests.post(url, headers=headers, data=data)


def create_user(username, email, password):
    url = "http://localhost:8000/users/"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    data = {
        "name": username,
        "email": email,
        "password": password,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return True
    else:
        return False


bp = Blueprint('api', __name__)


# GET

@bp.route('/')
def redirect_index():
    return if_token(redirect('/offline'), render_template('offline.html'))


@bp.route('/test')
def test():
    return if_token(redirect('/test'), render_template('test.html'))


@bp.route('/login')
def login():
    return if_token(redirect('/home'), render_template('login.html'))


@bp.route('/register')
def register():
    return if_token(redirect('/home'), render_template('register.html'))


@bp.route('/home')
def home():
    return if_token(render_template('home.html'), redirect('/login'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# POST

@bp.route('/test/createList', methods=['POST'])
def create_list():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "CreateList", "token": "", "name": "Lista de Teste",
            "items": [{"name": "peaches", "quantity": 3}, {"name": "pencils", "quantity": 1}]}
    socket.send_json(data)
    
    return redirect('/test')


@bp.route('/test/addToList', methods=['POST'])
def add_to_list():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")

    list_name = request.form['list']

    print(list_name)
    data = {"type": "AddItem", "token": "", "name": "bananas", "quantity": 6, "list_id": 1}
    socket.send_json(data)
    
    return redirect('/test')


@bp.route('/test/removeList', methods=['POST'])
def remove_list():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "DeleteList", "token": "", "list_id": 1}
    socket.send_json(data)
    
    return redirect('/test')

@bp.route('/test/removeItem', methods=['POST'])
def remove_item():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "DeleteItem", "token": "", "name": "bananas", "list_id": 1}
    socket.send_json(data)
    
    return redirect('/test')

@bp.route('/test/renameItem', methods=['POST'])
def rename_item():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "RenameItem", "token": "", "name": "bananas", "newName": "apples", "list_id": 1}
    socket.send_json(data)
    
    return redirect('/test')


@bp.route('/test/buyItem', methods=['POST'])
def buy_item():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "BuyItem", "token": "", "name": "bananas", "list_id": 1}
    socket.send_json(data)
    
    return redirect('/test')


@bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5569")
    data = {"type": "Login", "email": email, "password": password}
    socket.send_json(data)
    response = socket.recv_json()

    if "error" in response:
        return render_template('login.html', error_message=response["error"])

    session['token'] = response["token"]
    return redirect('/home')


@bp.route('/register', methods=['POST'])
def register_post():
    print(request.form)
    email = request.form.get('email')
    password = request.form.get('password')

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5569")
    data = {"type": "Register", "email": email, "password": password}
    print(data)
    socket.send_json(data)
    response = socket.recv_json()

    if "error" in response:
        return render_template('register.html', error_message=response["error"])

    data.update({"type": "Login"})
    socket.send_json(data)
    response = socket.recv_json()

    session['token'] = response["token"]
    return redirect('/home')
