import app.connect as c
from app import app
# Get recipe information by id (id, name, type, description)
def get_recipe(recipe_id):
    conn = c.get_db_connection()
    recipe = conn.execute('''SELECT r.id AS id, r.name AS name, rt.type AS type, r.descr AS descr
    FROM recipes r JOIN recipeTypes rt
    ON r.type_id = rt.id
    WHERE r.id = ?''', (recipe_id,)).fetchone()
    conn.close()
    if recipe is None:
        c.abort(404)
    return recipe
class RecipeAct:
    def __init__(self, recipe_id=None):
        self.conn = c.get_db_connection()
        self.types = self.conn.execute('SELECT * FROM recipeTypes').fetchall()
        self.prods = self.conn.execute('''SELECT p.id AS id, p.name AS name, p.weight AS weight, p.price AS price, s.name AS shop
            FROM products p JOIN shops s
            ON p.shop_id = s.id''').fetchall()
        self.shops = self.conn.execute('SELECT * FROM shops').fetchall()
        self.data = {'r_name': '', 'type': '', 'descr': '', 
                    'ingreds': {'names' : [],
                                'weights': []}
                    }
        self.error_p = []
        if recipe_id:
            self.recipe = get_recipe(recipe_id)
            ingredients = self.conn.execute('''SELECT * FROM ingredients
                WHERE rec_id=?''', (self.recipe['id'],)).fetchall()
            self.data = {'r_name': self.recipe['name'], 
                         'type': self.recipe['type'], 
                         'descr': self.recipe['descr'],
                         'ingreds': {'names': [],
                                     'weights': []}
                        }
            for ingred in ingredients:
                self.data['ingreds']['names'].append(ingred['prod_name'])
                self.data['ingreds']['weights'].append(ingred['weight'])
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
                prod_exist = self.conn.execute('SELECT * FROM products WHERE name=?',
                                                (ingred,)).fetchone()
                if not prod_exist:
                    self.error_p.append(ingred)
            # If one of the fields was not filled in, the existing data is saved and the page is reloaded
            if not self.data['r_name'] or self.error_p:
                c.flash('Name is required!')
            else:
                finish = func(type_id)
        return finish
    def create(self, type_id):
        self.conn.execute('INSERT INTO recipes (name, type_id, descr) VALUES (?, ?, ?)',
                    (self.data['r_name'], type_id[0], self.data['descr']))
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
# List of recipes page (open)
@app.route('/recipes')
def recipes():
    conn = c.get_db_connection()
    recipes = conn.execute('''SELECT r.id AS id, r.name AS name, rt.type AS type, r.descr AS descr
    FROM recipes r JOIN recipeTypes rt
    ON r.type_id = rt.id''').fetchall()
    conn.close()
    return c.render_template('recipes.html', recipes = recipes)
# Recipe information page (open)
@app.route('/recipe<int:recipe_id>')
def recipe(recipe_id):
    recipe = get_recipe(recipe_id)
    conn = c.get_db_connection()
    ingreds = conn.execute('''SELECT i.rec_id AS rec_id, i.prod_id AS prod_id, p.name AS name, i.weight AS weight
                            FROM ingredients i JOIN products p ON i.prod_id = p.id 
                            WHERE i.rec_id=?''',
                            (recipe_id,)).fetchall()
    conn.close()
    return c.render_template('recipe.html', recipe=recipe, ingreds=ingreds)
# Create recipe page (open, form handling)
@app.route('/create_recipe', methods=('GET', 'POST'))
def create_r():
    recipeAct = RecipeAct()
    if recipeAct.act(recipeAct.create):
        return c.redirect(c.url_for('recipes'))
    return c.render_template('create_r.html', prods=recipeAct.prods, types=recipeAct.types, shops=recipeAct.shops, data=recipeAct.data, errors=recipeAct.error_p)
# Edit recipe (open, form handling)
@app.route('/<int:id>_recipe_edit', methods=('GET', 'POST'))
def edit_r(id):
    recipeAct = RecipeAct(id)
    if recipeAct.act(recipeAct.edit):
        return c.redirect(c.url_for('recipes'))
    return c.render_template('edit_r.html', prods=recipeAct.prods, types=recipeAct.types, shops=recipeAct.shops, recipe=recipeAct.data, errors=recipeAct.error_p)
# Delete recipe
@app.route('/<int:id>/delete_recipe', methods=('POST',))
def delete_r(id):
    recipe = get_recipe(id)
    conn = c.get_db_connection()
    conn.execute('DELETE FROM recipes WHERE id = ?', (id,))
    conn.execute('DELETE FROM ingredients WHERE rec_id=?', (id,))
    conn.commit()
    conn.close()
    c.flash('"{}" was successfully deleted!'.format(recipe['name']))
    return c.redirect(c.url_for('recipes'))