import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    LOG_DIR = os.path.join(basedir, 'logs')
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\n2\xcfs;o\x1e\x12\x06\x99\xec,m7\xae_'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEAMS_WEBHOOK = ''
    WEBHOOK_MESSAGE = '''{}

with love,

Mom'''