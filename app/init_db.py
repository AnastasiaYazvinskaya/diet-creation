import sqlite3

connection = sqlite3.connect('database.db')

with open('app/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

recipeTypes = ["Завтрак", "Обед", "Ужин"]
connection.execute('INSERT INTO recipeTypes (id, type) VALUES (?, ?), (?, ?), (?, ?)',
                    (1, recipeTypes[0], 2, recipeTypes[1], 3, recipeTypes[2]))

connection.execute('INSERT INTO shops (name) VALUES (?)', ("Магнит",))
connection.execute('''INSERT INTO products (id, name, weight, weightType, price, shop_id) VALUES
                      (?,?,?,?,?,?), (?,?,?,?,?,?), (?,?,?,?,?,?), (?,?,?,?,?,?), (?,?,?,?,?,?),
                      (?,?,?,?,?,?), (?,?,?,?,?,?), (?,?,?,?,?,?), (?,?,?,?,?,?), (?,?,?,?,?,?)''',
                      (1, "Мандарины", 1, "кг", 68.99, 2, 
                       2, "Фарш домашний натуральный", 1, "кг", 329.98, 2, 
                       3, "Картофель для варки", 3, "кг", 239.99, 2, 
                       4, "Крупа Гречневая", 800, "г", 76.98, 2, 
                       5, "Пельмени Классические", 1, "кг", 125.88, 2, 
                       6, "Лук репчатый", 1, "кг", 18.99, 2, 
                       7, "Морковь", 1, "кг", 29.49, 2, 
                       8, "Яйцо куриное С1", 15, "шт", 114.99, 2, 
                       9, "Яблоки Новый урожай", 1, "кг", 79.38, 2, 
                       10, "Сердечки куриные охл", 1, "кг", 349.99, 2))

connection.commit()
connection.close()