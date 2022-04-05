import sqlite3
from werkzeug.security import generate_password_hash

connection = sqlite3.connect('usersdb.db')

with open('app/usersSchema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
# Insert user's icons
for i in range(1, 23):
    connection.execute('''INSERT INTO user_icons (icon) VALUES
                        (?)''',
                        ("../static/images/user-"+str(i)+".svg",))
# Inser 3 admins
connection.execute('INSERT INTO users (role, username, email, password) VALUES (?,?,?,?), (?,?,?,?), (?,?,?,?)',
                  ("admin", "adminValya", "diet.creation@gmail.com", generate_password_hash("admin2022Valya3"),
                   "admin", "adminNik", "diet.creation@gmail.com", generate_password_hash("admin2022Nik2"),
                   "admin", "adminAnastas", "diet.creation@gmail.com", generate_password_hash("admin2022Anastas4")))
# Insert test user
connection.execute('INSERT INTO users (role, username, email, password) VALUES (?,?,?,?)',
                  ("user", "TestUser", "diet.creation.sendler@gmail.com", generate_password_hash("TestUserCreated001")))

connection.commit()
connection.close()