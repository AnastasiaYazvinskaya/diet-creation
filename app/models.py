from app import app, login_manager
from flask_login import UserMixin, login_user, logout_user
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
     def __init__(self, id, username, email, password):
          self.id = id
          self.username = username
          self.email = email
          self.password = password
          self.authenticated = False
         
     def set_password(self, password):
          self.password_hash = generate_password_hash(password)

     def check_password(self, password):
          return check_password_hash(self.password_hash, password)

     def is_active(self):
          return self.is_active()
     def is_anonymous(self):
          return False
     def is_authenticated(self):
          return self.authenticated
     def is_active(self):
          return True
     def get_id(self):
          return self.id

@login_manager.user_loader
def load_user(user_id):
     conn = sqlite3.connect('usersdb.db')
     curs = conn.cursor()
     user = curs.execute("SELECT * FROM users WHERE id=?",(user_id,)).fetchone()
     if user is None:
          return None
     else:
          return User(int(user[0]), user[1], user[2], user[3])
