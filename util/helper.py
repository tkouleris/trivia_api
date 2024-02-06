import jwt
from flask import request

import models
from app import app


def get_user():
    token = request.headers.get('Authorization').replace('Bearer ', '')
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
    email = payload['email']
    return models.User.query.filter_by(email=email).first()