from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/method', methods=['GET', 'POST', 'PUT', 'DELETE'])
def show_method():
    return request.method

@app.route('/show_data', methods = ['POST'])
def postJsonHandler():
    return jsonify(request.json)
    



