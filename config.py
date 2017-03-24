import os

base_dir = os.path.abspath('./')

DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = base_dir + 'db/test.db'