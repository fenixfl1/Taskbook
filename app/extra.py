from flask_admin import AdminIndexView, expose
from flask_security import login_required, roles_required
from datetime import datetime


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

        user_datastore.create_user(email='admin@taskbook.com',
                                   first_name='Benjamin',
                                   last_name='Rosario',
                                   password='adminfl119',
                                   phone_number='(829) 359 4707',
                                   country='DO',
                                   gender='M',
                                   confirmed_at=datetime.now())
        db.commit()
