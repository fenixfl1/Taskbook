from app.database.queries import Queries
from flask_security import current_user
from app.database.models import Tasks, Courses, Teachers, StudyPlan
from app.database import db

"""
    In this class each function takes a boolean as parameter
    to indicate whether it is activated '1' or terminated '0'
    for example: {{ task | tasks(1) }} => list all the tasks to be delivere
"""


class NewFilter():

    @staticmethod
    def counters(app):

        @app.template_filter('tasks')
        def task(value, n=1):

            filtro = db.query(Tasks).\
                filter(Tasks.user_id == current_user.id).\
                filter(Tasks.state == 1).\
                filter(Tasks.done == n).count()

            return filtro

        @app.template_filter('subjects')
        def materias(value, n=1):

            filtro = db.query(Courses).\
                filter(Courses.user_id == current_user.id).\
                filter(Courses.finished == n).\
                filter(Courses.state == 1).count()

            return filtro

        @app.template_filter('teachers')
        def profesores(value, n=1):

            filtro = db.query(Teachers).\
                filter(Teachers.user_id == current_user.id).\
                filter(Teachers.state == 1).count()

            return filtro

        @app.template_filter('plan')
        def plan(value, n=1):

            filtro = Queries.contador(StudyPlan, current_user, n)

            return filtro
