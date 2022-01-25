import sqlite3

connection = sqlite3.connect('database.db')

with open('app/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

recipeTypes = ["Завтрак", "Обед", "Ужин"]
connection.execute('INSERT INTO recipeTypes (id, type) VALUES (?, ?), (?, ?), (?, ?)',
                    (1, recipeTypes[0], 2, recipeTypes[1], 3, recipeTypes[2]))

connection.commit()
connection.close()