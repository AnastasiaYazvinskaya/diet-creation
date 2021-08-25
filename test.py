import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def run():
    """conn = get_db_connection()

    rec_id = conn.execute('SELECT * FROM recipes').fetchall()

    print (rec_id)

    conn.commit()
    conn.close()"""
    while True:
        try:
            integ1 = int(input("Integer1: "))
            try:
                integ2 = int(input("Integer2: "))
            except ValueError:
                print("integ2 error")
        except ValueError:
            print("integ1 error")
    

run()
