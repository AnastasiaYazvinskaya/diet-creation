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
    weeks = []
    weeks.append(info[0][3])
    for row in info:
        if row[3] != weeks[0]:
            weeks.append(row[3])
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
    conn.close()
    return c.render_template('menu.html', menus=menus, menu=menu, menu_info=menu_info, weeks=weeks)
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
                    finish = c.url_for('menus')
            elif act == "edit":
                if menuAct.act(menuAct.edit):
                    finish = c.url_for('menus')
    return finish
