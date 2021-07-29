from flask import Blueprint, request, Response
from models import *
import json

customer_blueprint=Blueprint("customer", __name__)

@customer_blueprint.route("/new", methods=["POST"])
def index():
    c = Customer(request.args.get('name'),request.args.get('last_name'), request.args.get('email'))
    c.add()
    return c.as_dict()

@customer_blueprint.route("/all", methods=["GET"])
def get_all_customers():
    c = Customer.query.all()
    results = []
    for customer in c:
        results.append(customer.as_dict())
    return Response(json.dumps(results),  mimetype='application/json')

@customer_blueprint.route("/<guid>", methods=["GET"])
def fetch_customer(guid: str):
    c= Customer.query.filter_by(guid=guid).first()
    bookings = Booking.query.filter(Booking.customer == c.id).all()
    c.bookings = [x.as_dict() for x in bookings]
    return c.as_dict()

@customer_blueprint.route("/<guid>", methods=["PUT"])
def update_customer(guid: str):
    c= Customer.query.filter_by(guid=guid).first()
    c.update(request.args.get('name'),request.args.get('last_name'), request.args.get('email'))
    return c.as_dict()