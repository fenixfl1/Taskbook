# from . import admin_view
from flask import redirect, url_for
from app import adm
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
# from flask_security.decorators import roles_required
from wtforms.validators import DataRequired
from app.database import db
from app.database.models import (User, Role, Eventos, Tarea,
                                 PlanEstudio, HorarioClases, Materias,
                                 Profesor, DetalleEvento, DetallePlan,
                                 DetalleTarea)

role_name = ['Admin', 'Editor', 'Coordinador']


class AdminView(ModelView):

    create_modal = True
    edit_modal = True
    can_delete = False
    can_view_details = True

    def is_accessible(self):

        for i in role_name:

            if i in current_user.roles:

                return True

            else:
                
                if current_user.is_authenticated:
                    
                    return redirect(url_for('index'))
                
                return False


class UserView(AdminView):

    column_exclude_list = ['password', 'gender', 'last_login_at',
                           'current_login_at', 'current_login_ip',
                           'login_count', 'confirmed_at']
    column_searchable_list = ('first_name', 'email', 'country')
    column_filters = ('first_name', 'email')
    can_export = True

    form_args = {
        'roles': {
            'label': 'Roles',
            'validators': [DataRequired()]
        }
    }


class UserRelatedView(AdminView):

    form_args = {
        'user': {
            'label': 'User',
            'validators': [DataRequired()]
        }
    }


class Details(AdminView):
    
    column_exclude_list = {
        'asignada_en',
        'creada_en', 'realizada_en'
    }

    form_choices = {
        'dia': [
            ('', ''),
            ('Sun', 'Sunday'),
            ('Mon', 'Monday'),
            ('Tus', 'Tuesday'),
            ('Wed', 'Wednesday'),
            ('Thu', 'Thursday.'),
            ('Fri', 'Friday'),
            ('Sat', 'Saturday')
        ]
    }


class DetalleEventView(Details):

    form_args = {
        'evento': {
            'label': 'Evento',
            'validators': [DataRequired()]
        }
    }


class DetalleTareaView(Details):

    form_args = {
        'tarea': {
            'label': 'Tarea',
            'validators': [DataRequired()]
        }
    }


class DetallePlanView(Details):

    form_args = {
        'plan': {
            'label': 'Plan de estudio',
            'validators': [DataRequired()]
        }
    }


class HorarioView(AdminView):

    form_args = {
        'materia': {
            'label': 'Materias',
            'validators': [DataRequired()]
        }
    }


adm.add_view(UserView(User, db, category='User'))
adm.add_view(AdminView(Role, db, category='User'))
adm.add_view(UserRelatedView(Eventos, db, category='Events'))
adm.add_view(DetalleEventView(DetalleEvento, db, category='Events'))
adm.add_view(UserRelatedView(Tarea, db, category='Task'))
adm.add_view(DetalleTareaView(DetalleTarea, db, category='Task'))
adm.add_view(UserRelatedView(PlanEstudio, db, category='Stady plan'))
adm.add_view(DetallePlanView(DetallePlan, db, category='Stady plan'))
adm.add_view(HorarioView(HorarioClases, db))
adm.add_view(AdminView(Materias, db))
adm.add_view(UserRelatedView(Profesor, db))