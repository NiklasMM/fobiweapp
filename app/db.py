from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import UserManager, UserMixin, SQLAlchemyAdapter
from flask.ext.babel import Babel
from flask.ext.user.forms import RegisterForm
from wtforms import validators, ValidationError
from wtforms import StringField, SelectField
from app import secret_config

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
    gender = SelectField(
        "Geschlecht",
        choices=[
            ("f", "weiblich"),
            ("m", "männlich")
        ]
    )

def my_password_validator(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError('Das Passwort muss mindestens 8 Zeichen lang sein!')

def setup_db():
    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app, register_form=MyRegisterForm, password_validator=my_password_validator)

    db.create_all()

    # Create 'user007' user with 'secret' and 'agent' roles
    if not User.query.filter(User.email == secret_config.ADMIN_EMAIL).first():
        user1 = User(
            email=secret_config.ADMIN_EMAIL, active=True,
            password=user_manager.hash_password(secret_config.ADMIN_PW),
            qualification="RH", first_name="Admin", last_name="Admin",
            gender="m")
        user1.roles.append(Role(name='admin'))
        db.session.add(user1)
        db.session.commit()

# Define the User-Roles pivot table
user_roles = db.Table(
    'user_roles',
    db.Column('id', db.Integer(), primary_key=True),
    db.Column('user_id', db.Integer(), db.ForeignKey(
        'user.id', ondelete='CASCADE')
    ),
    db.Column('role_id', db.Integer(), db.ForeignKey(
        'role.id', ondelete='CASCADE'))
)


# Define Role model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define User model. Make sure to add flask.ext.user UserMixin!!
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))
    qualification = db.Column(db.Enum(*QUALIFICATIONS), nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    confirmed_at = db.Column(db.DateTime())
    gender = db.Column(db.Enum("m", "f"), nullable=False)
    reset_password_token = db.Column(
        db.String(100), nullable=False, default=''
    )
    # Relationships
    roles = db.relationship(
        'Role', secondary=user_roles,
        backref=db.backref('users', lazy='dynamic')
    )

    # additional info given in profile
    vegetarian = db.Column(db.Boolean, default=False)
    friday = db.Column(db.Boolean, default=True)
    saturday = db.Column(db.Boolean, default=True)
    sunday = db.Column(db.Boolean, default=True)
    own_car = db.Column(db.Boolean, default=False)

    comment = db.Column(db.Text)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    users = db.relationship("User", backref="room")
