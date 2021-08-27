import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def run():
    """conn = get_db_connection()

    test = conn.execute('''SELECT r.id AS id, r.name AS name, rt.type AS type, r.descr AS descr
FROM recipes r JOIN recipeTypes rt
ON r.type_id = rt.id
WHERE r.id = ?''', (6,)).fetchone()

    print(test['type'])

    conn.commit()
    conn.close()"""
    test = []
    if test:
        print('Not empty')
    else:
        print('Empty')

run()
