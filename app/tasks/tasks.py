from app.extentions import mail, celery
from app.database import db
from flask_mail import Message
from flask import render_template
from datetime import datetime


def send_mail(subject, recipients, text_body, html_body):

    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


@celery.task()
def pending_tasks(user):

    send_mail(
        'Tarea pendiente',
        user,
        render_template(
            'email/pending_tasks.txt',
            current_user=user
        ),
        render_template(
            'email/pending_tasks.html',
            current_user=user
        )
    )


@celery.task()
def next_subject(user):

    body_html = f"""
        <h2>Hi {user}</h2>
        <p>that's a test</p>
    """
    body_txt = f"Hola {user}, esto es una prueva"

    send_mail(
        'Proxima clase',
        user,
        body_txt,
        body_html
    )


@celery.task()
def test(name):

    saludo = f"Hola {name} esta es una prueva"

    return saludo
