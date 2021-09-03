import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def run():
    conn = get_db_connection()

    test = conn.execute('''SELECT * FROM products''').fetchall()

    for prod in test:
        print(f"{prod[0]}. {prod[2]} ({prod[3]}) - {prod[4]} [{prod[5]}]")


    conn.commit()
    conn.close()
    print(test)

run()
