from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from flask_security import Security
from flask_wtf import CSRFProtect
from flask_avatars import Avatars
from flask_mail import Mail
from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate
from .flask_celery import make_celery


sql = SQLAlchemy()
cors = CORS()
bootstrap = Bootstrap()
mail = Mail()
security = Security()
csrf = CSRFProtect()
avatars = Avatars()
adm = Admin(name='Taskbook', template_mode='bootstrap3')
login = LoginManager()
migrate = Migrate()
celery = make_celery()
db_session = sql.session


__all__ = [
    'sql',
    'cors',
    'bootstrap',
    'security',
    'csrf',
    'avatars',
    'mail',
    'adm',
    'login',
    'migrate',
    'celery',
]
