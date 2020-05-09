from app import mail, celery


@celery.task()
def send_mail():

    message = ''

    return message