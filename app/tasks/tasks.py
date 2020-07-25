from app.extentions import mail, celery
from app.database import db
from app.database.models import Notify
from flask_mail import Message
from flask import render_template


def send_mail(subject, recipients, text_body, html_body):

    msg = Message(subject, recipients)
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

    body_html = """
        <h2>Hi {}</h2>
        <p>that's a test</p>
    """.format(user)

    body_txt = "Hola {}, esto es una prueva".format(user)

    send_mail(
        'Proxima clase',
        user,
        body_txt,
        body_html
    )


@celery.task()
def notifications(title, msg, notify_date, user_id):

    try:
        notify = Notify(
            user_id=user_id,
            title=title,
            msg=msg,
            notify_time=notify_date
        )

        db.add(notify)
        db.commit()

        return {'User ID': user_id, 'Msg': msg}

    except ValueError as e:
        raise e
        return 'Error!'
