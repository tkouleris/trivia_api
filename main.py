from flask import Flask
import requests

app = Flask(__name__)


@app.route("/")
def hello_world():
    url = "https://opentdb.com/api.php?amount=10"
    response = requests.get(url)
    return response.json()
