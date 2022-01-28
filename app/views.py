import app.recipes as r
import app.products as p
import app.menu as m
#import app.test as t
import app.connect as c
from app import app, mail
from flask_mail import Message
# Starting-welcome page (just open)
@app.route('/')
@app.route('/index')
def index():
    return c.render_template('index.html')

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