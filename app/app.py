from flask import Flask
from flask_fontawesome import FontAwesome
from flask_security import SQLAlchemySessionUserDatastore
from .flask_celery.celery_utils import init_celery
from app.jinja_filters import Filter
from app.database.models import User, Role
from werkzeug.middleware.proxy_fix import ProxyFix
from app.database import db
from app.extra import register_error_handlers, MyAdminIndexView, all_request
from app.auth.security_form import ExtendRegisterForm
from .extentions import *
import os

name = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

user_datastore = SQLAlchemySessionUserDatastore(db, User, Role)


def create_app(setting_module, app_name=name, **kwargs):

    # application settings
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(setting_module)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    celery = kwargs.get('celery')

    if celery:
        init_celery(celery, app)

    if app.config.get('TESTING', True):
        app.config.from_envvar('APP_DEVELOPMENT_SETTINGS', silent=False)
    else:
        app.config.from_envvar('APP_PRODUCTION_SETTINGS', silent=False)

    # library integrations
    Filter(app)
    csrf.init_app(app)
    bootstrap.init_app(app)
    FontAwesome(app)
    cors.init_app(app)
    avatars.init_app(app)
    mail.init_app(app)
    sql.init_app(app)
    migrate.init_app(app, sql)
    adm.init_app(app, index_view=MyAdminIndexView())
    login.init_app(app)
    security.init_app(app, user_datastore,
                      register_form=ExtendRegisterForm,
                      confirm_register_form=ExtendRegisterForm)

    # register blueprint
    from .user import user_view
    app.register_blueprint(user_view)

    from .auth import auth_view
    app.register_blueprint(auth_view)

    from .admin import admin_view
    app.register_blueprint(admin_view)

    from .tasks import tasks
    app.register_blueprint(tasks)

    # my extentions
    register_error_handlers(app)
    all_request._(app, db)

    return app
