from config.default import *
from app import mail
from flask_mail import Message
from flask import render_template, jsonify
from . import notify


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def notify_tasks(task, user):

    send_email('%s esta programada para ser entregada el dia de hoy'
               % task.name,
               MAIL_SENDER, user.email, render_template(
                   'notify/notify_task.txt',
                   _current_user=user,
                   _current_task=task
               ), render_template(
                   'notify/notify_task.html',
                   _current_user=user,
                   _current_task=task
               )
               )


@notify.route('/notications')
def notications():

    resp = jsonify(
        'success': 1,
        'result': "It's Ok!"
    )

    return resp
