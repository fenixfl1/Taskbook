from flask import render_template
from flask_admin import AdminIndexView, expose
from flask_security import login_required, roles_required
from datetime import datetime
from app.database.models import User, RolesUsers, Role


class all_request(object):

    @staticmethod
    def _(app, session):
        """
        _(app, session) for execute before, after and teardown requests
        """

        @app.before_request
        def first_request_func():

            pass

        @app.after_request
        def after_request_func(response):

            session.close()
            return response

        @app.teardown_request
        def teardown_request_func(exception=None):

            session.remove()
            return exception


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


# funtion for create new user
def create_user(app, user_datastore, db, role):

    @app.before_first_request
    def new_user():

        user = db.query(User.email).all()

        role = db.query(Role).all()

        if len(role) == 0:
            rol = Role(
                name="Admin",
                description="Control total de la applicacion"
            )

            db.add(rol)
            db.commit()

        if len(user) == 0:

            user_datastore.create_user(email='benjaminfl119@gmail.com',
                                       first_name='Benjamin',
                                       last_name='Rosario',
                                       password='adminfl119',
                                       phone_number='(829) 359 4707',
                                       country='DO',
                                       gender='M',
                                       confirmed_at=datetime.now(),
                                       roles=['Admin'])
            db.commit()


# Errors views
def register_error_handlers(app):

    @ app.errorhandler(500)
    def base_error_handler(e):

        return render_template(
            'errors/500.html',
            title=e.name,
            e=e.description
        ), 500

    @ app.errorhandler(404)
    def error_404_handler(e):

        return render_template(
            'errors/404.html',
            title=e.name,
            e=e.description
        ), 404

    @ app.errorhandler(403)
    def error_403_handler(e):

        head = e.name
        body = e.description

        return render_template(
            'errors/403.html',
            title=head,
            e=body
        ), 403
