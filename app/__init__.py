from flask import Flask
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView, expose
from flask_login import LoginManager, login_required
from flask_cors import CORS
from flask_security import Security, SQLAlchemySessionUserDatastore, roles_required
from app.database import init_db
from app.database.models import User, Role
from werkzeug.middleware.proxy_fix import ProxyFix
from app.database import db
from app.extra import register_error_handlers, MyAdminIndexView, create_user, all_request
from .extendforms import ExtendRegisterForm
from datetime import datetime


mail = Mail()
adm = Admin(name='Taskbook', template_mode='bootstrap3')
sql = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
security = Security()


user_datastore = SQLAlchemySessionUserDatastore(db, User, Role)

def creatre_app(setting_module):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(setting_module)

    app.wsgi_app = ProxyFix(app.wsgi_app)

    if app.config.get('TESTING', True):
        app.config.from_envvar('APP_DEVELOPMENT_SETTINGS', silent=False)
    else:
        app.config.from_envvar('APP_PRODUCTION_SETTINGS', silent=False)

    CSRFProtect(app)
    Bootstrap(app)
    Migrate(app, db)
    FontAwesome(app)
    CORS(app)
    mail.init_app(app)
    sql.init_app(app)
    migrate.init_app(app, sql)
    adm.init_app(app, index_view=MyAdminIndexView())
    login.init_app(app)
    security.init_app(app, user_datastore,
                      register_form=ExtendRegisterForm,
                      confirm_register_form=ExtendRegisterForm)

    from .user import user_view
    app.register_blueprint(user_view)

    from .auth import auth_view
    app.register_blueprint(auth_view)

    from .admin import admin_view
    app.register_blueprint(admin_view)
    
    from .notify import notify
    app.register_blueprint(notify)
    
    register_error_handlers(app)
    all_request._(app, db)
    # create_user(app, user_datastore, db, Role)

    return app
