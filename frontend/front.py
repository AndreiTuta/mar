from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required

from frontend.forms import LoginForm
from api.models import Customer
from api.handler import *
frontend_blueprint = Blueprint("frontend", __name__)

@frontend_blueprint.route('/')
def homepage():
    return render_template("home.html" , )

@frontend_blueprint.route("/login", methods=["GET", "POST"])
def loginpage():
    if current_user.is_authenticated:
        flash("You are already logged in.", "warning")
        return redirect(url_for("frontend.homepage"))
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        member = Customer.query.filter_by(email=form.uname.data).first()
        if member and member.guid == form.password.data:
            login_user(member)
            flash("Welcome, %s!" % (form.uname.data), "success")
            return redirect(url_for("frontend.homepage"))
        else:
            flash("Username or Password doesn't match, please try again.", "danger")
            return redirect(url_for("frontend.loginpage"))
    return render_template("login.html", form=form)


@frontend_blueprint.route('/calendar')
def calendarpage():
    if current_user.is_authenticated:
        return render_template("calendar.html" , user_id=current_user.get_id())
    else:
       return redirect(url_for("frontend.loginpage"))

@frontend_blueprint.route('/confirmation')
def confirmationpage():    
    return render_template("confirmation.html")

@frontend_blueprint.route('/gallery')
def gallerypage():
    albums = get_albums()
    return render_template("gallery.html", albums = albums)

@frontend_blueprint.route('/gallery/albums/<album_id>')
def gallery_album_page(album_id:int):
    album = get_album(album_id)
    return render_template("album.html", album = album)

@frontend_blueprint.route("/logout")
def logoutpage():
    logout_user()
    flash("Successfuly logged out.", "success")
    return redirect(url_for("frontend.homepage"))
