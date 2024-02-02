from datetime import timedelta, datetime
from flask import Blueprint
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
    return {'token': token}, 200


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


@auth.route('/logout')
def logout():
    return 'Logout'
