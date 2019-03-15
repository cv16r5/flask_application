from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/method', methods=[`GET`, `POST`, `PUT`, `DELETE`])
def show_method():
    return request.method


