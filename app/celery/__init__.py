from __future__ import absolute_import
from . import tasks, config, celery
from .celery import app as celery_app

__all__ = ['celery_app']