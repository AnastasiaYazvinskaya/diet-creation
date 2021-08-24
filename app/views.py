from app import app
from flask import render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import BadRequest, abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?',
                        (product_id,)).fetchone()
    conn.close()
    if product is None:
        abort(404)
    return product

def get_recipe(recipe_id):
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?',
                        (recipe_id,)).fetchone()
    conn.close()
    if recipe is None:
        abort(404)
    return recipe

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/create_product', methods=('GET', 'POST'))
def create_p():
    if request.method == 'POST':
        name = request.form['name']
        weight = request.form['weight']
        price = request.form['price']
        shop = request.form['shop']

        if not name:
            flash('Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO products (name, weight, price, shop) VALUES (?, ?, ?, ?)',
                         (name, weight, price, shop))
            conn.commit()
            conn.close()
            return redirect(url_for('products'))
    return render_template('create_p.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit_p(id):
    product = get_product(id)

    if request.method == 'POST':
        name = request.form['name']
        weight = request.form['weight']
        price = request.form['price']
        shop = request.form['shop']

        if not name:
            flash('Name is requered!')


@app.route('/<int:id>/delete_product', methods=('POST',))
def delete_p(id):
    product = get_product(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(product['name']))
    return redirect(url_for('products'))

def create():
    i = 0
    create_r(i)
    i += 1

@app.route('/create_recipe', methods=('GET', 'POST'))
def create_r():
    if request.method == 'POST':
        r_name = request.form['r_name']
        type = request.form['type']
        descr = request.form['descr']

        ingreds = {
            'names': [],
            'weights': []
        }
        ingreds['names'].append(request.form['name_0'])
        ingreds['weights'].append(request.form['weight_0'])

        try:
            for i in range(1, 30):
                name = "name_"+str(i)
                weight = "weight_"+str(i)
                ingreds['names'].append(request.form[name])
                ingreds['weights'].append(request.form[weight])
                i += 1
        except BadRequest:
            pass
        
        if not r_name:
            flash('Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO recipes (name, type, descr) VALUES (?, ?, ?)',
                        (r_name, type, descr))
            rec_id = conn.execute('SELECT id FROM recipes WHERE name=?',
                                    (r_name,)).fetchall()
            rec_id = rec_id[0]
            for i in range(len(ingreds['names'])):
                conn.execute('INSERT INTO ingredients (rec_id, prod_name, weight) VALUES (?, ?, ?)',
                            (rec_id , ingreds['names'][i], ingreds['weights'][i]))
            conn.commit()
            conn.close()
            return redirect(url_for('recipes'))
    return render_template('create_r.html')

@app.route('/<int:id>/delete_recipe', methods=('POST',))
def delete_r(id):
    recipe = get_recipe(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM recipes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(recipe['name']))
    return redirect(url_for('recipes'))

@app.route('/products')
def products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('products.html', products = products)

@app.route('/recipes')
def recipes():
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return render_template('recipes.html', recipes = recipes)

@app.route('/<int:recipe_id>')
def recipe(recipe_id):
    recipe = get_recipe(recipe_id)
    return render_template('recipe.html', recipe=recipe)