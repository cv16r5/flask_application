from flask import (Flask,
                   request,
                   jsonify
                   )


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/method', methods=['GET', 'POST', 'PUT', 'DELETE'])
def show_method():
    return str(request.method)

@app.route('/show_data', methods = ['POST'])
def post_json():
    return jsonify(request.json)

@app.route('/pretty_print_name', methods = ['POST'])
def post_client():
    name =request.json.get('name')
    surename=request.json.get('surename')
    return ('Na imię mu {}, a nazwisko jego {}').format(name,surename)

app.counter=0

@app.route('/counter')
def count_visits():
    app.counter+=1
    return(str(app.counter))
    







    



