import os
from .default import *

# celery config
CELERY_BROKER_URL = os.getenv('REDIS')
CELERY_BACKEND_URL = 'db+cymysql://root:Adminfl119?@localhost:3306/Taskbook'

CELERY_CREATE_MISSING_QUEUES = True


MAIL_DEFAULT_SENDER = os.getenv('MAIL_USER')
SECURITY_EMAIL_SENDER = os.getenv('MAIL_USER')

ENV = os.getenv('FLASK_ENV')

TESTING = True
DEBUG = True
