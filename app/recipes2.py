from math import fabs
import app.connect as c
from app import app
from flask_login import login_required, current_user

#JOIN usersRecipes u
#    ON u.rec_id = r.id
#    WHERE r.id = ? AND u.user_id=?, (recipe_id, current_user.id)

# Get recipe information by id (id, name, type, description)
def get_recipe(recipe_id):
    conn = c.get_db_connection()
    recipe = conn.execute('''SELECT r.id AS id, u.user_id AS user_id, r.name AS name, rt.type AS type, r.descr AS descr
    FROM recipes r JOIN recipeTypes rt
    ON r.type_id = rt.id
    JOIN usersRecipes u
    ON u.rec_id = r.id
    WHERE r.id = ?''', (recipe_id,)).fetchone()
    conn.close()
    if recipe is None:
        c.abort(404)
    return recipe
class RecipeAct:
    def __init__(self, recipe_id=None):
        self.conn = c.get_db_connection()
        self.types = self.conn.execute('SELECT * FROM recipeTypes').fetchall()
        self.prods = self.conn.execute('''SELECT p.id AS id, u.user_id AS user_id, p.name AS name, p.weight AS weight, p.price AS price, s.name AS shop
            FROM products p JOIN shops s
            ON p.shop_id = s.id
            JOIN usersProducts u
            ON u.prod_id = p.id
            WHERE u.user_id=?''', (current_user.id,)).fetchall()
        self.shops = self.conn.execute('SELECT * FROM shops').fetchall()
        self.data = {'r_name': '', 'type': '', 'descr': '', 
                    'ingreds': {'names' : [],
                                'weights': [],
                                'weight_type': []}
                    }
        self.error_p = []
        if recipe_id:
            self.recipe = get_recipe(recipe_id)
            ingredients = self.conn.execute('''SELECT i.rec_id AS rec_id, i.prod_id AS prod_id, p.name AS prod_name, i.weight AS weight, p.weightType AS weight_type
                                               FROM ingredients i JOIN products p
                                               ON i.prod_id = p.id
                                               WHERE i.rec_id=?''', (self.recipe['id'],)).fetchall()
            self.data = {'r_name': self.recipe['name'], 
                         'type': self.recipe['type'], 
                         'descr': self.recipe['descr'],
                         'ingreds': {'names': [],
                                     'weights': [],
                                     'weight_type': []}
                        }
            for ingred in ingredients:
                self.data['ingreds']['names'].append(ingred['prod_name'])
                self.data['ingreds']['weights'].append(ingred['weight'])
                self.data['ingreds']['weight_type'].append(ingred['weight_type'])
            self.conn.execute('DELETE FROM ingredients WHERE rec_id=?', (self.recipe['id'],))
    def act(self, func):
        finish = False
        # Form handling
        if c.request.method == 'POST':
            self.data['r_name'] = c.request.form['r_name']
            self.data['type'] = c.request.form['type']
            self.data['descr'] = c.request.form['descr']
            # Checking for the presence of the type in the db, adding, if necessary, and searching for its id
            type_exist = self.conn.execute('SELECT * FROM recipeTypes WHERE type=?',
                                        (self.data['type'],)).fetchone()
            if not type_exist:
                add = self.conn.execute('INSERT INTO recipeTypes (type) VALUES (?)',
                                    (self.data['type'],))
            type_id = self.conn.execute('SELECT * FROM recipeTypes WHERE type=?',
                                    (self.data['type'],)).fetchone()
            # Form handling - Creating new product
            try:
                for i in range(0, 30):
                    p_name = c.request.form["p_name_"+str(i)]
                    p_weight = c.request.form["p_weight_"+str(i)]
                    p_price = c.request.form["p_price_"+str(i)]
                    p_shop = c.request.form["p_shop_"+str(i)]
                    if p_weight and p_price and p_shop:
                        shop_exist = self.conn.execute('SELECT id FROM shops WHERE name=?',
                                            (p_shop,)).fetchone()
                        if not shop_exist:
                            add = self.conn.execute('INSERT INTO shops (name) VALUES (?)',
                                                (p_shop,))
                        shop_id = self.conn.execute('SELECT id FROM shops WHERE name=?',
                                                (p_shop,)).fetchone()
                        self.conn.execute('INSERT INTO products (name, weight, price, shop_id) VALUES (?, ?, ?, ?)',
                                        (p_name, p_weight, p_price, shop_id[0]))
            except c.BadRequest:
                pass
            # Finding all added ingredients
            try:
                self.data['ingreds']['names'] = []
                self.data['ingreds']['weights'] = []
                for i in range(0, 30):
                    name = "name_"+str(i)
                    weight = "weight_"+str(i)
                    # If name was filled in, then save this ingredient
                    if c.request.form[name]:
                        prod = c.request.form[name].split(' [')
                        self.data['ingreds']['names'].append(prod[0])
                        self.data['ingreds']['weights'].append(c.request.form[weight])
            except c.BadRequest:
                pass
            for ingred in self.data['ingreds']['names']:
                prod_exist = self.conn.execute('''SELECT * FROM products p
                                                 JOIN usersProducts u ON p.id=u.prod_id
                                                 WHERE p.name=? AND u.user_id=?''',
                                                (ingred, current_user.id)).fetchone()
                if not prod_exist:
                    self.error_p.append(ingred)
            # If one of the fields was not filled in, the existing data is saved and the page is reloaded
            if not self.data['r_name'] or self.error_p:
                c.flash('Name is required!')
            else:
                finish = func(type_id)
        return finish
    def create(self, type_id):
        self.conn.execute('INSERT INTO recipes (name, type_id, descr, user_id) VALUES (?, ?, ?, ?)',
                    (self.data['r_name'], type_id[0], self.data['descr'], current_user.id))
        rec_id = self.conn.execute('SELECT id FROM recipes WHERE name=?',
                            (self.data['r_name'],)).fetchone()
        self.conn.execute('INSERT INTO usersRecipes (user_id, rec_id) VALUES (?, ?)',
                    (current_user.id, rec_id[0]))
        for i in range(len(self.data['ingreds']['names'])):
            prod_id =self.conn.execute('SELECT p.id FROM products p JOIN usersProducts u WHERE p.name=? AND u.user_id=?', (self.data['ingreds']['names'][i], current_user.id)).fetchone()
            self.conn.execute('INSERT INTO ingredients (rec_id, prod_id, weight) VALUES (?, ?, ?)',
                        (rec_id[0], prod_id[0], self.data['ingreds']['weights'][i]))
        self.conn.commit()
        self.conn.close()
        return True
    def edit(self, type_id):
        self.conn.execute('UPDATE recipes SET name=?, type_id=?, descr=?'
                     'WHERE id=?',
                    (self.data['r_name'], type_id[0], self.data['descr'], self.recipe['id']))
        rec_id = self.conn.execute('SELECT id FROM recipes WHERE name=?',
                                (self.data['r_name'],)).fetchone()
        rec_id = rec_id[0]
        for i in range(len(self.data['ingreds']['names'])):
            prod_id =self.conn.execute('SELECT id FROM products WHERE name=?', (self.data['ingreds']['names'][i],)).fetchone()
            self.conn.execute('INSERT INTO ingredients (rec_id, prod_id, weight) VALUES (?, ?, ?)',
                        (rec_id , prod_id[0], self.data['ingreds']['weights'][i]))
        self.conn.commit()
        self.conn.close()
        return True
    def add(self, type_id):
        pass
# List of recipes page (open)
@app.route('/recipes')
def recipes():
    conn = c.get_db_connection()
    recipes = conn.execute('''SELECT r.id AS id, u.user_id AS user_id, r.name AS name, rt.type AS type, r.descr AS descr
                            FROM recipes r JOIN recipeTypes rt
                            ON r.type_id = rt.id
                            JOIN usersRecipes u
                            ON u.rec_id = r.id''').fetchall()
    ingreds = conn.execute('''SELECT i.rec_id AS rec_id, i.prod_id AS prod_id, p.name AS prod_name
                            FROM ingredients i JOIN products p ON i.prod_id = p.id''').fetchall()
    conn.close()
    return c.render_template('recipes.html', recipes = recipes, ingredients=ingreds)
# Recipe information page (open)
@app.route('/recipe<int:recipe_id>')
def recipe(recipe_id):
    recipe = get_recipe(recipe_id)
    conn = c.get_db_connection()
    ingreds = conn.execute('''SELECT i.rec_id AS rec_id, i.prod_id AS prod_id, p.name AS name, i.weight AS weight, p.weightType as weight_type 
                            FROM ingredients i JOIN products p ON i.prod_id = p.id 
                            WHERE i.rec_id=?''',
                            (recipe_id,)).fetchall()
    conn.close()
    return c.render_template('recipe.html', recipe=recipe, ingreds=ingreds)
# Create recipe page (open, form handling)
@app.route('/create_recipe', methods=('GET', 'POST'))
@login_required
def create_r():
    recipeAct = RecipeAct()
    if recipeAct.act(recipeAct.create):
        return c.redirect(c.url_for('recipes'))
    return c.render_template('create_r.html', prods=recipeAct.prods, types=recipeAct.types, shops=recipeAct.shops, data=recipeAct.data, errors=recipeAct.error_p)
# Edit recipe (open, form handling)
@app.route('/<int:recipe_id>_recipe_edit', methods=('GET', 'POST'))
@login_required
def edit_r(recipe_id):
    conn = c.get_db_connection()
    rec_id_exist = conn.execute('SELECT id FROM usersRecipes WHERE user_id=? AND rec_id=?', (current_user.id, recipe_id)).fetchone()
    if not rec_id_exist:
        conn.commit()
        conn.close()
        return c.redirect(c.url_for('recipes'))
    else:
        recipeAct = RecipeAct(recipe_id)
        if recipeAct.act(recipeAct.edit):
            return c.redirect(c.url_for('recipes'))
        return c.render_template('edit_r.html', prods=recipeAct.prods, types=recipeAct.types, shops=recipeAct.shops, recipe=recipeAct.data, errors=recipeAct.error_p)
# Delete recipe
@app.route('/<int:recipe_id>/delete_recipe', methods=('POST',))
@login_required
def delete_r(recipe_id):
    conn = c.get_db_connection()
    rec_id_exist = conn.execute('SELECT id FROM usersRecipes WHERE user_id=? AND rec_id=?', (current_user.id, recipe_id)).fetchone()
    if not rec_id_exist:
        conn.commit()
        conn.close()
        return c.redirect(c.url_for('recipes'))
    else:
        recipe = get_recipe(recipe_id)
        conn.execute('DELETE FROM usersRecipes WHERE user_id=? AND rec_id = ?', (current_user.id, recipe_id))
        #conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        #conn.execute('DELETE FROM ingredients WHERE rec_id=?', (recipe_id,))
        conn.commit()
        conn.close()
        c.flash('"{}" was successfully deleted!'.format(recipe['name']))
        return c.redirect(c.url_for('recipes'))

@app.route('/recipes_list', methods=('GET', 'POST'))
@login_required
def recipes_list():
    data = {
        "id": [],
        "user_id": [],
        "name": [],
        "type": [],
        "ingreds": [],
        "heart": True
    }
    if c.request.method == 'POST':
        getorder = int(c.request.form['data'])
        if getorder != 0:
            data['heart'] = False
            conn = c.get_db_connection()
            recipes = conn.execute('''SELECT r.id AS id, r.name AS name, rt.type AS type
                                    FROM recipes r JOIN recipeTypes rt
                                    ON r.type_id = rt.id
                                    JOIN usersRecipes u
                                    ON u.rec_id = r.id
                                    WHERE u.user_id=?''', (getorder,)).fetchall()
            ingreds = conn.execute('''SELECT i.rec_id AS rec_id, i.prod_id AS prod_id, p.name AS prod_name
                                    FROM ingredients i JOIN products p ON i.prod_id = p.id
                                    JOIN usersRecipes u ON u.rec_id = i.rec_id WHERE u.user_id=?''',(getorder,)).fetchall()
            conn.close()
            for recipe in recipes:
                data['id'].append(recipe[0])
                data['name'].append(recipe[1])
                data['type'].append(recipe[2])
                data['ingreds'].append([])
            for ingred in ingreds:
                for recipe in data['id']:
                    if ingred[0] == recipe:
                        data['ingreds'][data['id'].index(recipe)].append(ingred[2])
        else:
            print("Show total recipes")
            conn = c.get_db_connection()
            recipes = conn.execute('''SELECT r.id AS id, r.name AS name, rt.type AS type, r.user_id AS user_id
                                    FROM recipes r JOIN recipeTypes rt
                                    ON r.type_id = rt.id
                                    JOIN usersRecipes u
                                    ON u.rec_id = r.id''').fetchall()
            ingreds = conn.execute('''SELECT i.rec_id AS rec_id, i.prod_id AS prod_id, p.name AS prod_name
                                    FROM ingredients i JOIN products p ON i.prod_id = p.id''').fetchall()
            conn.close()
            for recipe in recipes:
                data['id'].append(recipe[0])
                data['user_id'].append(recipe[3])
                data['name'].append(recipe[1])
                data['type'].append(recipe[2])
                data['ingreds'].append([])
            for ingred in ingreds:
                for recipe in data['id']:
                    if ingred[0] == recipe:
                        data['ingreds'][data['id'].index(recipe)].append(ingred[2])
    return c.jsonify(data)
