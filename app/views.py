from types import MethodType
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
    recipe = conn.execute('''SELECT r.id AS id, r.name AS name, rt.type AS type, r.descr AS descr
FROM recipes r JOIN recipeTypes rt
ON r.type_id = rt.id
WHERE r.id = ?''', (recipe_id,)).fetchone()
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
    conn = get_db_connection()
    shops = conn.execute('SELECT * FROM shops').fetchall()
    if request.method == 'POST':
        name = request.form['name']
        weight = request.form['weight']
        price = request.form['price']
        shop = request.form['shop']

        if not name:
            flash('Name is required!')
        else:
            shop_exist = conn.execute('SELECT id FROM shops WHERE name=?',
                                        (shop,)).fetchone()
            if not shop_exist:
                add = conn.execute('INSERT INTO shops (name) VALUES (?)',
                                    (shop,))
            shop_id = conn.execute('SELECT id FROM shops WHERE name=?',
                                    (shop,)).fetchone()
            conn.execute('INSERT INTO products (name, weight, price, shop_id) VALUES (?, ?, ?, ?)',
                         (name, weight, price, shop_id[0]))
            conn.commit()
            conn.close()
            return redirect(url_for('products'))
    return render_template('create_p.html', shops=shops)

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

@app.route('/adding_new_products')#, methods=('GET', 'POST'))
def add_ps():
    pass
    #return render_template('add_ps.html')#, prods=prods, types=types)#, shops=shops, errors=errors, added=added)

@app.route('/create_recipe', methods=('GET', 'POST'))
def create_r():
    conn = get_db_connection()
    types = conn.execute('SELECT * FROM recipeTypes').fetchall()
    prods = conn.execute('''SELECT p.id AS id, p.name AS name, p.weight AS weight, p.price AS price, s.name AS shop
FROM products p JOIN shops s
ON p.shop_id = s.id''').fetchall()

    if request.method == 'POST':
        r_name = request.form['r_name']
        type = request.form['type']
        descr = request.form['descr']
        error_p = []

        type_exist = conn.execute('SELECT * FROM recipeTypes WHERE type=?',
                                    (type,)).fetchone()
        if not type_exist:
            add = conn.execute('INSERT INTO recipeTypes (type) VALUES (?)',
                                (type,))
        type_id = conn.execute('SELECT * FROM recipeTypes WHERE type=?',
                                (type,)).fetchone()

        try:
            for i in range(0, 30):
                p_name = request.form["p_name_"+str(i)]
                p_weight = request.form["p_weight_"+str(i)]
                p_price = request.form["p_price_"+str(i)]
                p_shop = request.form["p_shop_"+str(i)]
                if p_weight and p_price and p_shop:
                    shop_exist = conn.execute('SELECT id FROM shops WHERE name=?',
                                        (p_shop,)).fetchone()
                    if not shop_exist:
                        add = conn.execute('INSERT INTO shops (name) VALUES (?)',
                                            (p_shop,))
                    shop_id = conn.execute('SELECT id FROM shops WHERE name=?',
                                            (p_shop,)).fetchone()
                    conn.execute('INSERT INTO products (name, weight, price, shop_id) VALUES (?, ?, ?, ?)',
                                (p_name, p_weight, p_price, shop_id[0]))
        except BadRequest:
            pass

        ingreds = {
            'names': [],
            'weights': []
        }
        try:
            for i in range(0, 30):
                name = "name_"+str(i)
                weight = "weight_"+str(i)
                ingreds['names'].append(request.form[name])

                prod_exist = conn.execute('SELECT * FROM products WHERE name=?',
                                        (ingreds['names'][i],)).fetchone()
                if not prod_exist:
                    error_p.append(ingreds['names'][i])

                ingreds['weights'].append(request.form[weight])
        except BadRequest:
            pass
        
        if not r_name:
            flash('Name is required!')
        elif error_p:
            data = []
            data.extend((r_name, type, descr, ingreds))
            shops = conn.execute('SELECT * FROM shops').fetchall()
            return render_template('create_r.html',shops=shops, data=data, errors=error_p)
        else:
            conn.execute('INSERT INTO recipes (name, type_id, descr) VALUES (?, ?, ?)',
                        (r_name, type_id[0], descr))
            rec_id = conn.execute('SELECT id FROM recipes WHERE name=?',
                                    (r_name,)).fetchone()
            rec_id = rec_id[0]
            for i in range(len(ingreds['names'])):
                conn.execute('INSERT INTO ingredients (rec_id, prod_name, weight) VALUES (?, ?, ?)',
                            (rec_id , ingreds['names'][i], ingreds['weights'][i]))
            conn.commit()
            conn.close()
            return redirect(url_for('recipes'))
    return render_template('create_r.html', prods=prods, types=types)#, shops=shops, errors=errors, added=added)

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
    products = conn.execute('''SELECT p.id AS id, p.name AS name, p.weight AS weight, p.price AS price, s.name AS shop
FROM products p JOIN shops s
ON p.shop_id = s.id''').fetchall()
    conn.close()
    return render_template('products.html', products = products)#, shops=shops)

@app.route('/recipes')
def recipes():
    conn = get_db_connection()
    recipes = conn.execute('''SELECT r.id AS id, r.name AS name, rt.type AS type, r.descr AS descr
FROM recipes r JOIN recipeTypes rt
ON r.type_id = rt.id''').fetchall()
    conn.close()
    return render_template('recipes.html', recipes = recipes)

@app.route('/<int:recipe_id>')
def recipe(recipe_id):
    recipe = get_recipe(recipe_id)
    conn = get_db_connection()
    ingreds = conn.execute('SELECT * FROM ingredients WHERE rec_id=?',
                            (recipe_id,)).fetchall()
    #types = conn.execute('SELECT * FROM recipeTypes').fetchall()
    conn.close()
    return render_template('recipe.html', recipe=recipe, ingreds=ingreds)