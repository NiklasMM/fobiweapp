from flask import render_template, request, redirect
from flask.ext.user import login_required, roles_required, current_user
from app import app
from app import babel
from app.db import User
from app.secret_config import ADMIN_EMAIL
from app.db import db, Room
from flask.ext.wtf import Form
from wtforms import BooleanField, TextAreaField


@babel.localeselector
def get_locale():
    translations = [
        str(translation) for translation in babel.list_translations()
    ]
    return request.accept_languages.best_match(translations)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
@login_required
def login():
    return render_template("index.html")


@app.route("/rooms")
#@login_required
def rooms():
    s = db.session
    rooms = s.query(Room).all()
    print(rooms)
    return render_template("rooms.html", rooms=rooms)


@app.route("/user_list")
@roles_required("admin")
def user_list():
    userlist = User.query.filter(User.email != ADMIN_EMAIL).all()
    return render_template("user_list.html", users=userlist)


class ProfileForm(Form):
    vegetarian = BooleanField('vegetarian', default=False)
    friday = BooleanField('Freitag', default=True)
    saturday = BooleanField('Samstag', default=True)
    sunday = BooleanField('Sonntag', default=True)
    own_car = BooleanField("own_car", default=False)
    comment = TextAreaField("text")


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == "GET":
        form = ProfileForm()
        form.friday.data = current_user.friday
        form.sunday.data = current_user.sunday
        form.saturday.data = current_user.saturday
        form.own_car.data = current_user.own_car
        form.vegetarian.data = current_user.vegetarian
        form.comment.data = current_user.comment
        if "success" in request.args:
            success = True
        else:
            success = False

        return render_template("profile.html", form=form, success=success)
    if request.method == "POST":
        current_user.vegetarian = "vegetarian" in request.form
        current_user.friday = "friday" in request.form
        current_user.saturday = "saturday" in request.form
        current_user.sunday = "sunday" in request.form
        current_user.own_car = "own_car" in request.form
        current_user.comment = request.form["comment"]
        db.session.add(current_user)
        db.session.commit()
        print(current_user.vegetarian)
        return redirect("{0}?success=t".format(request.path))
