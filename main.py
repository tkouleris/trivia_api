from flask import Flask
import requests
from urllib.parse import unquote

from QuestionTransformer import QuestionTransformer

app = Flask(__name__)


def myfunction():
    return 0.5


@app.route("/")
def hello_world():
    url = "https://opentdb.com/api.php?amount=10&encode=url3986"
    response = requests.get(url)
    json = response.json()
    transformer = QuestionTransformer()
    return transformer.run(json['results'])
