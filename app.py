import functools
import os
import datetime
import jwt
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin

def token_required(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        if 'Authorization' not in request.headers.keys():
            return {'message': 'Missing token'}, 400
        try:
            token = request.headers.get('Authorization').replace('Bearer ', '')
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')

            expires = payload['expiration'][:16]
            expires_timestamp = datetime.datetime.strptime(expires, "%Y-%m-%d %H:%M").timestamp()
            now_timestamp = datetime.datetime.utcnow().timestamp()
            if now_timestamp > expires_timestamp:
                return {'message': 'Token expired'}, 400

            email = payload['email']
            user = models.User.query.filter_by(email=email).first()
            if not user:
                return {'message': 'Invalid username'}, 400
            return func(*args, **kwargs)
        except:
            return {'message': 'invalid token'}, 400

    return decorated


def init_blueprints():
    # blueprint for auth routes in our app
    from blueprints import auth as auth_blueprint
    app.register_blueprint(auth_blueprint.auth)

    # blueprint for non-auth parts of app
    from blueprints import main as main_blueprint
    app.register_blueprint(main_blueprint.main)


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    return app


app = create_app()
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
import models

init_blueprints()

if __name__ == "__main__":
    app.run()
