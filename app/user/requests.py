from app.database import db
from app.database.models import Role, User
from app.extentions import user_datastore
from datetime import datetime


def fisrt_request_func():

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

        print(" * User admin has created!")


def before_request_func():

    pass

def after_request_func(response):

    db.close()
    return response


def teardown_request_func(exception=None):

    db.remove()
    return exception
