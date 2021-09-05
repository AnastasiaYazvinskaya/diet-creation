import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def run():
    conn = get_db_connection()

    recipe = conn.execute('''SELECT r.id AS id, r.name AS name, rt.type AS type, r.descr AS descr
    FROM recipes r JOIN recipeTypes rt
    ON r.type_id = rt.id
    WHERE r.name = ?''', ('Картофельное пюре',)).fetchone()
    ingredients = conn.execute('''SELECT * FROM ingredients
    WHERE rec_id=?''', (recipe['id'],)).fetchall()

    data = {'r_name': recipe['name'], 'type': recipe['type'], 'descr': recipe['descr'],
            'ingreds': {'id': [],
                        'names': [],
                        'weights': []}
            }
    for ingred in ingredients:
        data['ingreds']['id'].append(ingred['id'])
        data['ingreds']['names'].append(ingred['prod_name'])
        data['ingreds']['weights'].append(ingred['weight'])
    
    print(data['ingreds']['names'])

    for i in range(len(data['ingreds']['id'])):
        ingred_exist = conn.execute('SELECT * FROM ingredients WHERE prod_name=?',
                                            (data['ingreds']['names'][i],)).fetchone()
        if ingred_exist:
            ingred_id = ingred_exist[0]
            print(ingred_id)
            conn.execute('UPDATE ingredients SET prod_name=?, weight=?'
                        'WHERE id=?',
                        (data['ingreds']['names'][i], data['ingreds']['weights'][i], ingred_id))
        else:
            print('I do not find it')
            conn.execute('INSERT INTO ingredients VALUES (rec_id, prod_name, weight)',
                        (rec_id, data['ingreds']['names'][i], data['ingreds']['weights'][i]))

    test = conn.execute('SELECT * FROM ingredients WHERE prod_name=?',('Вода',)).fetchall()
    for i in test:
        for j in i:
            print(j)
        print()
    
    conn.commit()
    conn.close()
    

run()
