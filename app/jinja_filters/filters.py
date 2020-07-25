# from app.database.queries import Queries
from flask_security import current_user
from flask import Markup
from app.database.models import Tasks, Courses, Teachers, \
    StudyPlan, StudyPlanGoals
from app.database import db
from app.extentions import avatars, db_session
import hashlib


def tasks(value, **kwargs):

    filtro = db.query(Tasks).\
        filter(Tasks.user_id == current_user.id).\
        filter(Tasks.state == 1)

    progress = 0

    if 'done' in kwargs:

        if kwargs.get('done') == 1:
            return filtro.filter(Tasks.done == 1).count()

        if kwargs.get('done') == 0:
            return filtro.filter(Tasks.done == 0).count()

        else:
            return filtro.count()

    if 'progress' in kwargs:

        if kwargs.get('progress') == 1:
            total = filtro.filter(Tasks.course_id == value).count()
            done = filtro.filter(Tasks.done == 1).count()

            try:
                progress = (done * 100) / total
            except ZeroDivisionError as e:
                raise e
            finally:
                return progress


def courses(value, **kwargs):

    filtro = db.query(Courses).\
        filter(Courses.user_id == current_user.id).\
        filter(Courses.state == 1)

    progress = 0

    if 'finished' in kwargs:

        if kwargs.get('finished') == 0:
            return filtro.filter(Courses.finished == 0).count()

        if kwargs.get('finished') == 1:
            return filtro.filter(Courses.finished == 1).count()

        else:
            return filtro.count()

    if 'progress' in kwargs:

        if kwargs.get('progress') == 1:
            total = filtro.count()
            finished = filtro.filter(Courses.finished == 1).count()

            try:
                progress = (finished * 100) / total
            except ZeroDivisionError as e:
                raise e
            finally:
                return progress
        else:
            return None


def teachers(value, n=1):

    filtro = db.query(Teachers).\
        filter(Teachers.user_id == current_user.id).\
        filter(Teachers.state == n).count()

    return filtro


def study_plan(value, n=1):

    filtro = db.query(StudyPlan).\
        filter(StudyPlan.user_id == current_user.id).\
        filter(StudyPlan.state == n).count()

    return filtro


def study_plan_goals_done(id):

    filter = db.query(StudyPlanGoals).\
        join(StudyPlan, StudyPlanGoals.plan_id == StudyPlan.id).\
        filter(StudyPlanGoals.done == 1).\
        filter(StudyPlanGoals.state == 1).\
        filter(StudyPlan.id == id).\
        filter(StudyPlan.state == 1).\
        filter(StudyPlan.user_id == current_user.id).count()

    return filter


def study_plan_goals(id):

    filter = db.query(StudyPlanGoals).\
        join(StudyPlan, StudyPlanGoals.plan_id == StudyPlan.id).\
        filter(StudyPlanGoals.state == 1).\
        filter(StudyPlan.id == id).\
        filter(StudyPlan.state == 1).\
        filter(StudyPlan.user_id == current_user.id).count()

    return filter


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
        app.jinja_env.filters['study_plan_goals_done'] = study_plan_goals_done
        app.jinja_env.filters['study_plan_goals'] = study_plan_goals
