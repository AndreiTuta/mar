from flask import Flask
from customer import customer_blueprint
from booking import booking_blueprint

from flask_cors import CORS, cross_origin

from models import db

import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite://'+ os.path.join('/data', 'data.db'
    )
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(customer_blueprint, url_prefix="/customer")
app.register_blueprint(booking_blueprint, url_prefix="/booking")


# Error handling
@app.errorhandler(500)
@app.errorhandler(ValueError)
def internal_error(error):
    return f"Error {error}"


@app.errorhandler(404)
def page_not_found(e):
    return e

if __name__ == "__main__":
    # db init only after the app started
    db.init_app(app)
    app.run(debug = True, port = 8080)