import sqlite3

connection = sqlite3.connect('database.db')

with open('app/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.execute('INSERT INTO recipeTypes (id, type) VALUES (?, ?), (?, ?), (?, ?)',
                    (1, "Breakfast", 2, "Lunch", 3, "Dinner"))

connection.commit()
connection.close()