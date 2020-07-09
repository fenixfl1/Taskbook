# from app.database.queries import Queries
from flask_security import current_user
from flask import Markup
from app.database.models import Tasks, Courses, Teachers, StudyPlan
from app.database import db
from app.extentions import avatars, db_session
import hashlib

def tasks(value, n=1):

    filtro = db.query(Tasks).\
        filter(Tasks.user_id == current_user.id).\
        filter(Tasks.state == 1).\
        filter(Tasks.done == n).count()

    return filtro


def courses(value, n=1):

    filtro = db.query(Courses).\
        filter(Courses.user_id == current_user.id).\
        filter(Courses.finished == n).\
        filter(Courses.state == 1).count()

    return filtro


def teachers(value, n=1):

    filtro = db.query(Teachers).\
        filter(Teachers.user_id == current_user.id).\
        filter(Teachers.state == n).count()

    return filtro


def study_plan(value, n=1):

    filtro = db.query(StudyPlan).\
        filter(StudyPlan.user_id).\
        filter(StudyPlan.state == n).count()

    return filtro


def list_courses(value):
    return db.query(Courses).\
        filter(Courses.user_id == current_user.id).\
        filter(Courses.state == 1).\
        filter(Courses.finished == 0).all()


def paginate_courses(state, finished):

    filter = db_session.query(Courses).\
        filter(Courses.user_id == current_user.id).\
        filter(Courses.state == state).\
        filter(Courses.finished == finished).\
        paginate(1, 8, 0)

    return filter

def avatar(value, **kwargs):

    classes = ''
    size = '50'

    if kwargs['size']:
        size = kwargs['size']
    if kwargs['class']:
        classes = kwargs['class']

    email_hash = hashlib.md5(current_user.email.lower().
                             encode('utf-8')).hexdigest()

    url_avatar = avatars.gravatar(email_hash, size=size)

    return Markup(
        '<img src="{}" class="{}" title="{} {}">'.
        format(url_avatar, str(classes),
               current_user.first_name.capitalize(),
               current_user.last_name.capitalize())
    )


def generate_avatar(value, **kwargs):

    title = ''
    classes = ''
    size = '50'

    if 'title' in kwargs:
        title = kwargs.get('title')
    if 'size' in kwargs:
        size = kwargs['size']
    if 'class' in kwargs:
        classes = kwargs['class']

    email_hash = hashlib.md5(value.lower().encode('utf-8')).hexdigest()

    url_avatar = avatars.gravatar(email_hash, size=size)

    return Markup(
        '<img src="{}" class="{}" title="{}">'.
        format(url_avatar, str(classes), str(title))
    )

class Filter():

    def __init__(self, app):

        app.jinja_env.filters['tasks'] = tasks
        app.jinja_env.filters['courses'] = courses
        app.jinja_env.filters['teacher'] = teachers
        app.jinja_env.filters['plan'] = study_plan
        app.jinja_env.filters['list_courses'] = list_courses
        app.jinja_env.filters['default'] = avatar
        app.jinja_env.filters['generate_avatar'] = generate_avatar
        app.jinja_env.filters['paginate_courses'] = paginate_courses
