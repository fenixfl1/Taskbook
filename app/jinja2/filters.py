from jinja2 import Environment
from flask_security import current_user
from app.database.queries import Queries
from app.database.models import Profesor


def num_teachers():

    count = Queries.contador(Profesor, current_user, 1)

    return count


env = Environment()
env.filters['num_teachers'] = num_teachers
