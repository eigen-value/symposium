import os
from symposium import basedir

# Default RRWebApp parameters
# DO NOT MODIFY THIS FILE
# You can overwrite params in your own ./RRWebApp/instance/config.py file

# CONFERENCE NAME
CONFERENCE_NAME = "Symposium"

# DO NOT USE DEBUG MODE IN PRODUCTION
DEBUG = True

# TESTING APP (EG FOR RECAPTCHA TO WORK)
TESTING = True

# SESSION
SESSION_TIMEOUT = 300

# SQL_Alchemy DB settings
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'db', 'symposium.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# email
MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
ADMINS = ['support@symposium.com']
EMAIL_SENDER_TEXT = "[Symposium:app]"

# recaptcha
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''