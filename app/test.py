import app.connect as c
from app import app

# test
@app.route('/test', methods=('GET', 'POST'))
def test():
    conn = c.get_db_connection()
    recipes = conn.execute('''SELECT r.id AS id, r.name AS name, rt.type AS type, r.descr AS descr
    FROM recipes r JOIN recipeTypes rt
    ON r.type_id = rt.id''').fetchall()
    types = conn.execute('SELECT * FROM recipeTypes').fetchall()
    return c.render_template('test.html', recipes=recipes, types=types, menu_id=0)
 
@app.route("/updateList",methods=('GET', 'POST'))
def updateList():
    conn = c.get_db_connection()
    if c.request.method == 'POST':    
        getorder = c.request.form['order']
        orders = getorder.split(",")
        print(orders)
        #for index in range(0, len(orders), 7):
        #    for i in range(7):
        #        print(f"index={index}, orders[index]={orders[index]}, index//7={index//7}")
        #        conn.execute("INSERT INTO meal (id, recipe, weekday_id) VALUES (?, ?, ?)",
        #                 (index, orders[index], index//7))
        #        index += 1
        #order = getorder.split(",", number_of_rows)
        #count=0   
        #for value in order:
        #    count +=1
        #    print(count)                       
        #    conn.execute("UPDATE recipes SET listorder = ? WHERE id = ? ",
        #                 (count, value))
        #    conn.commit()       
        #conn.close()
    return c.jsonify('Successfully Updated')

#Tests
@app.route('/tests')
def tests():
    conn = c.get_db_connection()
    recipes = conn.execute('''SELECT * FROM recipes''').fetchall()
    #types = conn.execute('SELECT * FROM recipeTypes').fetchall()
    return c.render_template('tests.html', recipes=recipes)