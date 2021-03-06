import os

basedir = os.path.abspath(os.path.dirname(__file__))

#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'diet.creation.sendler@gmail.com'
    MAIL_PASSWORD = 'lyqadopvxqcslakq'
    ADMINS = ['diet.creation@gmail.com']