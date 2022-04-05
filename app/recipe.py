import app.connect as c
from flask_login import current_user

class Recipe:
    def __init__(self):
        self.id = None
        self.name = None            # Recipe name
        self.description = None     # Cooking description
        self.as_product = None      # Recipe as ingredient (product)

        self.recipe_photo = None    # Photo of the dish
        self.time = None            # Cooking time
        self.portions = None        # Number of portions
        self.portion_weight = None  # Protion weight
        self.kcal = None            # Kcal
        self.average_price = None   # Average price of the 

        self.ingredients = {        # Recipe ingredients
            'id': [],
            'name':[],
            'weight':[],
            'weight_type':[]
        }

        self.dish_type = None       # Recipe type
        self.meal_type = None
        self.kitchen_type = None
        self.other_type = None

        #self.conn = c.get_db_connection() # connect to the database
        #self.cur = self.conn.cursor()

    def set_required_data(self, name, ingredients, description, as_product):
        self.name = name
        self.ingredients['name'] = ingredients['name']
        self.ingredients['weight'] = ingredients['weight']
        self.ingredients['weight_type'] = ingredients['weight_type']
        self.description = description
        self.as_product = as_product
    def set_types(self, meal, kitchen, other):
        self.meal_type = meal
        self.kitchen_type = kitchen
        self.other_type = other
    def set_photo(self, photo=None):
        self.recipe_photo = photo
    def set_dish_type(self, dish=None):
        self.dish_type = dish
    def set_additional_data(self, time=None, portions=None, portion_weight=None, kcal=None):#, average_price=None):
        self.time = time
        self.portions = portions
        self.portion_weight = portion_weight
        self.kcal = kcal
        #self.average_price = average_price
    def set_ingredients_by_id(self, recipe_id):
        conn = c.get_db_connection()
        list = conn.execute('''SELECT i.id AS id, recipe_id, sp.id AS product_id, sp.name AS product_name, weight, weight_type
                                    FROM ingredients i
                                    JOIN simpleProducts sp ON product_id = sp.id
                                    WHERE i.recipe_id=?''', (recipe_id,)).fetchall()
        for line in list:
            self.ingredients['id'].append(line['product_id'])
            self.ingredients['name'].append(line['product_name'])
            self.ingredients['weight'].append(line['weight'])
            self.ingredients['weight_type'].append(line['weight_type'])
        conn.close()
    def set_data_by_id(self, recipe_id):
        self.id = recipe_id
        conn = c.get_db_connection()
        data = conn.execute('SELECT * FROM recipes r WHERE r.id=?', (recipe_id,)).fetchone()
        self.name = data[1]
        self.recipe_photo = data[2]
        self.description = data[3].split('endofstep')#('\r\n')
        self.as_product = data[4]
        self.time = data[5]
        self.portions = data[6]
        self.portion_weight = data[7]
        self.kcal = data[8]
        self.average_price = data[9]
        self.set_ingredients_by_id(recipe_id)

        types = conn.execute('''SELECT rt.recipe_type, rt.type 
                                    FROM recipeTypes rt
                                    JOIN recipeTypesrecipes rtr ON rtr.recipe_type_id = rt.id
                                    WHERE rtr.recipe_id=?''',
                                    (recipe_id,)).fetchall()
        for type in types:
            if type[0]==2:
                self.meal_type = type[1]
            elif type[0]==1:
                self.dish_type = type[1]
            elif type[0]==3:
                self.kitchen_type = type[1]
            elif type[0]==4:
                self.other_type = type[1]
        conn.close()

    def get_recipe_id(self):
        conn = c.get_db_connection()
        id = conn.execute('SELECT id FROM recipes WHERE name=? AND description=?', (self.name, self.description)).fetchone()
        conn.close()
        return id[0]
    def get_product_id(self, product):
        conn = c.get_db_connection()
        id = conn.execute("""SELECT id FROM simpleProducts WHERE name=?""",
                                    (product,)).fetchone()
        if not id:
            conn.execute("INSERT INTO simpleProducts (name) VALUES (?)", (product,))
            id = conn.execute("""SELECT id FROM simpleProducts WHERE name=?""",
                                    (product,)).fetchone()
            self.ingredients['id'].append(id[0])
        conn.commit()
        conn.close()
        return id[0]
    def get_type_id(self, recipe_type, type):
        conn = c.get_db_connection()
        id = conn.execute('SELECT id FROM recipeTypes WHERE type=?',(type,)).fetchone()
        if not id:
            conn.execute('INSERT INTO recipeTypes (recipe_type, type) VALUES (?,?)', (recipe_type, type))
            id = conn.execute('SELECT id FROM recipeTypes WHERE type=?',(type,)).fetchone()
        conn.commit()
        conn.close()
        return id[0]
    def get_data_ids(self):
        data = {
            'recipe_id': None,
            'products_id': [],
            'dish': None,
            'meal': None,
            'kitchen': None,
            'other': None
        }
        if self.id:
            data['recipe_id'] = self.id
        else:
            # Insert into recipes table
            conn = c.get_db_connection()
            conn.execute('''INSERT INTO recipes (name, description, as_product, cooking_time, portions, portion_weight, kcal, user_id)
                            VALUES (?,?,?,?,?,?,?,?)''',
                            (self.name, self.description, self.as_product, self.time, self.portions, self.portion_weight, self.kcal, current_user.id))
            conn.commit()
            conn.close()
            data['recipe_id'] = self.get_recipe_id()
        for i in range(len(self.ingredients['name'])):
            data['products_id'].append(self.get_product_id(self.ingredients['name'][i]))
        if self.dish_type:
            data['dish'] = self.get_type_id(1, self.dish_type)
        if self.meal_type:
            data['meal'] = self.get_type_id(2, self.meal_type)
        if self.kitchen_type:
            data['kitchen'] = self.get_type_id(3, self.kitchen_type)
        if self.other_type:
            data['other'] = self.get_type_id(4, self.other_type)
        return data
    def get_recipe_data(self, recipe_id):
        conn = c.get_db_connection()
        data = conn.execute('''SELECT r.id AS id, u.user_id AS user_id, r.name AS name, rt.type AS type, r.descr AS descr
                                    FROM recipes r JOIN recipeTypes rt
                                    ON r.type_id = rt.id
                                    JOIN usersRecipes u
                                    ON u.rec_id = r.id
                                    WHERE r.id = ?''', (recipe_id,)).fetchone()
        conn.close()
        if data is None:
            c.abort(404)
        return data
    
    def create_recipe(self):
        data = self.get_data_ids()
        conn = c.get_db_connection()
        # Insert into ingredients table
        print(self.ingredients)
        print(data['products_id'])
        for i in range(len(data['products_id'])):
            conn.execute('''INSERT INTO ingredients (recipe_id, product_id, weight, weight_type) VALUES (?,?,?,?)''', (data['recipe_id'], data['products_id'][i], float(self.ingredients['weight'][i]), self.ingredients['weight_type'][i]))
        # Insert into recipeTypesRecipes table
        if self.dish_type:
            conn.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (data['recipe_id'], data['dish']))
        if self.meal_type:
            conn.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (data['recipe_id'], data['meal']))
        if self.kitchen_type:
            conn.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (data['recipe_id'], data['kitchen']))
        if self.other_type:
            conn.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (data['recipe_id'], data['other']))
        if not self.dish_type and not self.meal_type and not self.kitchen_type and not self.other_type:
            conn.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (data['recipe_id'], 1))
        # Insert into usersRecipes table
        conn.execute('''INSERT INTO usersRecipes (user_id, recipe_id) VALUES (?,?)''', (current_user.id, data['recipe_id']))
        conn.commit()
        conn.close()

    def edit_recipe(self):
        data = self.get_data_ids()
        conn = c.get_db_connection()
        # Update recipes table
        conn.execute('UPDATE recipes SET name=?, description=?, as_product=?, cooking_time=?, portions=?, portion_weight=?, kcal=?, user_id=? WHERE id=?',
                            (self.name, self.description, self.as_product, self.time, self.portions, self.portion_weight, self.kcal, current_user.id, self.id))
        # Delete all ingredients for this recipe
        conn.execute('DELETE FROM  ingredients WHERE recipe_id=?',(self.id,))
        # Update ingredients table
        for i in range(len(data['products_id'])):
            conn.execute('INSERT INTO ingredients (recipe_id, product_id, weight, weight_type) VALUES (?,?,?,?)',
                                (self.id, data['products_id'][i], float(self.ingredients['weight'][i]), self.ingredients['weight_type'][i]))
        # Delete all recipe types for this recipe
        conn.execute('DELETE FROM  recipeTypesRecipes WHERE recipe_id=?',(self.id,))
        # Update recipetypesRecipes table
        if self.dish_type:
            conn.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (self.id, data['dish']))
        if self.meal_type:
            conn.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (self.id, data['meal']))
        if self.kitchen_type:
            conn.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (self.id, data['kitchen']))
        if self.other_type:
            conn.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (self.id, data['other']))
        if not self.dish_type and not self.meal_type and not self.kitchen_type and not self.other_type:
            conn.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (self.id, 1))
        conn.commit()
        conn.close()
        
    def test_recipe(self):
        print(f"""      Recipe ID: {self.id}
        Recipe name: {self.name}
        As product: {self.as_product}
        Dish type: {self.dish_type}
        Meal type: {self.meal_type}
        Kitchen type: {self.kitchen_type}
        Other type: {self.other_type}
        Time: {self.time}
        Portionos: {self.portions}
        Portion weight: {self.portion_weight}
        Kcal: {self.kcal}
        
        Description: {self.description}""")
    

    def recipe_exist(self, recipe_name, ingredients, description, as_product):
        conn = c.get_db_connection()
        exist = conn.execute('''SELECT id FROM recipes
                                    WHERE name=? AND description=? AND as_product=?''', 
                                    (recipe_name, description, as_product)).fetchone()
        conn.close()
        return exist

class RecipeAct:
    def __init__(self, recipe_id=None):
        self.conn = c.get_db_connection()
        #self.types = self.conn.execute('SELECT * FROM recipeTypes WHERE id != 1').fetchall()
        #self.products = self.conn.execute('SELECT * FROM simpleProducts WHERE id != 1').fetchall()
        #self.r_products = self.conn.execute('SELECT * FROM recipes WHERE as_product=true').fetchall()
        #conn.close()
        self.recipe = Recipe()
        if recipe_id:
            self.recipe.set_data_by_id(recipe_id)
    def act(self, func):
        # Form handling
        if c.request.method == 'POST':
            recipe_name = c.request.form['r_name']
            dish_type = c.request.form['dishtype']
            ingredients = {
                'name':[],
                'weight':[],
                'weight_type':[]
            }
            for i in range(0,30):
                try:
                    name = "name_"+str(i)
                    weight = "weight_"+str(i)
                    weight_type = "weight-type_"+str(i)
                    # If name was filled in, then save this ingredient
                    if c.request.form[name] and c.request.form[weight] and c.request.form[weight_type]:
                        ingredients['name'].append(c.request.form[name].lower())
                        ingredients['weight'].append(c.request.form[weight])
                        ingredients['weight_type'].append(c.request.form[weight_type])
                except c.BadRequest:
                    pass
            #description = c.request.form['step_0']
            description = ""
            for i in range(0,30):
                try:
                    step = "step_"+str(i)
                    if c.request.form[step]:
                        description += c.request.form[step]
                        step = "step_"+str(i+1)
                        if i != 29 and c.request.form[step]:
                            description += "endofstep"
                    print(description)
                    print()
                except c.BadRequest:
                    pass
            print(description)
            try:
                as_product = int(c.request.form['recipe_as_product'])
            except c.BadRequest:
                as_product = None
            if recipe_name and ingredients['name'] and description:
                if not self.recipe.recipe_exist(recipe_name, ingredients, description, as_product) or self.recipe.id:
                    self.recipe.set_required_data(recipe_name, ingredients, description, as_product)
                    # Types
                    try:
                        meal_type = c.request.form['mealtype'].lower()
                        kitchen_type = c.request.form['kitchentype'].lower()
                        other_type = c.request.form['othertype'].lower()
                        self.recipe.set_types(meal_type, kitchen_type, other_type)
                    except c.BadRequest:
                        pass
                    # Secondary data
                    try:
                        #photo = c.request.form['photo']
                        #if photo:
                        #    self.recipe.set_photo(photo)
                        dish_type = c.request.form['dishtype'].lower()
                        if dish_type:
                            self.recipe.set_dish_type(dish_type)
                    except c.BadRequest:
                        pass
                    # Additional data
                    try:
                        portions = c.request.form['portions']
                        time = None #c.request.form['time']
                        portion_weight = None #c.request.form['portion_weight']
                        kcal = None #c.request.form['kcal']
                        #average_price
                        self.recipe.set_additional_data(time, portions, portion_weight, kcal)
                    except c.BadRequest:
                        pass
                    return func()
        return False
            
    def create(self):
        self.recipe.create_recipe()  
        return True
    def edit(self):
        self.recipe.edit_recipe()  
        return True
