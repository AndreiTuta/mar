from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.exc import IntegrityError
import uuid
import datetime

db = SQLAlchemy()


class ModelClass():
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def add(self):
        try:
            print(f"Adding {self}")
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            print(f"Error processing new add")
            raise ValueError(e)


class Customer(db.Model, ModelClass, UserMixin):
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    guid = db.Column(db.String, nullable=False)
    # populated when fetched
    bookings = []

    def __init__(self, name, last_name, email):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.guid = str(uuid.uuid4())

    def as_dict(self):
        dicti = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dicti["bookings"] = self.bookings
        return dicti

    def update(self, name, last_name, email, plate):
        if name != '':
            print(f"Updating {self.id} name {self.name} to {name}")
            self.name = name
        if last_name != '':
            print(
                f"Updating {self.id} last_name {self.last_name} to {last_name}")
            self.last_name = last_name
        if email != '':
            print(f"Updating {self.id} email {self.email} to {email}")
            self.email = email
        db.session.flush()
        db.session.commit()
        
    def get_id(self):
        try:
            return self.id
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`")

    def __repr__(self):
        return "User(%s , %s)" % (self.uname, self.email)



class Booking(db.Model, ModelClass):
    __tablename__ = "booking"

    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, customer: int, date: str):
        self.customer = customer
        format = "%Y-%m-%dT%H:%M:%S.000Z"
        dt_object = datetime.datetime.strptime(date, format)
        self.date = dt_object
