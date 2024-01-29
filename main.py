from flask import Flask
import requests
from urllib.parse import unquote

app = Flask(__name__)


@app.route("/")
def hello_world():
    print(unquote("Alejandro%20G.%20I%C3%B1%C3%A1rritu"))
    url = "https://opentdb.com/api.php?amount=10&encode=url3986"
    response = requests.get(url)
    return response.json()
