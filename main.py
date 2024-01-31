# from flask import Flask
from flask import Blueprint

from . import Categories
from .OpenTDB import OpenTDB

# from . import db

main = Blueprint('main', __name__)


# app = Flask(__name__)


@main.route("/")
def hello_world():
    opentdb = OpenTDB()
    return opentdb.get("10", Categories.GENERAL_KNOWLEDGE, 'easy')
