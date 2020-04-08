from app import creatre_app
from app.database import init_db
import os

settings_module = os.getenv('APP_SETTINGS_MODULE')

if __name__ == '__main__':

    app = creatre_app(settings_module)

    with app.app_context():
        init_db()

    app.run()
