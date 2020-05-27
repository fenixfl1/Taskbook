from app import creatre_app
from app.database import init_db
from app.extentions import celery, socket
import os

settings_module = os.getenv('APP_SETTINGS_MODULE')

app = creatre_app(settings_module, celery=celery)

with app.app_context():
    init_db()


if __name__ == '__main__':
    socket.run(app)
