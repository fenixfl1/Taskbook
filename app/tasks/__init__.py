from .tasks import pending_tasks, next_subject,\
    test
from flask import Blueprint


tasks = Blueprint(
    'task',
    __name__,
    static_folder='static',
    template_folder='templates'
)
