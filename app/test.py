import app.connect as c
from app import app

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
# test
@app.route('/test<int:menu_id>', methods=('GET', 'POST'))
def test(menu_id):
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
    return c.render_template('test.html', menus=menus, menu=menu, menu_info=menu_info, weeks=weeks, products=products, price=total_price)
 
@app.route("/create_list",methods=('GET', 'POST'))
def createList():
    conn = c.get_db_connection()
    if c.request.method == 'POST':    
        getorder = c.request.form['data']
        orders = getorder.split(",") # 0-menu_id, 1-weeks_amount, 2-5-choosen_weeks
        print(f"orders={orders}")
        week = {
            'type': [1, 2, 3, 4],
            'amount': [0, 0, 0, 0],
            'finish': ""
        }
        for i in range(2, 6):
            if i < len(orders):
                print(f"orders[i] exist: {int(orders[i]) in week['type']}")
                if int(orders[i]) in week['type']:
                    week['amount'][week['type'].index(int(orders[i]))] += 1
        for i in range(len(week['amount'])):
            if week['amount'][i] != 0:
                if len(week['finish']) != 0:
                    week['finish'] += ", "
                week['finish'] += str(week['type'][i])
        print(f"week[amount]={week['amount']}    week[finish]={week['finish']}")
        print(f"menu_id={orders[0]}    num_of_weeks={orders[1]}    week={week['finish']}")
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
                        print(product['price'])
                        data['price'].append(product['price']*week['amount'][i])
                        data['total_price'] += product['price']*week['amount'][i]
            
    return c.jsonify(data)

#Tests
@app.route('/tests')
def tests():
    conn = c.get_db_connection()
    recipes = conn.execute('''SELECT * FROM recipes''').fetchall()
    #types = conn.execute('SELECT * FROM recipeTypes').fetchall()
    return c.render_template('tests.html', recipes=recipes)