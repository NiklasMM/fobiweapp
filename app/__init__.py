from flask import Flask
from flask.ext.babel import Babel
from flask.ext.mail import Mail
import app.secret_config as mailconfig


class ConfigClass(object):
    # Configure Flask
    SECRET_KEY = 'THIS IS AN INSECURE SECRET'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///fobiwe.sqlite'
    CSRF_ENABLED = True
    USER_ENABLE_USERNAME = False
    USER_ENABLE_CHANGE_USERNAME = False
    USER_ENABLE_EMAIL = True
    DEFAULT_LOCALE = "de"
    # Configure Flask-User
    USER_ENABLE_CONFIRM_EMAIL = True
    USER_ENABLE_CHANGE_PASSWORD = True
    USER_ENABLE_FORGOT_PASSWORD = True
    USER_ENABLE_RETYPE_PASSWORD = True

    # Configure Flask-Mail --
    # Required for Confirm email and Forgot password features
    MAIL_SERVER = mailconfig.MAIL_SERVER
    MAIL_PORT = 465
    MAIL_USE_SSL = True  # Some servers use MAIL_USE_TLS=True instead
    MAIL_USERNAME = mailconfig.MAIL_ADDRESS
    MAIL_PASSWORD = mailconfig.MAIL_PASSWORD
    MAIL_DEFAULT_SENDER = mailconfig.MAIL_ADDRESS

app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')
babel = Babel(app)      # Initialize Flask-Babel
mail = Mail(app)

from app import views  # noqa
