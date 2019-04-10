import os

#os.chdir(r'/home/admin5/python_project/level-up-python/')
from flask import Flask, abort, render_template, request,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from wtforms import (Form,
                     StringField, 
                     validators,
                     IntegerField
                     )
from cerberus import Validator
from sqlalchemy import func
import models
from models import Base


DATABASE_URL = os.environ['DATABASE_URL']

#engine = create_engine("postgresql://postgres:test1234@localhost:5432/chinook")
engine = create_engine(DATABASE_URL)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base.query = db_session.query_property()

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


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


@app.route("/longest_tracks")
def longest_tracks():
    try:
        tracks = db_session.query(models.Track).order_by(models.Track.milliseconds.desc()).limit(10).all() 
        result=[]
        for j,row in enumerate(tracks):
            list_result=({c.name: str(getattr(row,c.name)) for c in row.__table__.columns})          
            result.append(dict(list_result))
        return jsonify(result)
    except Exception as e:
        return e

class TracksRegistrationForm(Form):
    artist=StringField(validators=[validators.optional()])    


@app.route("/longest_tracks_by_artist")
def longest_tracks_by_artist():
    a = request.args
    if ('artist' in a):
        art = a['artist']

    else:
        abort(404)
        
    try:
        tracks = db_session.query(models.Track).join(models.Track.album).join(models.Album.artist).filter(models.Artist.name == art).order_by(models.Track.milliseconds.desc()).limit(10).all()
        result = []
        for j,row in enumerate(tracks):
            list_result=({c.name: str(getattr(row,c.name)) for c in row.__table__.columns})          
            result.append(dict(list_result))
                
        if len(result) == 0:
            abort(404)

    except:
        abort(404)

    return jsonify(result)



@app.route("/artists", methods=["POST"])
def artists():
    if request.method == "POST":
        return post_artists()
    abort(405)

def post_artists():
    data = request.json
    new_name = data.get("name")
    if new_name is None:
        abort(400)
    if isinstance(new_name,str) is False and len(new_name)>200:
        abort(400)
        
    art = models.Artist(name = new_name)
    db_session.add(art)
    db_session.commit()
    
    row = db_session.query(models.Artist).filter(models.Artist.name == new_name).first()
    result = []
    list_result=({c.name: str(getattr(row,c.name)) for c in row.__table__.columns})          
    result.append(dict(list_result))

    return jsonify(result)




#@app.route("/longest_tracks_by_artist")
#def get_artist():
#    form=TracksRegistrationForm(request.args)
#    
#    if not form.validate():
#        return jsonify(error=form.error)
#    
#    if  form.data['artist'] is None:
#        return str(404)
#    
#    name_artist=form.data['artist']
#    
#    try:
#        tracks = db_session.query(models.Track).filter(models.Track.composer==name_artist).order_by(models.Track.milliseconds.desc()).limit(10).all() 
#        result=[]
#        for j,row in enumerate(tracks):
#            list_result=({c.name: str(getattr(row,c.name)) for c in row.__table__.columns})          
#            result.append(dict(list_result))
#        if len (result)<1:
#            abort(404)
#            return str(404)
#        else:
#            return jsonify(result)
#    except Exception as e:
#        return 405
 
#if __name__ == "__main__":
#    app.run(debug=False)



## Aaron Goldberg , 202
#def patch_artist():
#    data = request.json
#    artist_id = data.get("artist_id")
#    new_name = data.get("name")
#    if artist_id is None:
#        abort(404)
#    artist = (
#        db_session.query(models.Artist)
#        .filter(models.Artist.artist_id == artist_id)
#        .with_for_update()
#        .one()
#    )
#    artist.name = new_name
#    db_session.add(artist)
#    db_session.commit()
#    return "OK"






