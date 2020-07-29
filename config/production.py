import os
from .default import *

SECURITY_EMAIL_SENDER = os.getenv('MAIL_USER')

<<<<<<< HEAD
ENV = os.getenv('APP_ENV')

TESTING = False
DEBUG = False
=======
ENV = os.getenv('FLASK_ENV')
>>>>>>> 8a3ff0439701a9d79847b1879434a12d9f2ec8fb
