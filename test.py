import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def run():
    conn = get_db_connection()

    test=conn.execute("SELECT * FROM recipeTypes").fetchall()
    print(test)
    for item in test:
        print(f"{item[0]}. {item[1]}")
    
    conn.commit()
    conn.close()

run()