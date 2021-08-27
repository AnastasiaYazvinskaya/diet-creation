import sqlite3

connection = sqlite3.connect('database.db')


with open('app/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO shops (name) VALUES (?)",
            ('Магнит',)
            )

cur.execute("INSERT INTO products (name, weight, price, shop_id) VALUES (?, ?, ?, ?)",
            ('Молоко', 900, 42, 1)
            )

cur.execute("INSERT INTO recipeTypes (type) VALUES (?)",
            ('Завтрак',)
            )

cur.execute("INSERT INTO recipes (name, type_id, descr) VALUES (?, ?, ?)",
            ('Овсяная каша', 1, 'Сварить кашу')
            )

cur.execute("INSERT INTO ingredients (rec_id, prod_name, weight) VALUES (?, ?, ?)",
            (1, 'Молоко', 100)
            )

connection.commit()
connection.close()
