from datetime import timedelta, datetime
from flask import Blueprint, jsonify
from flask import request
from models import User
from app import db, app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'email' not in data.keys():
        return {'status': 0, 'message': 'email missing'}, 400
    if 'password' not in data.keys():
        return {'status': 0, 'message': 'password missing'}, 400
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return {'status': 0, 'message': 'wrong credentials'}, 401

    token = jwt.encode({'email': user.email, 'expiration': str(datetime.utcnow() + timedelta(minutes=120))},
                       app.config['SECRET_KEY'], algorithm='HS256'
                       )
    response = jsonify({'token': token, 'username': user.username})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
    # return {'token': token, 'username': user.username}, 200


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

    user = User.query.filter_by(email=email).first()
    if user:
        return {'status': 0, 'message': 'user exists'}, 400

    new_user = User(email=email, username=username, password=generate_password_hash(password, method="scrypt"))
    db.session.add(new_user)
    db.session.commit()

    return {'status': 1, 'message': 'User created'}


@auth.route('/refresh', methods=['POST'])
def refresh():
    try:
        token = request.headers.get('Authorization').replace('Bearer ', '')
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        token = jwt.encode({'email': payload['email'], 'expiration': str(datetime.utcnow() + timedelta(minutes=120))},
                           app.config['SECRET_KEY'], algorithm='HS256')
    except:
        return {'status': 0, 'message': 'not valid token'}, 400

    return {'status': 1, 'token': token}
