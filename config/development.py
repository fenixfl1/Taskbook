import os
from .default import *

USE_NGROK = os.getenv('USE_NGROK')

# celery config
CELERY_BROKER_URL = os.getenv('REDIS')
CELERY_BACKEND_URL = 'db+cymysql://root:Adminfl119?@localhost:3306/Taskbook'

CELERY_CREATE_MISSING_QUEUES = True

SECURITY_EMAIL_SENDER = os.getenv('MAIL_USER')

<<<<<<< HEAD
ERROR_404_HELP = False

ENV = os.getenv('FLASK_ENV')

TESTING = True
DEBUG = True
=======
ENV = os.getenv('FLASK_ENV')
>>>>>>> 8a3ff0439701a9d79847b1879434a12d9f2ec8fb
