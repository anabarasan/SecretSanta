import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\n2\xcfs;o\x1e\x12\x06\x99\xec,m7\xae_'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEAMS_WEBHOOK = ('https://outlook.office.com/webhook/'
                     '6aad4618-18e0-4bea-9efd-b9817f162da0@75c696ec'
                     '-5bfb-4892-9a0c-9187a9061cd6/'
                     'IncomingWebhook/1dcdbecca74140ecaa0e695d4bb69377/'
                     'd38ceb21-608c-4aa4-9567-53e6807813d2')
    WEBHOOK_MESSAGE = '''{}

with love,

Mom'''