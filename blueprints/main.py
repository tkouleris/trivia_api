from flask import Blueprint
import Categories
from OpenTDB import OpenTDB


main = Blueprint('main', __name__)


# app = Flask(__name__)


@main.route("/")
def hello_world():
    opentdb = OpenTDB()
    return opentdb.get("10", Categories.GENERAL_KNOWLEDGE, 'easy')
