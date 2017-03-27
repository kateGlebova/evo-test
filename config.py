import os

base_dir = os.path.abspath(os.path.dirname(__file__) )

DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'hr.db')
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SECRET_KEY = 'kjghs8xhtkqi4*yr87+rv@7#+y4njwrd4+9v)a*+ztduw#9q^s&jv+zgaeg'