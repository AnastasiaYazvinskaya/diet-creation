import sqlite3
from flask import flash, render_template, request, url_for
import app.recipes as r
import app.products as p
import app.menu as m
#import app.test as t
from app.forms import LoginForm, RegisterForm
import app.connect as c
from app import app, mail
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

# Imports for users
from flask_login import login_required, current_user, login_user, logout_user
from app.models import User

# Starting-welcome page (just open)
@app.route('/')
@app.route('/index')
def index():
    return c.render_template('index.html')

@app.route('/user_<int:user_id>')
@login_required
def user(user_id):
    data = {
        'products': 0,
        'recipes': 0,
        'menus': 0
    }
    conn = c.get_db_connection()
    products = conn.execute('''SELECT COUNT(*)
                              FROM products p JOIN usersProducts u
                              ON u.prod_id = p.id
                              WHERE u.user_id=?''', (current_user.id,)).fetchone()
    data['products'] = products[0]
    recipes = conn.execute('''SELECT COUNT(*)
                              FROM recipes r JOIN usersRecipes u
                              ON u.rec_id = r.id
                              WHERE u.user_id=?''', (current_user.id,)).fetchone()
    data['recipes'] = recipes[0]
    menus = conn.execute('''SELECT COUNT(*) FROM menu m
                              WHERE user_id=?''', (current_user.id,)).fetchone()
    data['menus'] = menus[0]
    return c.render_template('user.html', data=data)

@app.route('/about', methods=('GET', 'POST'))
def about():
    if c.request.method == 'POST':
        subject = c.request.form['subject']
        message = c.request.form['message']
        if message:
            msg = Message(subject, sender = 'adyazvinskaya@gmail.com', recipients = ['diet.creation@gmail.com'])
            msg.body = message
            mail.send(msg)
            return c.redirect(c.url_for('thanks'))
    return c.render_template('about.html')

@app.route('/thanks')
def thanks():
    return c.render_template('thanks.html')

from werkzeug.security import generate_password_hash, check_password_hash
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return c.redirect(c.url_for('user', user_id=current_user.id))

    form = LoginForm()
    if form.validate_on_submit():
        if c.request.method == 'POST':
            name = c.request.form['username']
            password = c.request.form['password']
            try:
                remember_me = c.request.form['remember_me']
            except c.BadRequest:
                remember_me = False

            con = sqlite3.connect('usersdb.db')
            cur = con.cursor()

            user_exist = cur.execute("SELECT * FROM users WHERE username=?",
                                     (name, )).fetchall()
            if user_exist:
                for user in user_exist:
                    if check_password_hash(user[3], password):
                        userLog = User(int(user[0]), user[1], user[2], user[3], user[4])
                        login_user(userLog, remember=remember_me)
                        return c.redirect(c.url_for('user', user_id=userLog.get_id()))
    return c.render_template('login.html', title='Sign In', form=form)

@app.route('/registration', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    con = sqlite3.connect('usersdb.db')
    cur = con.cursor()
    if c.request.method == 'POST':
        if c.request.form['username'] != "" and c.request.form['password'] != "" and c.request.form['email'] != "":
            name = c.request.form['username']
            email = c.request.form['email']
            password = c.request.form['password']

            username_exist = cur.execute("SELECT id, password FROM users WHERE username=?",
                                     (name,)).fetchone()
            email_exist = cur.execute("SELECT id, password FROM users WHERE email=?",
                                     (email,)).fetchone()

            if username_exist:
                c.flash('Username Exist!')
                print("Username Exist")
            elif email_exist:
                c.flash('Email Exist!')
                print("Email Exist")
            else:
                cur.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)",
                            (name, email, generate_password_hash(password)))
                users = cur.execute("SELECT * FROM users").fetchall()
                for user in users:
                    print(f"{user[0]} | {user[1]} | {user[2]} | {user[3]}")
                con.commit()
                con.close()
                return c.redirect(c.url_for('login'))

    return c.render_template('register.html', title='New user registration', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return c.redirect(url_for('index'))