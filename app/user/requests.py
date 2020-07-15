from . import user_view as app
from app.database import db


app.before_request
def before_request():

    return "response"


@app.after_request
def after_request_func(response):

    db.close()
    return response


@app.teardown_request
def teardown_request_func(exception=None):

    db.remove()
    return exception
