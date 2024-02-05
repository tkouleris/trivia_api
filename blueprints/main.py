from flask import Blueprint, request
import Categories
from OpenTDB import OpenTDB
from app import token_required

main = Blueprint('main', __name__)

@main.route("/trivia", methods=['GET'])
@token_required
def hello_world():
    opentdb = OpenTDB()
    return opentdb.get("10", Categories.list[request.args['cat'].upper()], 'easy')
