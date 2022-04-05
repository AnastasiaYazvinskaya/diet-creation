from flask import Flask
from flask_jsglue import JSGlue
from config import Config
from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail

app = Flask(__name__)
jsglue = JSGlue(app)
app.config.from_object(Config)
db = SQLAlchemy(app)

from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "login"

mail = Mail(app)

from app import views