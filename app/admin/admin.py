from flask import redirect, url_for
from app.extentions import adm
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import rediscli
from flask_login import current_user
from flask_admin import AdminIndexView, expose
from flask_security import login_required, roles_required
from app.database import db
from redis import Redis
from wtforms.validators import DataRequired
from app.database.models import (User, Role, Events, Tasks,
                                 StudyPlan, ClassSchedule, Courses,
                                 Teachers, StudyPlanGoals, Notify)

role_name = ['Admin', 'admin', 'administrador']


# my own index view in admin panel
class MyAdminIndexView(AdminIndexView):
    @expose()
    @login_required
    @roles_required('Admin')
    def index(self):

        return self.render(
            'admin/index.html',
            name='Taskbook'
        )


class AdminView(ModelView):

    create_modal = True
    edit_modal = True
    # can_delete = False
    can_view_details = True

    def is_accessible(self):

        for i in role_name:

            if i in current_user.roles:

                return True

            else:
                return False

    def inaccessible_callback(self, name, **kwargs):

        return redirect(url_for('users.index'))


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
        'creada_en',
        'realizada_en'
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


class StudyPlanGoalsView(Details):

    form_args = {
        'plan': {
            'label': 'Plan de estudio',
            'validators': [DataRequired()]
        }
    }


class HorarioView(AdminView):

    form_args = {
        'materia': {
            'label': 'Courses',
            'validators': [DataRequired()]
        }
    }


adm.add_view(rediscli.RedisCli(Redis()))
adm.add_view(UserView(User, db, category='User'))
adm.add_view(AdminView(Role, db, category='User'))
adm.add_view(UserRelatedView(Events, db))
adm.add_view(UserRelatedView(Tasks, db))
adm.add_view(UserRelatedView(StudyPlan, db, category='Stady plan'))
adm.add_view(StudyPlanGoalsView(StudyPlanGoals, db, category='Stady plan'))
adm.add_view(HorarioView(ClassSchedule, db))
adm.add_view(AdminView(Courses, db))
adm.add_view(UserRelatedView(Teachers, db))
adm.add_view(UserRelatedView(Notify, db))
