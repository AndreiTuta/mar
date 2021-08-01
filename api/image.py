from flask import Blueprint, request, Response
from api.models import *
import json

image_blueprint=Blueprint("image", __name__)

@image_blueprint.route("/new", methods=["POST"])
def index():
    c = Image(request.args.get('link'),request.args.get('album'), request.args.get('desc'))
    c.add()
    return c.as_dict()

@image_blueprint.route("/all", methods=["GET"])
def get_all_images():
    c = Image.query.all()
    results = []
    for image in c:
        results.append(image.as_dict())
    print(results)
    return Response(json.dumps(results),  mimetype='application/json')

@image_blueprint.route("/<code>", methods=["GET"])
def fetch_image(code: str):
    c= Image.query.filter_by(code=code).first()
    return c.as_dict()

@image_blueprint.route("/<code>", methods=["PUT"])
def update_image(code: str):
    c= Image.query.filter_by(code=code).first()
    c.update(request.args.get('link'),request.args.get('album'), request.args.get('desc'))
    return c.as_dict()