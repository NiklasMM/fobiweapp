from flask import render_template, request, redirect, url_for
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
    users = User.query.filter(User.email != ADMIN_EMAIL).all()
    print(rooms)
    return render_template("rooms.html", rooms=rooms, users=users)


@app.route("/rooms/<room_id>", methods=['GET', 'POST'])
def room_detail(room_id):
    room = Room.query.get_or_404(int(room_id))
    if request.method == "GET":
        users = User.query.filter(
            User.email != ADMIN_EMAIL
        ).all()
        room_users = User.query.filter(
            User.room == room, User.email != ADMIN_EMAIL
        ).all()

        assigned_users = [-1 for i in range(room.capacity)]
        for i, u in enumerate(room_users):
            assigned_users[i] = u.id

        return render_template(
            "room_detail.html", room=room, unassigned_users=users,
            assigned_users=assigned_users)
    if request.method == "POST":
        # first unassign all users
        old_users = User.query.filter(
            User.room == room, User.email != ADMIN_EMAIL
        ).all()
        for u in old_users:
            u.room = None
            db.session.add(u)
        for bed, user in request.form.items():
            if int(user) != -1:
                u = User.query.get(int(user))
                u.room = room
                db.session.add(u)
        db.session.commit()
        return redirect(url_for("room_detail", room_id=room_id))



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


@app.route("/rooms/manage", methods=['GET', 'POST'])
@roles_required("admin")
def room_list():
    if request.method == "GET":
        return render_template("room_list.html", rooms=Room.query.all())
    if request.method == "POST":
        try:
            new_room = Room()
            new_room.number = int(request.form["room-number"])
            new_room.capacity = int(request.form["room-capacity"])
            db.session.add(new_room)
            db.session.commit()
        except ValueError:
            pass
        return redirect(url_for("room_list"))

@app.route("/rooms/<room_id>/delete")
@roles_required("admin")
def delete_room(room_id):
    room = Room.query.get_or_404(int(room_id))
    db.session.delete(room)
    db.session.commit()
    return redirect(url_for("room_list"))
