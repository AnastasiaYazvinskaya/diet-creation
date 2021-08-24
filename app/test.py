import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def run():
    conn = get_db_connection()
    #conn.execute('INSERT INTO recipes (name, type, descr) VALUES (?, ?, ?)',
    #            (r_name, type, descr))
    conn.execute('SELECT id FROM recipes WHERE name=?',
                        ('Some1',))
    rec_id = conn.fetchall()
    #rec_id = rec_id[0]
    #for i in range(len(ingreds['names'])):
    #    conn.execute('INSERT INTO ingredients (rec_id, prod_name, weight) VALUES (?, ?, ?)',
    #                (rec_id , ingreds['names'][i], ingreds['weights'][i]))
    conn.commit()
    conn.close()

    return rec_id

print(run())
