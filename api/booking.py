from flask import Blueprint, request
from api.models import *
from flask import Flask
from flask_cors import cross_origin

booking_blueprint = Blueprint("booking", __name__)


@booking_blueprint.route("/new", methods=["POST"])
@cross_origin(origin='*')
def new():
    b = Booking(request.args.get('customer'), request.args.get('date'))
    b.add()
    return b.as_dict()


@booking_blueprint.route("/<id>", methods=["GET"])
@cross_origin(origin='*')
def fetch_booking(id: str):
    b = Booking.query.filter_by(id=id).first()
    if b is not None:
        return b.as_dict()
    return "", 404


@booking_blueprint.route("/period", methods=["GET"])
@cross_origin(origin='*')
def fetch_bookings_in_period():
    start = request.args.get('start')
    end = request.args.get('end')
    b = Booking.query.filter(Booking.date > start, Booking.date < end).all()
    results = {}
    if len(b) > 0:
        for booking in b:
            results[booking.id] = booking.as_dict()
        return results
    return ""
