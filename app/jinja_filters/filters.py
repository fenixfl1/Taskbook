from app.database.queries import Queries
from flask_security import current_user
from app.database.models import Tasks, Courses, Teachers, StudyPlan
from app.database import db
from flask import Blueprint

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

    filtro = Queries.contador(StudyPlan, current_user, n)

    return filtro

class Filter(object):

    def __init__(self, app):

        blueprint = Blueprint('filter', __name__)

        app.jinja_env.filters['tasks'] = tasks
        app.jinja_env.filters['courses'] = courses
        app.jinja_env.filters['teacher'] = teachers
        app.jinja_env.filters['plan'] = study_plan
        app.register_blueprint(blueprint)
