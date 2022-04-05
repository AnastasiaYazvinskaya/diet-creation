import app.connect as c
from flask_login import current_user

class Recipe:
    def __init__(self):
        self.id = None
        self.name = None            # Recipe name
        #self.recipe_type = "general"
        self.meal_type = None  # Recipe type
        self.kitchen_type = None
        self.dish_type = None
        self.other_type = None
        self.recipe_photo = None    # Photo of the dish
        self.ingredients = {
            'id': [],
            'name':[],
            'weight':[],
            'weight_type':[]
        }     # Recipe ingredients
        self.description = None     # Cooking description
        self.as_product = None
        self.time = None            # Cooking time
        self.portions = None        # Number of portions
        self.portion_weight = None  # Protion weight
        self.kcal = None            # Kcal
        self.average_price = None   # Average price of the 
        self.conn = c.get_db_connection() # connect to the database
        self.cur = self.conn.cursor()

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
        list = self.conn.execute('''SELECT i.id AS id, recipe_id, sp.name AS product_name, weight, weight_type
                                    FROM ingredients i
                                    JOIN simpleProducts sp ON product_id = sp.id
                                    WHERE i.recipe_id=?''', (recipe_id,)).fetchall()
        for line in list:
            self.ingredients['id'].append(line['id'])
            self.ingredients['name'].append(line['product_name'])
            self.ingredients['weight'].append(line['weight'])
            self.ingredients['weight_type'].append(line['weight_type'])
    def set_data_by_id(self, recipe_id):
        self.id = recipe_id
        data = self.conn.execute('SELECT * FROM recipes r WHERE r.id=?', (recipe_id,)).fetchone()
        self.name = data[1]
        self.recipe_photo = data[2]
        self.description = data[3]
        self.as_product = data[4]
        self.time = data[5]
        self.portions = data[6]
        self.portion_weight = data[7]
        self.kcal = data[8]
        self.average_price = data[9]
        self.set_ingredients_by_id(recipe_id)

        types = self.conn.execute('''SELECT rt.recipe_type, rt.type 
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

    def get_recipe_id(self):
        id = self.conn.execute('SELECT id FROM recipes WHERE name=? AND description=?', (self.name, self.description)).fetchone()
        return id[0]
    def get_product_id(self, product):
        id = self.conn.execute("""SELECT id FROM simpleProducts WHERE name=?""",
                                    (product,)).fetchone()
        if not id:
            self.cur.execute("INSERT INTO simpleProducts (name) VALUES (?)", (product,))
            id = self.conn.execute("""SELECT id FROM simpleProducts WHERE name=?""",
                                    (product,)).fetchone()
        self.conn.commit()
        return id[0]
    def get_type_id(self, recipe_type, type):
        id = self.conn.execute('SELECT id FROM recipeTypes WHERE type=?',(type,)).fetchone()
        if not id:
            self.cur.execute('INSERT INTO recipeTypes (recipe_type, type) VALUES (?,?)', (recipe_type, type))
            id = self.conn.execute('SELECT id FROM recipeTypes WHERE type=?',(type,)).fetchone()
        self.conn.commit()
        return id[0]
    def get_recipe_data(self, recipe_id):
        data = self.conn.execute('''SELECT r.id AS id, u.user_id AS user_id, r.name AS name, rt.type AS type, r.descr AS descr
                                    FROM recipes r JOIN recipeTypes rt
                                    ON r.type_id = rt.id
                                    JOIN usersRecipes u
                                    ON u.rec_id = r.id
                                    WHERE r.id = ?''', (recipe_id,)).fetchone()
        if data is None:
            c.abort(404)
        return data
    
    def create_recipe(self):
        # Insert into recipes table
        self.cur.execute('''INSERT INTO recipes (name, description, as_product, cooking_time, portions, portion_weight, kcal, user_id)
                            VALUES (?,?,?,?,?,?,?,?)''',
                            (self.name, self.description, self.as_product, self.time, self.portions, self.portion_weight, self.kcal, current_user.id))
        recipe_id = self.get_recipe_id()
        # Insert into ingredients table
        for i in range(len(self.ingredients['name'])):
            product_id = self.get_product_id(self.ingredients['name'][i]), float(self.ingredients['weight'][i]), self.ingredients['weight_type'][i]
            self.cur.execute('''INSERT INTO ingredients (recipe_id, product_id, weight, weight_type) VALUES (?,?,?,?)''', (recipe_id, product_id))
        # Insert into recipeTypesRecipes table
        if self.dish_type:
            type_id = self.get_type_id(1, self.dish_type)
            self.cur.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (recipe_id, type_id))
        if self.meal_type:
            type_id = self.get_type_id(2, self.meal_type)
            self.cur.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (recipe_id, type_id))
        if self.kitchen_type:
            type_id = self.get_type_id(3, self.kitchen_type)
            self.cur.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (recipe_id, type_id))
        if self.other_type:
            type_id = self.get_type_id(4, self.other_type)
            self.cur.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (recipe_id, type_id))
        if not self.dish_type and not self.meal_type and not self.kitchen_type and not self.other_type:
            self.cur.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (recipe_id, 1))
        # Insert into usersRecipes table
        self.cur.execute('''INSERT INTO usersRecipes (user_id, recipe_id) VALUES (?,?)''', (current_user.id, recipe_id))
        self.conn.commit()
        self.conn.close()

    def edit_recipe(self):
        # Update recipes table
        self.cur.execute('UPDATE recipes SET name=?, description=?, as_product=?, cooking_time=?, portions=?, portion_weight=?, kcal=?, user_id=? WHERE id=?',
                            (self.name, self.description, self.as_product, self.time, self.portions, self.portion_weight, self.kcal, current_user.id, self.id))
        # Delete all ingredients for this recipe
        self.cur.execute('DELETE FROM  ingredients WHERE recipe_id=?',(self.id,))
        # Update ingredients table
        for i in range(len(self.ingredients['id'])):
            product_id = self.get_product_id(self.ingredients['name'][i])
            self.cur.execute('INSERT INTO ingredients (recipe_id, product_id, weight, weight_type) VALUES (?,?,?,?)',
                                (self.id, product_id, float(self.ingredients['weight'][i]), self.ingredients['weight_type'][i]))
        # Delete all recipe types for this recipe
        self.cur.execute('DELETE FROM  recipeTypesRecipes WHERE recipe_id=?',(self.id,))
        # Update recipetypesRecipes table
        if self.dish_type:
            type_id = self.get_type_id(1, self.dish_type)
            self.cur.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (self.id, type_id))
        if self.meal_type:
            type_id = self.get_type_id(2, self.meal_type)
            self.cur.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (self.id, type_id))
        if self.kitchen_type:
            type_id = self.get_type_id(3, self.kitchen_type)
            self.cur.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (self.id, type_id))
        if self.other_type:
            type_id = self.get_type_id(4, self.other_type)
            self.cur.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (self.id, type_id))
        if not self.dish_type and not self.meal_type and not self.kitchen_type and not self.other_type:
            self.cur.execute('''INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?)''', (self.id, 1))
        self.conn.commit()
        self.conn.close()

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
        exist = self.conn.execute('''SELECT id FROM recipes
                                    WHERE name=? AND description=? AND as_product=?''', 
                                    (recipe_name, description, as_product)).fetchone()
        return exist
