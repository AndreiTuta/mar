from flask import Blueprint, request, Response
from api.models import *
import json

album_blueprint=Blueprint("album", __name__)

@album_blueprint.route("/new", methods=["POST"])
def index():
    c = Album(request.args.get('name'),str(request.args.get('private')) == "True")
    c.add()
    return c.as_dict()

@album_blueprint.route("/all", methods=["GET"])
def get_all_albums():
    c = Album.query.all()
    results = []
    for album in c:
        results.append(album.as_dict())
    print(results)
    return Response(json.dumps(results),  mimetype='application/json')

@album_blueprint.route("/<name>", methods=["GET"])
def fetch_album(name: str):
    c= Album.query.filter_by(name=name).first()
    return c.as_dict()

@album_blueprint.route("/<name>", methods=["PUT"])
def update_album(name: str):
    c= Album.query.filter_by(name=name).first()
    c.update(request.args.get('name'),request.args.get('date'), request.args.get('private') == "True")
    return c.as_dict()