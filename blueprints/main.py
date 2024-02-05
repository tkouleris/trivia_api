from flask import Blueprint
import Categories
from OpenTDB import OpenTDB
from app import token_required

main = Blueprint('main', __name__)


# app = Flask(__name__)

@main.route('/test', methods=['GET'])
@token_required
def locked():
    return "Locked"

@main.route("/trivia/general")
@token_required
def hello_world():
    opentdb = OpenTDB()
    return opentdb.get("10", Categories.GENERAL_KNOWLEDGE, 'easy')
