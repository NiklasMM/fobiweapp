from flask import Flask
from flask.ext.babel import Babel


class ConfigClass(object):
    # Configure Flask
    SECRET_KEY = 'THIS IS AN INSECURE SECRET'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///minimal_app.sqlite'
    CSRF_ENABLED = True
    USER_ENABLE_EMAIL = False
    DEFAULT_LOCALE = "de"

app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')
babel = Babel(app)      # Initialize Flask-Babel

from app import views  # noqa
