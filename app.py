from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from multiprocessing import Value


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/method', methods=['GET', 'POST', 'PUT', 'DELETE'])
def show_method():
    return request.method

@app.route('/show_data', methods = ['POST'])
def post_json():
    return jsonify(request.json)

@app.route('/pretty_print_name', methods = ['POST'])
def post_client():
    data=request.json
    name =data['name']
    surename=data['surename']
    return ('Na imię mu {}, a nazwisko jego {}').format(name,surename)

counter = Value('i', 0)
@app.route('/counter')
def count_visits():
    with counter.get_lock():
        counter.value += 1
    return str(counter.value)




    



