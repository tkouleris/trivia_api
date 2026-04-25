from datetime import timedelta, datetime
from flask import Blueprint, jsonify
from flask import request
from flask_mail import Message
from models import User
from app import db, app, token_required, mail
from util.helper import get_user
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import secrets

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

    token = jwt.encode({'email': user.email, 'expiration': str(datetime.utcnow() + timedelta(minutes=43200))},
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

@auth.route("/verify", methods=['GET'])
@token_required
def verify():
    user = get_user()
    return {'status': 0, 'data': user.username}, 200


@auth.route('/request-reset-password', methods=['POST'])
def request_reset_password():
    data = request.get_json()
    if 'email' not in data:
        return {'status': 0, 'message': 'email missing'}, 400

    email = data['email']
    user = User.query.filter_by(email=email).first()

    if user:
        token = secrets.token_urlsafe(32)
        user.forgot_password_token = token
        db.session.commit()

        msg = Message("Password Reset Request",
                      recipients=[email])
        msg.body = (f"To reset your password, visit the following link: {request.host_url}confirm-reset-password \r\n "
                    f"and use this {token} token to reset your password")
        mail.send(msg)

    return {'status': 1, 'message': 'If the email exists, a password reset link has been sent.'}

@auth.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    if not all(k in data for k in ('email', 'token', 'password')):
        return {'status': 0, 'message': 'missing fields'}, 400

    email = data['email']
    token = data['token']
    password = data['password']

    user = User.query.filter_by(email=email, forgot_password_token=token).first()

    if not user:
        return {'status': 0, 'message': 'invalid email or token'}, 404

    user.password = generate_password_hash(password, method="scrypt")
    user.forgot_password_token = None
    db.session.commit()

    return {'status': 1, 'message': 'Password has been reset successfully.'}
