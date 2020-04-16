from flask import Blueprint
from flask_cors import CORS


auth_view = Blueprint('auth', __name__,
                      template_folder='templates')
CORS(auth_view)

from . import auth
