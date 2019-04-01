#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 20:12:29 2019

@author: admin5
"""

import sqlite3
from flask import (Flask,
                   g,
                   jsonify
                   )

app = Flask(__name__)

DATABASE = '/home/admin5/python_project/level-up-python/sqlite_source/chinook.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route('/tracks', methods = ['GET','POST'])
def name_track():
    db = get_db()
    data = db.execute(
        'SELECT Name FROM tracks ORDER BY Name ASC').fetchall()
    return jsonify(data)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#if __name__ == '__main__':
#    app.run(debug=True)
