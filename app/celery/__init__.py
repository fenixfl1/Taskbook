from __future__ import absolute_import
from . import config, celery
from .celery import app as celery_app
from .tasks import send_mail

__all__ = [
    'celery_app',
    'send_mail'
]