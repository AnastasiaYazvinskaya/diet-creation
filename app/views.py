import app.recipes as r
import app.products as p
import app.menu as m
#import app.test as t
import app.connect as c
from app import app
# Starting-welcome page (just open)
@app.route('/')
@app.route('/index')
def index():
    return c.render_template('index.html')

@app.route('/about')
def about():
    return c.render_template('about.html')