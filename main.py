from flask import Flask
# import requests
# from urllib.parse import unquote
from OpenTDB import OpenTDB

# from QuestionTransformer import QuestionTransformer

app = Flask(__name__)


@app.route("/")
def hello_world():
    opentdb = OpenTDB()
    return opentdb.get("10", "9", 'easy')
    # url = "https://opentdb.com/api.php?amount=10&encode=url3986"
    # response = requests.get(url)
    # json = response.json()
    # transformer = QuestionTransformer()
    # return transformer.run(json['results'])
