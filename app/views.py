from flask import render_template, request
from flask.ext.user import login_required
from app import app
from app import babel

from app.db import db, Room


@babel.localeselector
def get_locale():
    print("hallo")
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
