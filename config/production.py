import os
from .default import *

SECURITY_EMAIL_SENDER = os.getenv('MAIL_USER')

TESTING = False
DEBUG = False

ENV = os.getenv('FLASK_ENV')
