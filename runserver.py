#!/usr/bin/python3

from app import create_app, celery
from app.database import init_db
import app as module
import os

settings_module = os.getenv('APP_SETTINGS_MODULE')

app = create_app(settings_module, celery=celery)

print(" * Author: {}".format(module.__author__))
print(" * Version: {}".format(module.__version__))
print(" * Date: {}".format(module.__date__))

with app.app_context():
    init_db()


if __name__ == '__main__':
    app.run()
