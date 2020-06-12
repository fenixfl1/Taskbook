from celery import Celery

def make_celery(app_name=__name__):

    return Celery(
        app_name,
        backend='redis://',
        broker='redis://localhost:6379/0'
    )
