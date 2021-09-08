import app.recipes as r
import app.products as p
import app.connect as c
from app import app
# Starting-welcome page (just open)
@app.route('/')
@app.route('/index')
def index():
    return c.render_template('index.html')