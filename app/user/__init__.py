from flask import Blueprint

user_view = Blueprint('users', __name__,
                      template_folder='templates')


from . import routes, requests, errors