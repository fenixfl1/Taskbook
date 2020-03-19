from flask_script import Manager
from flask_migrate import MigrateCommand
from app.database import init_db
from wsgi import app
from app import migrate


manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    
    manager.run()
    init_db()