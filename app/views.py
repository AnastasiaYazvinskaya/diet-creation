import sqlite3
from flask import flash, render_template, request, url_for
import app.recipes as r
import app.products as p
#import app.menu as m
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
                              ON u.product_id = p.id
                              WHERE u.user_id=?''', (current_user.id,)).fetchone()
    data['products'] = products[0]
    recipes = conn.execute('''SELECT COUNT(*)
                              FROM recipes r JOIN usersRecipes u
                              ON u.recipe_id = r.id
                              WHERE u.user_id=?''', (current_user.id,)).fetchone()
    data['recipes'] = recipes[0]
    #menus = conn.execute('''SELECT COUNT(*) FROM menu m
    #                          WHERE user_id=?''', (current_user.id,)).fetchone()
    #data['menus'] = menus[0]

    #con = c.get_users_db_connection()
    #user_icons = con.execute("SELECT * FROM user_icons").fetchall()
    #con.commit()
    conn.commit()
    conn.close()
    #con.close()

    return c.render_template('user.html', data=data)#, user_icons=user_icons)

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

            con = c.get_users_db_connection()

            user_exist = con.execute("""SELECT u.id AS id, role, username, email, password, icon FROM users u 
                                        JOIN user_icons ui ON u.icon_id=ui.id WHERE u.username=?""",(name, )).fetchall()
            if user_exist:
                for user in user_exist:
                    if check_password_hash(user[4], password):
                        userLog = User(int(user[0]), user[1], user[2], user[3], user[4], user[5])
                        login_user(userLog, remember=remember_me)
                        con.commit()
                        con.close()
                        return c.redirect(c.url_for('user', user_id=userLog.get_id()))
    return c.render_template('login.html', title='Sign In', form=form)

@app.route('/registration', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    con = c.get_users_db_connection()
    user_icons = con.execute("SELECT * FROM user_icons").fetchall()

    if c.request.method == 'POST':
        if c.request.form['username'] != "" and c.request.form['password'] != "" and c.request.form['email'] != "":
            name = c.request.form['username']
            email = c.request.form['email']
            password = c.request.form['password']
            icon = c.request.form['icon']

            username_exist = con.execute("SELECT id, password FROM users WHERE username=?",
                                     (name,)).fetchone()
            email_exist = con.execute("SELECT id, password FROM users WHERE email=?",
                                     (email,)).fetchone()

            if username_exist:
                c.flash('Username Exist!')
            elif email_exist:
                c.flash('Email Exist!')
            else:
                con.execute("INSERT INTO users (username, email, password, icon_id) VALUES (?,?,?,?)",
                            (name, email, generate_password_hash(password), int(icon)))
                users = con.execute("SELECT * FROM users").fetchall()
                con.commit()
                con.close()
                return c.redirect(c.url_for('login'))

    return c.render_template('register.html', title='New user registration', form=form, user_icons=user_icons)

@app.route('/logout')
def logout():
    logout_user()
    return c.redirect(url_for('index'))

@app.route('/choose_avatar', methods=('GET', 'POST'))
def choose_avatar():
    if c.request.method == "POST":
        con = c.get_users_db_connection()
        user_icons = con.execute('SELECT * FROM user_icons').fetchall()
        icons = {
            'id': [],
            'icon': []
        }
        for icon in user_icons:
            icons['id'].append(icon['id'])
            icons['icon'].append(icon['icon'])
        con.commit()
        con.close()
    return c.jsonify(icons)

@app.route('/update_icon', methods=('GET', 'POST'))
def update_icon():
    if c.request.method == "POST":
        icon = c.request.form['data']
        con = c.get_users_db_connection()
        con.execute("UPDATE users SET icon_id=? WHERE id=?", (icon,current_user.id))
        icon_text = con.execute("SELECT icon FROM user_icons WHERE id=?", (icon,)).fetchone()
        icon = {
            'icon': icon_text[0]
        }
        con.commit()
        con.close()
    return c.jsonify(icon)
