from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from fernet import Secret
from flask_restful import Api
from logger import Logger
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)
#print(app.config)
#print(app.config['SQLALCHEMY_DATABASE_URI'])


api = Api(app)


CORS(app, resources={r"/API/*": {"origins": "*"}})


db = SQLAlchemy(app)
migrate = Migrate(app, db)


login = LoginManager(app)


secret = Secret(app)


logger = Logger(app)


from app import routes, models, workers, endpoints

logger.upd_log('App started', type=9, user='SYSTEM')