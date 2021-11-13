import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):

    # ----------SECRETS & COOKIES
    SECRET_KEY = os.environ.get('SECRET_KEY') or '01!ChAnGeThIs!10'
    SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME') or '!Opt2021!'
    COOKIE_LIFESPAN = os.environ.get('SESSION_LIFESPAN') or 60 * 60 * 24 * 30
    ENV_FOLDER = basedir
    LOGIN_EXP_TIME = 3600

    # ----------STATICS & TEMPLATES
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # ----------LOGS
    LOG_FOLDER = os.path.join(basedir, 'log')

    # ----------DATABASE
    if os.environ.get('DB_TYPE') == 'sqlite':
        print('SELECTED DB: SQLite')
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    elif os.environ.get('DB_TYPE') == 'mariadb':
        print('SELECTED DB: MDB')
        print(os.environ.get('PRODUCTION'))

        if os.environ.get('PRODUCTION') and os.environ.get('PRODUCTION') == 'PROD':
            print("Production database in use!")
            SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')
            SQLALCHEMY_TRACK_MODIFICATIONS = False
        else:
            print("Development database in use!")
            SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')
            SQLALCHEMY_TRACK_MODIFICATIONS = False
