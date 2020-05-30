import os
from os.path import abspath, dirname
from dotenv import load_dotenv

APP_ROOT = dirname(dirname(abspath(__file__)))
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


UPLOAD_FOLDER_DEST = os.getenv('UPLOAD')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE')


IMAGE_SET_EXT = ('jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp')


# configuracion de despligue de la aplicacion
DEBUG = False
TESTING = False
ENV = ''

# Security
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = 'sha512_crypt'

SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
SECURITY_CONFIRMABLE = True
SECURITY_CHANGEABLE = True

SECURITY_LOGIN_URL = '/'
SECURITY_POST_LOGIN_VIEW = '/index'
SECURITY_POST_REGISTER_VIEW = '/'
SECURITY_POST_CONFIRM_VIEW = '/'

FLASK_ADMIN_SWATCH = 'simplex'

SQLALCHEMY_TRACK_MODIFICATIONS = False
