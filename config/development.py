import os
from .default import *


# celery config
CELERY_RESULT_BACKEND = os.getenv('BACKEND')
CELERY_BROKER_URL = os.getenv('REDIS')


MAIL_DEFAULT_SENDER = os.getenv('MAIL_USER')
SECURITY_EMAIL_SENDER = os.getenv('MAIL_USER')

MAIL_SENDER = MAIL_DEFAULT_SENDER

ENV = os.getenv('FLASK_ENV')

SERVER_NAME = DEVELOPMENT_DOMAIN

TESTING = True
