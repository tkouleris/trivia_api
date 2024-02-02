import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv


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

    return app


app = create_app()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models
init_blueprints()

if __name__ == "__main__":
    app.run()
