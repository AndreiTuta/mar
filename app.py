from flask import Flask

from api.models import db, Customer
from api.customer import customer_blueprint
from api.booking import booking_blueprint
from api.album import album_blueprint
from api.image import image_blueprint
from frontend.front import frontend_blueprint

from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


import os

app = Flask(__name__, static_folder="./frontend/dist/static",
            template_folder="./frontend/dist")
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite://' + os.path.join('/data', 'data.db'
                                                                   )
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
cors = CORS(app)
app.secret_key = 'xxxxyyyyyzzzzz'
pwd = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "admin.loginpage"
login_manager.login_message = "You are mot authorised to access this page. Please login first."
login_manager.login_message_category = "danger"

app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(customer_blueprint, url_prefix="/customer")
app.register_blueprint(booking_blueprint, url_prefix="/booking")
app.register_blueprint(album_blueprint, url_prefix="/album")
app.register_blueprint(image_blueprint, url_prefix="/image")

app.register_blueprint(frontend_blueprint, url_prefix="/")


@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))

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
    app.run(debug=True, port=8080)
