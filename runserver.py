from app import create_app, celery
from app.database import init_db
import os

settings_module = os.getenv('APP_SETTINGS_MODULE')

app = create_app(settings_module, celery=celery)

with app.app_context():
    init_db()
    
if __name__ == '__main__':
    app.run()
