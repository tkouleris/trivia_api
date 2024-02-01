from flask import Blueprint
from flask import request

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return 'Login'


@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if 'username' not in data.keys():
        return {'status': 0, 'message': 'username missing'}, 400
    if 'email' not in data.keys():
        return {'status': 0, 'message': 'email missing'}, 400
    if 'password' not in data.keys():
        return {'status': 0, 'message': 'password missing'}, 400

    username = data['username']
    email = data['email']
    password = data['password']
    return {'status': 1, 'message': 'User created'}


@auth.route('/logout')
def logout():
    return 'Logout'
