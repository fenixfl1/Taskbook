import os
from .default import *


MAIL_DEFAULT_SENDER = os.getenv('MAIL_USER')
SECURITY_EMAIL_SENDER = os.getenv('MAIL_USER')

ENV = os.getenv('FLASK_ENV')
SERVER_NAME = DEVELOPMENT_DOMAIN

TESTING = True
