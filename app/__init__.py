from flask import Flask
from config import Config

from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)

from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "login"

mail = Mail(app)

from app import views