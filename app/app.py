from flask import Flask
from flask_fontawesome import FontAwesome
from .flask_celery.celery_utils import init_celery
from app.jinja_filters import Filter
from werkzeug.middleware.proxy_fix import ProxyFix
from app.auth.security_form import ExtendRegisterForm
from app.admin.admin import MyAdminIndexView
from .extentions import *


# factory app
def create_app(setting_module, **kwargs):

    # application settings
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(setting_module)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    if kwargs.get('celery'):
        init_celery(kwargs.get('celery'), app)

    if app.config.get('TESTING', True):
        print(" * Running in development mode")
        app.config.from_envvar('APP_DEVELOPMENT_SETTINGS', silent=False)
    else:
        print(" * Running in production mode")
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
    ma.init_app(app)
    migrate.init_app(app, sql)
    adm.init_app(app, index_view=MyAdminIndexView())
    login.init_app(app)
    security.init_app(app, user_datastore,
                      register_form=ExtendRegisterForm,
                      confirm_register_form=ExtendRegisterForm)

    # register blueprints
    from .user import user_view
    app.register_blueprint(user_view)

    from .auth import auth_view
    app.register_blueprint(auth_view)

    from .admin import admin_view
    app.register_blueprint(admin_view)

    from .tasks import tasks
    app.register_blueprint(tasks)

    # Register error handler
    from .user.errors import error_500_handler
    app.register_error_handler(500, error_500_handler)

    from .user.errors import error_403_handler
    app.register_error_handler(403, error_403_handler)

    from .user.errors import error_404_handler
    app.register_error_handler(404, error_404_handler)

    # Register context requests
    from .user.requests import before_request_func
    app.before_request(before_request_func)

    from .user.requests import after_request_func
    app.after_request(after_request_func)

    from .user.requests import teardown_request_func
    app.teardown_request(teardown_request_func)

    from .user.requests import fisrt_request_func
    app.before_first_request(fisrt_request_func)

    return app
