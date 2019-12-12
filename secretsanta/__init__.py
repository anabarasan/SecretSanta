import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from secretsanta.config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

login.login_view = 'login'

log_dir = app.config['LOG_DIR']
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

file_handler = RotatingFileHandler(log_dir + '/secretsanta.log', maxBytes=10240, backupCount=20)
file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)

from secretsanta import routes, models

app.logger.info('secret santa startup complete')