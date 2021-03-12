import os
from secret_configs import SHEETS_URL
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT=False
    PORT = 9805
    HOST = '0.0.0.0'
    ENABLE_SHEETS_UPDATE = True
    SHEETS_BACKEND = os.environ.get('SHEETS_URL') or SHEETS_URL