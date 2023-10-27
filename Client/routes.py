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
    return redirect('/login')




@bp.route('/login')
def login():
    return if_token(redirect('/home'), render_template('login.html'))


@bp.route('/register')
def register():
    return if_token(redirect('/home'), render_template('register.html'))


@bp.route('/home')
def home():
    return if_token(render_template('offline.html'), redirect('/login'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# POST

@bp.route('/req/createList', methods=['POST'])
def create_list():
    data = request.get_json()
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "CreateList", "token": session['token'], "list_name": data.get('list_name'), "items": []}
    socket.send_json(data)
    return ''


@bp.route('/req/addToList', methods=['POST'])
def add_to_list():
    data = request.get_json()
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "AddItem", "token": session['token'], "name": data.get('item_name'), "quantity": data.get('quantity'), "list_name": data.get('list_name')}
    socket.send_json(data) 
    return ''


@bp.route('/req/removeList', methods=['POST'])
def remove_list():
    data = request.get_json()
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "DeleteList", "token": session['token'], "list_name": data.get('list_name')}
    socket.send_json(data)
    return ''

@bp.route('/req/removeItem', methods=['POST'])
def remove_item():
    data = request.get_json()
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "DeleteItem", "token": session['token'], "name": data.get('name'), "list_name": data.get('list_name')}
    socket.send_json(data) 
    return ''

@bp.route('/req/renameItem', methods=['POST'])
def rename_item():
    data = request.get_json()
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "RenameItem", "token": session['token'], "name": data.get('item_name'), "newName": data.get('new_item_name'), "list_name": data.get('list_name')}
    socket.send_json(data)   
    return ''


@bp.route('/req/buyItem', methods=['POST'])
def buy_item():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "BuyItem", "token": session['token'], "name": "bananas", "list_id": 1}
    socket.send_json(data)  
    return ''


@bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5575")
    data = {"type": "Login", "email": email, "password": password}
    socket.send_json(data)
    response = socket.recv_json()

    if "error" in response:
        return render_template('login.html', error_message=response["error"])

    session['token'] = response["token"]
    return redirect('/home')


@bp.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    password = request.form.get('password')

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5575")
    data = {"type": "Register", "email": email, "password": password}
    socket.send_json(data)
    response = socket.recv_json()

    if "error" in response:
        return render_template('register.html', error_message=response["error"])

    data.update({"type": "Login"})
    socket.send_json(data)
    response = socket.recv_json()

    session['token'] = response["token"]
    return redirect('/home')
