import sqlite3

connection = sqlite3.connect('database.db')


with open('app/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

#cur.execute("INSERT INTO products (name, weight, price, shop) VALUES (?, ?, ?, ?)",
#            ('Молоко', 900, 42, 'Магнит')
#            )

#cur.execute("INSERT INTO recipes (name, type, descr) VALUES (?, ?, ?)",
#            ('Some1', 'Lunch', 'Description')
#            )

connection.commit()
connection.close()
