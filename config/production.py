import os
from .default import *

SECURITY_EMAIL_SENDER = os.getenv('MAIL_USER')

ENV = os.getenv('APP_ENV')

TESTING = False
DEBUG = False
