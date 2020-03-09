from flask import Blueprint


auth_view = Blueprint('auth', __name__,
                      template_folder='templates')

from . import auth
