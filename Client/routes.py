from flask import Blueprint, render_template, redirect, request, session
import requests
import zmq
import json
import hashlib
from time import sleep


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
    list_server = socket.recv_json()
    print(type(list_server))
    print(list_server)
    return list_server


@bp.route('/req/addToList', methods=['POST'])
def add_to_list():
    data = request.get_json()
    print(data)
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "AddItem", "token": session['token'], "name": data.get('item_name'),
            "quantity": data.get('quantity'), "list_id": data.get('list_id')}
    socket.send_json(data)
    res = socket.recv_json()
    return res


@bp.route('/req/removeList', methods=['POST'])
def remove_list():
    data = request.get_json()
    print(data)
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "DeleteList", "token": session['token'], "list_id": data.get('list_id')}
    socket.send_json(data)
    res = socket.recv_json()
    return res


@bp.route('/req/removeItem', methods=['POST'])
def remove_item():
    data = request.get_json()
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "DeleteItem", "token": session['token'], "name": data.get('name'),
            "list_id": data.get('list_id')}
    socket.send_json(data)
    res = socket.recv_json()
    return res


@bp.route('/req/renameItem', methods=['POST'])
def rename_item():
    data = request.get_json()
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "RenameItem", "token": session['token'], "name": data.get('item_name'),
            "newName": data.get('new_item_name'), "list_id": data.get('list_id')}
    socket.send_json(data)
    res = socket.recv_json()
    return res


@bp.route('/req/buyItem', methods=['POST'])
def buy_item():
    data = request.get_json()
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "BuyItem", "token": session['token'], "name": data.get('name'), "list_id": data.get('list_id'),
            "quantity": data.get('quantity')}
    socket.send_json(data)
    res = socket.recv_json()
    return res


@bp.route('/req/cloudHash/<list_id>')
def cloud_hash(list_id):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "GetListHash", "token": session['token'], "list_id": list_id}
    socket.send_json(data)
    sleep(1)
    res = socket.recv_json()
    return res


@bp.route('/req/list_id/<list_name>')
def list_id(list_name):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    data = {"type": "GetListID", "token": session['token'], "list_name": list_name}
    socket.send_json(data)
    sleep(1)
    res = socket.recv_json()
    return res


@bp.route('/req/synchronize/<list_id>', methods=['POST'])
def synchronize(list_id):
    data = request.get_json()
    print(data)
    print(list_id)
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    if 'name' in data:
        data = {"type": "Synchronize", "token": session['token'], "list_id": list_id, "list_name": data['name'], "changelog": data['changes']}
    else:
        data = {"type": "Synchronize", "token": session['token'], "list_id": list_id, "changelog": data}
    socket.send_json(data)
    sleep(1)
    res = socket.recv_json()
    print(res)
    return res


@bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.SNDTIMEO, 1000)  # Setting a send timeout of 1000 milliseconds
    socket.setsockopt(zmq.IMMEDIATE, 1)


    try:
        socket.connect("tcp://localhost:5575")
        data = {"type": "Login", "email": email, "password": password}
        socket.send_json(data)
        response = socket.recv_json()
    except:
        return render_template('login.html', error_message="Server Timeout")

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
    socket.setsockopt(zmq.SNDTIMEO, 1000)  # Setting a send timeout of 1000 milliseconds
    socket.setsockopt(zmq.IMMEDIATE, 1)

    try:
        socket.connect("tcp://localhost:5575")
        data = {"type": "Register", "email": email, "password": password}
        socket.send_json(data)
        response = socket.recv_json()
    except:
        return render_template('register.html', error_message="Server Timeout")

    if "error" in response:
        return render_template('register.html', error_message=response["error"])

    data.update({"type": "Login"})
    socket.send_json(data)
    response = socket.recv_json()

    session['token'] = response["token"]
    return redirect('/home')
