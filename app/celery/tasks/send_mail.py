from __future__ import absolute_import, unicode_literals
from celery.celery import app
from app import mail


@app.task(name='send_mails.task')
def send_mail(text):

    return text


result = send_mail.delay('Hola mundo!')
result.wait()