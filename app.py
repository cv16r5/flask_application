from flask import Flask, request, Response, session, redirect, url_for, jsonify,render_template
from functools import wraps
import uuid 


app = Flask(__name__)
app.secret_key = 'my super secret key'.encode('utf8') 
app.trains = {}

@app.route('/')
def root():
    return 'Hello, World!'

def check_auth(username, password):
    return username == 'TRAIN' and password == 'TuN3L'

def please_authenticate():
    return Response('Not authorized.\n'
                    'Please try again', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_basic_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return please_authenticate()
        return func(*args, **kwargs)
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
@requires_basic_auth
def login():
    session['username'] = request.authorization.username
    return redirect(url_for('hello'))

def requires_user_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper

@app.route('/hello')
@requires_user_session
def hello():
    return render_template('hello.html', user =session['username'])

@app.route('/logout', methods=['GET', 'POST'])
@requires_user_session
def logout():
    if request.method == 'GET':
        return redirect(url_for('root'))
    del session['username']
    return redirect(url_for('root'))


def get_train_from_json():
    train_data = request.get_json()
    if not train_data:
        raise 'Please provide json data'
    return train_data


def set_train(train_id=None, data=None, update=False):
    if train_id is None:
        train_id = str(uuid.uuid4())

    if data is None:
        data = get_train_from_json()
        if data is None:
            raise ('Please provide json data')

    if update:
        app.trains[train_id].update(data)
    else:
        app.trains[train_id] = data

    return train_id


@app.route('/trains', methods=['GET', 'POST'])
@requires_user_session
def trains():
    if request.method == 'GET':
        return jsonify(app.trains)
    elif request.method == 'POST':
        train_id = set_train()
        return redirect(url_for('train', train_id=train_id, format='json'))


@app.route('/trains/<train_id>',methods=['GET', 'DELETE'])
def fish(train_id):
    if train_id not in app.trains:
        return 'No such train', 404

    if request.method == 'DELETE':
        del app.trains[train_id]
        return '', 204

    if request.method == 'GET' and request.args.get('format') != 'json':
        raise ("Missing 'format=json' in query string.")
    return jsonify(app.trains[train_id])


