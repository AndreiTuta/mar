from flask import Blueprint, request, render_template, redirect, url_for
frontend_blueprint = Blueprint("frontend", __name__)


@frontend_blueprint.route("/", methods=["GET"])
def index():
    return render_template('index.html')


@frontend_blueprint.route("calendar/", methods=["GET"])
@frontend_blueprint.route("calendar/<path:dummy>", methods=["GET"])
@frontend_blueprint.route("login/", methods=["GET"])
def page_not_found(dummy=None):
    return redirect(url_for("frontend.index"))


@frontend_blueprint.route("confirmation/", methods=["GET"])
def confirmation():
    return "Your booking was confirmed."
