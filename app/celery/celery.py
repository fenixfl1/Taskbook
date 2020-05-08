from __future__ import unicode_literals, absolute_import
from celery import Celery
import os

app = Celery('app')
app.config_from_object('celery.config')


if __name__ == "__main__":
    app.start()
