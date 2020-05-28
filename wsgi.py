from app import create_app as application
import os

settings_module = os.getenv('APP_SETTINGS_MODULE')

app = application(settings_module)
