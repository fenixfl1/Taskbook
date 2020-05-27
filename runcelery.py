from app.flask_celery.celery_utils import init_celery
from runserver import app
from app.extentions import celery


init_celery(celery, app)
