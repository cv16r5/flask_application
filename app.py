
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 20:12:29 2019

@author: admin5
"""


from flask import (Flask,
                   g,
                   jsonify,
                   request
                   )

from wtforms import (Form,
                     StringField, 
                     validators,
                     IntegerField
                     )

from functools import wraps
import sqlite3

#import os
app = Flask(__name__)

#os.chdir(r'/home/admin5/python_project/level-up-python/')

DATABASE='chinook.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.execute('PRAGMA foreign_keys = ON')
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, error, status_code=None, payload=None):
        super().__init__(self)
        self.error = error
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.error
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response





@app.route('/tracks', methods = ['GET','POST'])
def tracks():
    if request.method=='GET':
        return get_tracks()
    else:
        return post_new_record()
        

class TracksRegistrationForm(Form):
    name_artist=StringField(validators=[validators.optional()])
    per_page=IntegerField(validators=[validators.optional(),validators.number_range(min=1)])
    page=IntegerField(validators=[validators.optional(),validators.number_range(min=1)])
    
def to_json(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if func:
            result=jsonify([row[0] for row in func().fetchall()])
            return result
        return func(*args,**kwargs)
    return wrapper

@to_json
def get_tracks():
    db = get_db()
    
    form=TracksRegistrationForm(request.args)
    
#    additional
    if not form.validate():
        return jsonify(error=form.error)
    
    per_page=form.data['per_page'] or -1
    limit=per_page
    
    page=form.data['page'] or 0
    page_index=page-1
    offset=page_index*per_page
    
    if form.data['name_artist']:
        
        data = db.execute(
                '''
                SELECT tracks.name FROM tracks
                JOIN albums ON tracks.albumid = albums.albumid
                JOIN artists ON albums.artistid = artists.artistid
                where artists.name =?
                order by tracks.name COLLATE NOCASE LIMIT ? OFFSET ?;''',
                (form.data['name_artist'],limit,offset))
    else:
        data = db.execute(
                '''SELECT Name FROM tracks ORDER BY Name 
                COLLATE NOCASE LIMIT ? OFFSET ?''',
                (limit,offset))
    
    return data

def post_new_record():
    db = get_db()

    new_track = request.get_json()
    column_name = db.execute(
                'PRAGMA table_info(tracks);' ).fetchall()
    for clname in column_name:
        if new_track.get(clname[1]) and clname[1]!='TrackId'is None:
             raise InvalidUsage('missing {} in request data').format(clname[0])
   
    
    
    try:
        db.execute(
            'INSERT INTO tracks ( Name, AlbumId, MediaTypeId, '
           ' GenreId, Composer, Milliseconds, Bytes, UnitPrice) '
            'VALUES ( :Name, :AlbumId, :MediaTypeId,'
            ':GenreId, :Composer, :Milliseconds, :Bytes, :UnitPrice;',
            new_track
        )
        db.commit()
    
    except sqlite3.IntegrityError as error:

        db.rollback()
        error_reason = error.args[0]

        if error_reason.startswith('UNIQUE constraint failed'):
            raise InvalidUsage('Track already exists in ')

        elif error_reason.startswith('FOREIGN KEY constraint failed'):
            raise InvalidUsage('No country with album_id')

        else:
            raise error

    db_track = db.execute(
        'SELECT * FROM tracks '
        'where tracks.Name=:Name and'
        'tracks.AlbumId=:AlbumId and  tracks.MediaTypeId=:MediaTypeId and'
            'tracks.GenreId=:GenreId and tracks.Composer= :Composer and '
            'tracks.Milliseconds= :Milliseconds and tracks.Bytes= :Bytes'
            ' and tracks.UnitPrice= :UnitPrice;',
        new_track
    ).fetchone()

    return jsonify(dict(db_track))


@app.route('/genres', methods = ['GET'])
def genres():
    db = get_db()
    data = db.execute('''
                SELECT genres.name, count(tracks.Name) FROM tracks
                JOIN genres ON tracks.GenreId = genres.GenreId
                GROUP BY genres.name order by genres.name COLLATE NOCASE;'''
                ).fetchall()
    return jsonify(dict(data))
    
 
    


#if __name__ == '__main__':
#    app.run(debug=True, use_debugger=False)    
    
    
    
    