import os

MAIL_DEFAULT_SENDER = os.getenv('MAIL_USER')
SECURITY_EMAIL_SENDER = os.getenv('MAIL_USER')

ENV = os.getenv('FLASK_ENV')

TESTING = False
DEBUG = False
