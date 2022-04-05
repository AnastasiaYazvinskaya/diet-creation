import app.connect as c
from app import app
from flask_login import login_required, current_user
from app.recipe import Recipe, RecipeAct

#JOIN usersRecipes u
#    ON u.rec_id = r.id
#    WHERE r.id = ? AND u.user_id=?, (recipe_id, current_user.id)

# Get recipe information by id (id, name, type, description)
def get_recipe(recipe_id):
    conn = c.get_db_connection()
    recipe = conn.execute('''SELECT r.id AS id, u.user_id AS user_id, r.name AS name, REPLACE(GROUP_CONCAT(DISTINCT rt.type), ",", ", ") AS type, r.description AS description
    FROM recipeTypesRecipes rtr 
    JOIN recipes r ON r.id = rtr.recipe_id
    JOIN recipeTypes rt ON rt.id = rtr.recipe_type_id
    JOIN usersRecipes u ON u.recipe_id = r.id
    WHERE r.id = ?''', (recipe_id,)).fetchone()
    conn.close()
    if recipe is None:
        c.abort(404)
    return recipe

# List of recipes page (open)
@app.route('/recipes')
def recipes():
    conn = c.get_db_connection()
    my_recipes = None
    if current_user.is_authenticated:
        my_recipes = conn.execute('''SELECT r.id AS id, u.user_id AS user_id, r.name AS name, REPLACE(GROUP_CONCAT(DISTINCT rt.type), ",", ", ") AS type, REPLACE(GROUP_CONCAT(DISTINCT sp.name), ",", ", ") AS ingredients, r.user_id AS createdBy
                                FROM usersRecipes u
                                JOIN recipes r ON r.id = u.recipe_id
                                JOIN recipeTypesRecipes rtr ON r.id = rtr.recipe_id
                                JOIN recipeTypes rt ON rt.id = rtr.recipe_type_id
                                JOIN ingredients i ON i.recipe_id = r.id
                                JOIN simpleProducts sp ON i.product_id = sp.id
                                WHERE u.user_id=?
                                GROUP BY i.recipe_id''', (current_user.id,)).fetchall()
    recipes = conn.execute('''SELECT r.id AS id, GROUP_CONCAT(DISTINCT u.user_id) AS user_id, r.name AS name, REPLACE(GROUP_CONCAT(DISTINCT rt.type), ",", ", ") AS type, REPLACE(GROUP_CONCAT(DISTINCT sp.name), ",", ", ") AS ingredients, r.user_id AS createdBy
                            FROM recipes r 
                            JOIN recipeTypesRecipes rtr ON r.id = rtr.recipe_id
                            JOIN recipeTypes rt ON rt.id = rtr.recipe_type_id
                            JOIN usersRecipes u ON u.recipe_id = r.id
                            JOIN ingredients i ON i.recipe_id = r.id
                            JOIN simpleProducts sp ON i.product_id = sp.id
                            GROUP BY i.recipe_id''').fetchall()
    my_data = {'heart':[]}
    total_data = {'heart':[]}
    if current_user.is_authenticated:
        for i in range(len(my_recipes)):
            if my_recipes[i][5] != my_recipes[i][1]:
                my_data['heart'].append(True)
            else: my_data['heart'].append(False)
        for i in range(len(recipes)):
            user_ids = recipes[i][1].split(",")
            for id in user_ids:
                if current_user.id == int(id):
                    total_data['heart'].append(True)
            if len(total_data['heart']) != i+1:
                total_data['heart'].append(False)
    conn.close()
    return c.render_template('recipes.html', my_recipes = my_recipes, recipes = recipes, my_heart = my_data, total_heart = total_data)
# Recipe information page (open)
@app.route('/recipe<int:recipe_id>')
def recipe(recipe_id):
    recipe = get_recipe(recipe_id)
    description = recipe['description'].split('endofstep')#('\r\n')
    conn = c.get_db_connection()
    ingredients = conn.execute('''SELECT i.recipe_id AS recipe_id, i.product_id AS product_id, sp.name AS name, i.weight AS weight, i.weight_type as weight_type 
                            FROM ingredients i JOIN simpleProducts sp ON i.product_id = sp.id 
                            WHERE i.recipe_id=?''',
                            (recipe_id,)).fetchall()
    conn.close()
    return c.render_template('recipe.html', recipe=recipe, ingredients=ingredients, description=description)
# Create recipe page (open, form handling)
@app.route('/create_recipe', methods=('GET', 'POST'))
@login_required
def create_r():
    conn = c.get_db_connection()
    types = conn.execute('SELECT * FROM recipeTypes WHERE id != 1').fetchall()
    products = conn.execute('SELECT * FROM simpleProducts WHERE id != 1').fetchall()
    r_products = conn.execute('SELECT * FROM recipes WHERE as_product=true').fetchall()
    conn.close()
    recipeAct = RecipeAct()
    if recipeAct.act(recipeAct.create):
        return c.redirect(c.url_for('recipes'))
    return c.render_template('create_r.html',products = products, r_products = r_products, types=types)
# Edit recipe (open, form handling)
@app.route('/<int:recipe_id>_recipe_edit', methods=('GET', 'POST'))
@login_required
def edit_r(recipe_id):
    conn = c.get_db_connection()
    rec_id_exist = bool(conn.execute('SELECT id FROM recipes WHERE user_id=? AND id=?', (current_user.id, recipe_id)).fetchone())
    if not rec_id_exist:
        conn.commit()
        conn.close()
        return c.redirect(c.url_for('recipes'))
    else:
        types = conn.execute('SELECT * FROM recipeTypes WHERE id != 1').fetchall()
        products = conn.execute('SELECT * FROM simpleProducts WHERE id != 1').fetchall()
        r_products = conn.execute('SELECT * FROM recipes WHERE as_product=true').fetchall()
        conn.commit()
        conn.close()
        recipeAct = RecipeAct(recipe_id)
        if recipeAct.act(recipeAct.edit):
            return c.redirect(c.url_for('recipes'))
        return c.render_template('edit_r.html', products=products, r_products = r_products, types=types, recipe=recipeAct.recipe)
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
        "recipes": 2,
        "id": [],
        "user_id": [],
        "created_by": [],
        "name": [],
        "type": [],
        "ingreds": [],
        "heart": []
    }
    if c.request.method == 'POST':
        getorder = int(c.request.form['data'])
        conn = c.get_db_connection()
        if getorder != 0:
            data['recipes'] = current_user.id
            recipes = conn.execute('''SELECT r.id AS id, u.user_id AS user_id, r.name AS name, REPLACE(GROUP_CONCAT(DISTINCT rt.type), ",", ", ") AS type, REPLACE(GROUP_CONCAT(DISTINCT sp.name), ",", ", ") AS ingredients, r.user_id AS createdBy
                            FROM usersRecipes u
                            JOIN recipes r ON r.id = u.recipe_id
                            JOIN recipeTypesRecipes rtr ON r.id = rtr.recipe_id
                            JOIN recipeTypes rt ON rt.id = rtr.recipe_type_id
                            JOIN ingredients i ON i.recipe_id = r.id
                            JOIN simpleProducts sp ON i.product_id = sp.id
                            WHERE u.user_id=?
                            GROUP BY i.recipe_id''', (current_user.id,)).fetchall()
            
            for recipe in recipes:
                data['id'].append(recipe[0])
                data['created_by'].append(recipe[5])
                data['name'].append(recipe[2])
                data['type'].append(recipe[3])
                data['ingreds'].append(recipe[4])
                if data['created_by'] != recipe[1]:
                    data['heart'].append(True)
                else: data['heart'].append(False)
        else:
            data['recipes'] = 0
            recipes = conn.execute('''SELECT r.id AS id, GROUP_CONCAT(DISTINCT u.user_id) AS user_id, r.name AS name, REPLACE(GROUP_CONCAT(DISTINCT rt.type), ",", ", ") AS type, REPLACE(GROUP_CONCAT(DISTINCT sp.name), ",", ", ") AS ingredients, r.user_id AS createdBy
                            FROM recipeTypesRecipes rtr 
                            JOIN recipes r ON r.id = rtr.recipe_id
                            JOIN recipeTypes rt ON rt.id = rtr.recipe_type_id
                            JOIN usersRecipes u ON u.recipe_id = r.id
                            JOIN ingredients i ON i.recipe_id = r.id
                            JOIN simpleProducts sp ON i.product_id = sp.id
                            GROUP BY i.recipe_id''').fetchall()
            
            for i in range(len(recipes)):
                data['id'].append(recipes[i][0])
                user_ids = recipes[i][1].split(",")
                data['user_id'].append(recipes[i][1])
                data['created_by'].append(recipes[i][5])
                data['name'].append(recipes[i][2])
                data['type'].append(recipes[i][3])
                data['ingreds'].append(recipes[i][4])
                for id in user_ids:
                    if current_user.id == int(id):
                        data['heart'].append(True)
                if len(data['heart']) != i+1:
                    data['heart'].append(False)
        conn.commit()
        conn.close()
    return c.jsonify(data) 

@app.route('/like', methods=('GET', 'POST'))
@login_required
def like():
    if c.request.method == 'POST':
        getorder = c.request.form['like']
        getorder = getorder.split(",")
        conn = c.get_db_connection()
        exist = conn.execute('SELECT id FROM usersRecipes WHERE user_id=? AND recipe_id=?', (int(getorder[1]), int(getorder[2]))).fetchone()
        if not exist:
            conn.execute('INSERT INTO usersRecipes (user_id, recipe_id) VALUES (?,?)', (int(getorder[1]), int(getorder[2])))
            getorder[0] = 1
        else:
            conn.execute('DELETE FROM usersRecipes WHERE user_id=? AND recipe_id=?', (int(getorder[1]), int(getorder[2])))
            getorder[0] = 0
        conn.commit()
        conn.close()
    return c.jsonify({'like':int(getorder[0])})

@app.route('/add_recipe_types', methods=('GET', 'POST'))
@login_required
def add_recipe_types():
    if c.request.method == 'POST':
        conn = c.get_db_connection()
        r_types = conn.execute('SELECT * FROM recipeTypes WHERE recipe_type != 1 AND type != "general"').fetchall()
        types = {
            'id': [],
            'recipe_type': [],
            'type': []
        }
        for type in r_types:
            types['id'].append(type['id'])
            types['recipe_type'].append(type['recipe_type'])
            types['type'].append(type['type'])
        conn.commit()
        conn.close()
    return c.jsonify(types)
