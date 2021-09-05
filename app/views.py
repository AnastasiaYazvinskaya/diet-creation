from types import MethodType
from app import app
from flask import render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import BadRequest, InternalServerError, abort
# Get connection to db
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
# Get product information by id (id, name, weight, price, shop_name)
def get_product(product_id):
    conn = get_db_connection()
    product = conn.execute('''SELECT p.id AS id, p.name AS name, p.weight AS weight, p.price AS price, s.name AS shop
    FROM products p JOIN shops s
    ON p.shop_id = s.id
    WHERE p.id = ?''', (product_id,)).fetchone()
    conn.close()
    if product is None:
        abort(404)
    return product
# Get recipe information by id (id, name, type, description)
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
# Starting-welcome page (just open)
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
# Create new product page (open, form handling)
@app.route('/create_product', methods=('GET', 'POST'))
def create_p():
    conn = get_db_connection()
    shops = conn.execute('SELECT * FROM shops').fetchall()
    data = {'name': '', 'weight': '', 'price': '', 'shop': ''}
    # Form handling
    if request.method == 'POST':
        name = request.form['name']
        weight = request.form['weight']
        price = request.form['price']
        shop = request.form['shop']
        # If one of the fields was not filled in, the existing data is saved and the page is reloaded
        if not name or not weight or not price or not shop:
            data['name'] = name
            data['weight'] = weight
            data['price'] = price
            data['shop'] = shop
            flash('Name is required!')
        # If all fields was filled in, the existing data is added to the db
        else:
            # (HERE) Checking for the presence of the same product
            # Checking for the presence of a store in the db, adding, if necessary, and searching for its id
            shop_exist = conn.execute('SELECT id FROM shops WHERE name=?',
                                        (shop,)).fetchone()
            if not shop_exist:
                add = conn.execute('INSERT INTO shops (name) VALUES (?)',
                                    (shop,))
            shop_id = conn.execute('SELECT id FROM shops WHERE name=?',
                                    (shop,)).fetchone()
            # Inserting product to the db
            conn.execute('INSERT INTO products (name, weight, price, shop_id) VALUES (?, ?, ?, ?)',
                         (name, weight, price, shop_id[0]))
            conn.commit()
            conn.close()
            return redirect(url_for('products'))
    return render_template('create_p.html', shops=shops, data=data)
# Edit product page (open, form handling)
@app.route('/<int:id>_product_edit', methods=('GET', 'POST'))
def edit_p(id):
    conn = get_db_connection()
    product = get_product(id)
    shops = conn.execute('SELECT * FROM shops').fetchall()
    data = {'name': product['name'], 'weight': product['weight'], 'price': product['price'], 'shop': product['shop']}
    # Form handling
    if request.method == 'POST':
        name = request.form['name']
        weight = request.form['weight']
        price = request.form['price']
        shop = request.form['shop']

        if not name or not weight or not price or not shop:
            data['name'] = name
            data['weight'] = weight
            data['price'] = price
            data['shop'] = shop
            flash('Name is requered!')
        else:
            shop_exist = conn.execute('SELECT id FROM shops WHERE name=?',
                                        (shop,)).fetchone()
            if not shop_exist:
                add = conn.execute('INSERT INTO shops (name) VALUES (?)',
                                    (shop,))
            shop_id = conn.execute('SELECT id FROM shops WHERE name=?',
                                    (shop,)).fetchone()
            conn.execute('UPDATE products SET name=?, weight=?, price=?, shop_id=?'
                         'WHERE id=?',
                         (name, weight, price, shop_id[0], id))
            conn.commit()
            conn.close()
            return redirect(url_for('products'))
    return render_template('edit_p.html', shops=shops, product=data)
# Delete product
@app.route('/<int:id>/delete_product', methods=('POST',))
def delete_p(id):
    product = get_product(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(product['name']))
    return redirect(url_for('products'))
# Create recipe page (open, form handling)
@app.route('/create_recipe', methods=('GET', 'POST'))
def create_r():
    conn = get_db_connection()
    types = conn.execute('SELECT * FROM recipeTypes').fetchall()
    prods = conn.execute('''SELECT p.id AS id, p.name AS name, p.weight AS weight, p.price AS price, s.name AS shop
    FROM products p JOIN shops s
    ON p.shop_id = s.id''').fetchall()
    shops = conn.execute('SELECT * FROM shops').fetchall()
    data = {'r_name': '', 'type': '', 'descr': '', 'ingreds': ''}
    error_p = []
    # Form handling
    if request.method == 'POST':
        r_name = request.form['r_name']
        type = request.form['type']
        descr = request.form['descr']
        # Checking for the presence of the type in the db, adding, if necessary, and searching for its id
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
        # Finding all added ingredients
        ingreds = {
            'names': [],
            'weights': []
        }
        try:
            for i in range(0, 30):
                name = "name_"+str(i)
                weight = "weight_"+str(i)
                # If name was filled in, then save this ingredient
                if request.form[name]:
                    prod = request.form[name].split(' [')

                    ingreds['names'].append(prod[0])

                    prod_exist = conn.execute('SELECT * FROM products WHERE name=?',
                                            (ingreds['names'][i],)).fetchone()
                    if not prod_exist:
                        error_p.append(ingreds['names'][i])

                    ingreds['weights'].append(request.form[weight])
        except BadRequest:
            pass
        # If one of the fields was not filled in, the existing data is saved and the page is reloaded
        if not r_name or error_p:
            data['r_name'] = r_name
            data['type'] = type
            data['descr'] = descr
            data['ingreds'] = ingreds
            flash('Name is required!')
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
    return render_template('create_r.html', prods=prods, types=types, shops=shops, data=data, errors=error_p)
# Edit recipe (open, form handling)
@app.route('/<int:id>_recipe_edit', methods=('GET', 'POST'))
def edit_r(id):
    conn = get_db_connection()
    recipe = get_recipe(id)
    ingredients = conn.execute('''SELECT * FROM ingredients
    WHERE rec_id=?''', (id,)).fetchall()
    types = conn.execute('SELECT * FROM recipeTypes').fetchall()
    prods = conn.execute('''SELECT p.id AS id, p.name AS name, p.weight AS weight, p.price AS price, s.name AS shop
    FROM products p JOIN shops s
    ON p.shop_id = s.id''').fetchall()
    shops = conn.execute('SELECT * FROM shops').fetchall()
    data = {'r_name': recipe['name'], 'type': recipe['type'], 'descr': recipe['descr'],
            'ingreds': {'names': [],
                        'weights': []}
            }
    for ingred in ingredients:
        data['ingreds']['names'].append(ingred['prod_name'])
        data['ingreds']['weights'].append(ingred['weight'])
    error_p = []
    # Form handling
    if request.method == 'POST':
        r_name = request.form['r_name']
        type = request.form['type']
        descr = request.form['descr']
        # Checking for the presence of the type in the db, adding, if necessary, and searching for its id
        type_exist = conn.execute('SELECT * FROM recipeTypes WHERE type=?',
                                    (type,)).fetchone()
        if not type_exist:
            add = conn.execute('INSERT INTO recipeTypes (type) VALUES (?)',
                                (type,))
        type_id = conn.execute('SELECT * FROM recipeTypes WHERE type=?',
                                (type,)).fetchone()
        # Form handling - Creating new product
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
        # Finding all added ingredients
        try:
            data['ingreds']['names'] = []
            data['ingreds']['weights'] = []
            for i in range(0, 30):
                name = "name_"+str(i)
                weight = "weight_"+str(i)
                # If name was filled in, then save this ingredient
                if request.form[name]:
                    prod = request.form[name].split(' [')

                    data['ingreds']['names'].append(prod[0])

                    prod_exist = conn.execute('SELECT * FROM products WHERE name=?',
                                            (data['ingreds']['names'][i],)).fetchone()
                    if not prod_exist:
                        error_p.append(data['ingreds']['names'][i])

                    data['ingreds']['weights'].append(request.form[weight])
        except BadRequest:
            pass
        # If one of the fields was not filled in, the existing data is saved and the page is reloaded
        if not r_name or error_p:
            data['r_name'] = r_name
            data['type'] = type
            data['descr'] = descr
            flash('Name is required!')
        else:
            conn.execute('UPDATE recipes SET name=?, type_id=?, descr=?'
                         'WHERE id=?',
                        (r_name, type_id[0], descr, recipe['id']))
            rec_id = conn.execute('SELECT id FROM recipes WHERE name=?',
                                    (r_name,)).fetchone()
            rec_id = rec_id[0]
            for i in range(len(data['ingreds']['names'])):
                ingred_exist = conn.execute('SELECT * FROM ingredients WHERE rec_id=? AND prod_name=?',
                                            (rec_id, data['ingreds']['names'][i],)).fetchone()
                if ingred_exist:
                    ingred_id = ingred_exist[0]
                    conn.execute('UPDATE ingredients SET prod_name=?, weight=?'
                                 'WHERE id=?',
                                 (data['ingreds']['names'][i], data['ingreds']['weights'][i], ingred_id))
                else:
                    conn.execute('INSERT INTO ingredients (rec_id, prod_name, weight) VALUES (?, ?, ?)',
                                 (rec_id, data['ingreds']['names'][i], data['ingreds']['weights'][i]))
            conn.commit()
            conn.close()
            return redirect(url_for('recipes'))
    return render_template('edit_r.html', prods=prods, types=types, shops=shops, recipe=data, errors=error_p)
# Delete recipe
@app.route('/<int:id>/delete_recipe', methods=('POST',))
def delete_r(id):
    recipe = get_recipe(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM recipes WHERE id = ?', (id,))
    conn.execute('DELETE FROM ingredients WHERE rec_id=?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(recipe['name']))
    return redirect(url_for('recipes'))
# List of products page (open)
@app.route('/products')
def products():
    conn = get_db_connection()
    products = conn.execute('''SELECT p.id AS id, p.name AS name, p.weight AS weight, p.price AS price, s.name AS shop
    FROM products p JOIN shops s
    ON p.shop_id = s.id''').fetchall()
    conn.close()
    return render_template('products.html', products = products)#, shops=shops)
# List of recipes page (open)
@app.route('/recipes')
def recipes():
    conn = get_db_connection()
    recipes = conn.execute('''SELECT r.id AS id, r.name AS name, rt.type AS type, r.descr AS descr
    FROM recipes r JOIN recipeTypes rt
    ON r.type_id = rt.id''').fetchall()
    conn.close()
    return render_template('recipes.html', recipes = recipes)
# Recipe information page (open)
@app.route('/<int:recipe_id>')
def recipe(recipe_id):
    recipe = get_recipe(recipe_id)
    conn = get_db_connection()
    ingreds = conn.execute('SELECT * FROM ingredients WHERE rec_id=?',
                            (recipe_id,)).fetchall()
    #types = conn.execute('SELECT * FROM recipeTypes').fetchall()
    conn.close()
    return render_template('recipe.html', recipe=recipe, ingreds=ingreds)