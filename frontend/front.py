from flask import Blueprint, request, render_template

frontend_blueprint=Blueprint("frontend", __name__)

@frontend_blueprint.route("/", methods=["GET"])
def index():
    return render_template('index.html')
    