from api.models import *

def get_albums():
    return Album.query.all()

def get_album(album_id):
    return Album.query.filter_by(id=album_id).first()