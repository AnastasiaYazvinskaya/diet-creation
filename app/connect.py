import sqlite3
from flask import render_template, request, url_for, flash, redirect, jsonify
from werkzeug.exceptions import BadRequest, InternalServerError, abort

# Get connection to db
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_users_db_connection():
    conn = sqlite3.connect('usersdb.db')
    conn.row_factory = sqlite3.Row
    return conn

from app import app, mail
from flask_mail import Message
from flask_login import current_user

def send_db():
    pass

def send_user_db():
    msg = Message('User-DB', sender = 'adyazvinskaya@gmail.com', recipients = ['diet.creation@gmail.com'])
    msg.body = 'New user'
    with app.open_resource("userdb.db") as fp:
        msg.attach("userdb.db", "db", fp.read())
    mail.send(msg)
    print('Mail sended')