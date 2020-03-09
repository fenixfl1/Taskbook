from flask import Blueprint


admin_view = Blueprint('adm', __name__,
                       template_folder='templates')

from . import admin
