import app.connect as c
from app import app
# Menu
class Menu:
    def __init__(self):
        self.id = 0
        self.name = ''
        self.menu = {
            'breakfast':[],
            'lunch': [],
            'dinner': []
        }
# Class for creating and editing menu information
class MenuAct:
    def __init__(self, menu_id=None):
        self.conn = c.get_db_connection()
        
        self.data = Menu()
        if menu_id:
            self.data.id = menu_id
        else:
            menu_list = self.conn.execute("SELECT id FROM menu").fetchall()
            if menu_list:
                self.data.id = menu_list[-1][0]+1
            else:
                self.data.id = 1
    def act(self, func):
        finish = False
        if c.request.method == 'POST':
            finish = func(self.data.id)
        return finish
    def create(self, menu_id):
        # Create new menu
        self.conn.execute('INSERT INTO menu (id, menu_name) VALUES (?, ?)',
                            (menu_id, self.data.name))
        # Create new menu info
        for value in self.data.menu:
            for recipe in self.data.menu[value]:
                rec_id = self.conn.execute('SELECT id FROM recipes WHERE name=?', (recipe[0],)).fetchone()
                self.conn.execute('INSERT INTO meal (rec_id, weekday_id, week, menu_id, type, place) VALUES (?, ?, ?, ?, ?, ?)',
                                (rec_id[0], int(recipe[1]), int(recipe[2]), menu_id, int(recipe[3]), int(recipe[4])))
        self.conn.commit()
        self.conn.close()
        return True
    def edit(self, menu_id):
        # Update menu (menu)
        self.conn.execute('UPDATE menu SET menu_name=? WHERE id=?',
                            (self.data.name, menu_id))
        # Update menu info (meal)
        for key in self.data.menu:
            for recipe in self.data.menu[key]:
                rec_id = self.conn.execute('SELECT id FROM recipes WHERE name=?', (recipe[0],)).fetchone()
                rec_exist = self.conn.execute('SELECT * FROM meal WHERE weekday_id=? AND week=? AND menu_id=? AND type=? AND place=?',
                                                (int(recipe[1]), int(recipe[2]), menu_id, int(recipe[3]), int(recipe[4]))).fetchone()
                if rec_exist:
                    self.conn.execute('UPDATE meal SET rec_id=? WHERE id=?', (rec_id[0], rec_exist[0]))
                else:
                    self.conn.execute('INSERT INTO meal (rec_id, weekday_id, week, menu_id, type, place) VALUES (?, ?, ?, ?, ?, ?)',
                                      (rec_id[0], int(recipe[1]), int(recipe[2]), menu_id, int(recipe[3]), int(recipe[4])))
        self.conn.commit()
        self.conn.close()
        return True
# Get menu information by id (id, name)
def get_menu(menu_id):
    conn = c.get_db_connection()
    menu = conn.execute('SELECT * FROM menu m WHERE m.id = ?', (menu_id,)).fetchone()
    conn.close()
    if menu is None:
        c.abort(404)
    return menu
def get_weeks(info):
    weeks = [ info[0]['week'] ]
    new = ''
    for row in info:
        for i in range(len(weeks)):
            if row['week'] != weeks[i]:
                new = row['week']
            else:
                new = ''
                break
            if i == len(weeks)-1 and new != '':
                weeks.append(new)
    return weeks

# List of menu page (open)
@app.route('/menus')
def menus():
    conn = c.get_db_connection()
    menus = conn.execute('SELECT * FROM menu').fetchall()
    conn.close()
    return c.render_template('menus.html', menus=menus)
# Menu information page (open)
@app.route('/menu<int:menu_id>')
def menu(menu_id):
    menu = get_menu(menu_id)
    conn = c.get_db_connection()
    menus = conn.execute("SELECT * FROM menu").fetchall()
    menu_info = conn.execute("""SELECT m.id AS id, r.name AS recipe, m.weekday_id AS weekday_id, m.week AS week, m.menu_id AS menu_id, m.type AS type, m.place AS place, m.rec_id AS rec_id
                                FROM meal m JOIN recipes r  ON m.rec_id = r.id WHERE m.menu_id=?""", (menu_id,)).fetchall()
    weeks = get_weeks(menu_info)
    products = conn.execute("""SELECT m.week AS week, m.rec_id AS rec_id, p.id AS prod_id, p.name AS prod_name, SUM(i.weight) AS weight, 
                                p.price*SUM(i.weight)/p.weight AS price, s.name AS shop_name
                                FROM meal m JOIN ingredients i ON m.rec_id=i.rec_id
                                JOIN products p ON i.prod_id=p.id
                                JOIN shops s ON p.shop_id=s.id
                                WHERE m.menu_id=?
                                GROUP BY m.week, p.id""", (menu_id,)).fetchall()
    total_price = [0, 0, 0, 0]
    for product in products:
        if product['week'] == 1:
            total_price[0] += product['price']
        elif product['week'] == 2:
            total_price[1] += product['price']
        elif product['week'] == 3:
            total_price[2] += product['price']
        elif product['week'] == 4:
            total_price[3] += product['price']
    conn.close()
    return c.render_template('menu.html', menus=menus, menu=menu, menu_info=menu_info, weeks=weeks, products=products, price=total_price)
# Create menu
@app.route('/create_menu', methods=('GET', 'POST'))
def create_m():
    conn = c.get_db_connection()
    recipes = conn.execute('''SELECT r.id AS id, r.name AS name, rt.type AS type, r.descr AS descr
            FROM recipes r JOIN recipeTypes rt
            ON r.type_id = rt.id''').fetchall()
    types = conn.execute('SELECT * FROM recipeTypes').fetchall()
    return c.render_template('create_m.html', recipes=recipes, types=types)
# Edit menu
@app.route('/<int:id>_menu_edit', methods=('GET', 'POST'))
def edit_m(id):
    conn = c.get_db_connection()
    recipes = conn.execute('''SELECT r.id AS id, r.name AS name, rt.type AS type, r.descr AS descr
            FROM recipes r JOIN recipeTypes rt
            ON r.type_id = rt.id''').fetchall()
    types = conn.execute('SELECT * FROM recipeTypes').fetchall()
    menu = get_menu(id)
    menu_info = conn.execute("""SELECT m.id AS id, r.name AS recipe, m.weekday_id AS weekday_id, m.week AS week, m.menu_id AS menu_id, m.type AS type, m.place AS place, m.rec_id AS rec_id
                                FROM meal m JOIN recipes r  ON m.rec_id = r.id WHERE m.menu_id = ?""", (id,)).fetchall()
    weeks = get_weeks(menu_info)
    return c.render_template('edit_m.html', recipes=recipes, types=types, menu=menu, menu_info=menu_info, weeks=weeks)
# Delete menu
@app.route('/<int:id>/delete_menu', methods=('POST',))
def delete_m(id):
    menu = get_menu(id)
    conn = c.get_db_connection()
    conn.execute('DELETE FROM menu WHERE id = ?', (id,))
    conn.execute('DELETE FROM meal WHERE menu_id=?', (id,))
    conn.commit()
    conn.close()
    c.flash('"{}" was successfully deleted!'.format(menu['menu_name']))
    return c.redirect(c.url_for('menus'))

@app.route("/update_menu",methods=('GET', 'POST'))
def update_m():
    finish = ""
    if c.request.method == 'POST':
        getorder = c.request.form['data']
        orders = getorder.split(",")
        menuAct = MenuAct() # MenuAct(id)
        # Menu id
        if orders[0].isnumeric():
            menuAct.data.id = int(orders[0])
            orders.pop(0)
        # Menu name
        if len(orders) % 5 == 2:
            menuAct.data.name = orders[0]
            orders.pop(0)
        else:
            menuAct.data.name = "New Menu №" + str(menuAct.data.id)
        # Act with menu
        act = orders[0]
        orders.pop(0)
        # Meal's sorting
        for i in range(0, len(orders), 5):
            if orders[i+3] == '1':
                menuAct.data.menu['breakfast'].append([orders[i], int(orders[i+1]), int(orders[i+2]), int(orders[i+3]), int(orders[i+4])])
            elif orders[i+3] == '2':
                menuAct.data.menu['lunch'].append([orders[i], int(orders[i+1]), int(orders[i+2]), int(orders[i+3]), int(orders[i+4])])
            elif orders[i+3] == '3':
                menuAct.data.menu['dinner'].append([orders[i], int(orders[i+1]), int(orders[i+2]), int(orders[i+3]), int(orders[i+4])])
        if menuAct.data.menu['breakfast'] or menuAct.data.menu['lunch'] or menuAct.data.menu['dinner']:
            if act == "create":
                if menuAct.act(menuAct.create):
                    finish = c.url_for('menu', menu_id=menuAct.data.id)
            elif act == "edit":
                if menuAct.act(menuAct.edit):
                    finish = c.url_for('menu', menu_id=menuAct.data.id)
    return finish


@app.route("/create_list",methods=('GET', 'POST'))
def createList():
    conn = c.get_db_connection()
    if c.request.method == 'POST':    
        getorder = c.request.form['data']
        orders = getorder.split(",") # 0-menu_id, 1-weeks_amount, 2-5-choosen_weeks
        #print(f"orders={orders}")
        week = {
            'type': [1, 2, 3, 4],
            'amount': [0, 0, 0, 0],
            'finish': ""
        }
        for i in range(2, 6):
            if i < len(orders):
                #print(f"orders[i] exist: {int(orders[i]) in week['type']}")
                if int(orders[i]) in week['type']:
                    week['amount'][week['type'].index(int(orders[i]))] += 1
        for i in range(len(week['amount'])):
            if week['amount'][i] != 0:
                if len(week['finish']) != 0:
                    week['finish'] += ", "
                week['finish'] += str(week['type'][i])
        #print(f"week[amount]={week['amount']}    week[finish]={week['finish']}")
        #print(f"menu_id={orders[0]}    num_of_weeks={orders[1]}    week={week['finish']}")
        data = {
            'total_weeks': len(get_weeks(conn.execute("SELECT id, week FROM meal WHERE menu_id=?", (int(orders[0]),)).fetchall())),
            'weeks': int(orders[1]),
            'week': week['finish'],
            'rec_id': [],
            'prod_id': [],
            'prod_name': [],
            'weight': [],
            'price': [],
            'shop_name': [],
            'total_price': 0,
            'num': 0
        }
        if week['finish'] != "":
            products = conn.execute("""SELECT m.week AS week, m.rec_id AS rec_id, p.id AS prod_id, p.name AS prod_name, SUM(i.weight) AS weight, 
                                    p.price*SUM(i.weight)/p.weight AS price, s.name AS shop_name
                                    FROM meal m JOIN ingredients i ON m.rec_id=i.rec_id
                                    JOIN products p ON i.prod_id=p.id
                                    JOIN shops s ON p.shop_id=s.id
                                    WHERE m.menu_id=? AND m.week IN ("""+week['finish']+""")
                                    GROUP BY p.id""", (int(orders[0]),)).fetchall()
            data['num'] = len(products)
            for product in products:
                data['rec_id'].append(product['rec_id'])
                data['prod_id'].append(product['prod_id'])
                data['prod_name'].append(product['prod_name'])
                data['shop_name'].append(product['shop_name'])
                for i in range(len(week['amount'])):
                    if product['week'] == i+1:
                        data['weight'].append(product['weight']*week['amount'][i])
                        #print(product['price'])
                        data['price'].append(product['price']*week['amount'][i])
                        data['total_price'] += product['price']*week['amount'][i]
            
    return c.jsonify(data)