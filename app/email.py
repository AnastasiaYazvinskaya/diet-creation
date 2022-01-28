import app.connect as c
from flask_mail import Message
from app import app, mail

@app.route("/send_email", methods=('GET','POST'))
def send_email():
    #if c.request.method == 'POST':
    #    data = c.request.form['data']
    msg = Message('Hello', sender = 'adyazvinskaya@gmail.com', recipients = ['diet.creation@gmail.com'])
    msg.body = "This is the email body"
    mail.send(msg)
    return c.render_template('about.html')
