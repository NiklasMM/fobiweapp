from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import UserManager, UserMixin, SQLAlchemyAdapter
from flask.ext.babel import Babel
from flask.ext.user.forms import RegisterForm
from wtforms import validators
from wtforms import StringField, SelectField

from app import app
# Initialize Flask extensions
babel = Babel(app)                              # Initialize Flask-Babel
db = SQLAlchemy(app)                            # Initialize Flask-SQLAlchemy

QUALIFICATIONS = [
    "RH",
    "RS",
    "RA"
]


class MyRegisterForm(RegisterForm):
    first_name = StringField(
        'First name',
        validators=[validators.Required('First name is required')]
    )
    last_name = StringField(
        'Last name',
        validators=[validators.Required('Last name is required')]
    )
    qualification = SelectField(
        'RD-Qualifikation',
        choices=[
            ('RH', 'Rettungshelfer'),
            ('RS', 'Rettungssanitäter'),
            ('RA', 'Rettungsassistent')
        ]
    )


def setup_db():
    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app, register_form=MyRegisterForm)

    db.create_all()


# Define User model. Make sure to add flask.ext.user UserMixin!!
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))
    qualification = db.Column(db.Enum(*QUALIFICATIONS), nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    users = db.relationship("User", backref="room")
