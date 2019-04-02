import sqlite3
from flask import (Flask,
                   g,
                   jsonify,
                   request,
                   render_template
                   )
import os
app = Flask(__name__)

os.chdir(r'/home/admin5/python_project/level-up-python/')

DATABASE='chinook.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        
    return db

@app.route('/tracks', methods = ['GET'])
def name_track():
    id_artist = request.args.get('artist', None)
    per_page = request.args.get('per_page', type=int)
    nr_page = request.args.get('page', None) 
    db = get_db()
    if id_artist:
        data = db.execute(
                '''
                SELECT tracks.name FROM tracks
                JOIN albums ON tracks.albumid = albums.albumid
                JOIN artists ON albums.artistid = artists.artistid
                where artists.name =:id_artist
                order by tracks.name COLLATE NOCASE  limit :per_page;''',{"id_artist":id_artist,
                                              "per_page": str(per_page),
                                              "nr_page":nr_page  
                                                }).fetchall()
        
    else:
        data = db.execute(
                'SELECT Name FROM tracks ORDER BY Name COLLATE NOCASE ').fetchall()
   
    
    return jsonify([row[0] for row in data])
#    ab=type(data)




@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
