from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, instance_relative_config=True, static_folder="./static")
app.config.from_object('config')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

from . import views
from . import error_handlers