# Flask app configuration
from os import environ, path

from dotenv import load_dotenv

# create a basedir and pass it into the function if environment variable is not stored in the root directory
load_dotenv()
# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, ".venv"))

class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = "app.py"
    
    # API
    FIREBASE_API_KEY = environ.get('FIREBASE_API_KEY')
    
    # Flask-Mail
    DEBUG = True
    # TESTING = True
    MAIL_DEBUG = False
    MAIL_SERVER = 'smtp-relay.sendinblue.com'
    MAIL_PORT = 587
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'noreply@sendinblue.com'
    MAIL_MAX_EMAILS = None
    # MAIL_SUPPRESS_SEND = False
    MAIL_ASCII_ATTACHMENTS = False