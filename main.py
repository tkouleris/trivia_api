from flask import Flask

from OpenTDB import OpenTDB
import Categories

app = Flask(__name__)


@app.route("/")
def hello_world():
    opentdb = OpenTDB()
    return opentdb.get("10", Categories.GENERAL_KNOWLEDGE, 'easy')
