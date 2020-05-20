from app.database.queries import Queries
from flask_security import current_user
from app.database.models import Tasks, Courses, Teachers, StudyPlan

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

            filtro = Queries.contador(Tasks, current_user, n)

            return filtro

        @app.template_filter('subjects')
        def materias(value, n=1):

            filtro = Queries.contador(Courses, current_user, n)

            return filtro

        @app.template_filter('teachers')
        def profesores(value, n=1):

            filtro = Queries.contador(Teachers, current_user, n)

            return filtro

        @app.template_filter('plan')
        def plan(value, n=1):

            filtro = Queries.contador(StudyPlan, current_user, n)

            return filtro
