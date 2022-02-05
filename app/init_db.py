import sqlite3
from werkzeug.security import generate_password_hash

connection2 = sqlite3.connect('usersdb.db')
connection = sqlite3.connect('database.db')

with open('app/usersSchema.sql') as f:
    connection2.executescript(f.read())
with open('app/schema.sql') as f:
    connection.executescript(f.read())

cur2 = connection2.cursor()
cur = connection.cursor()

connection2.execute('''INSERT INTO user_icons (icon) VALUES
                      (?),(?),(?),(?)''',
                      ("../static/images/user-3.svg", "../static/images/user-4.svg", "../static/images/user-5.svg", "../static/images/user-6.svg"))

connection2.execute('INSERT INTO users (username, email, password, icon_id) VALUES (?,?,?,?)',
                    ("TestUser", "diet.creation.sendler@gmail.com", generate_password_hash("TestUserCreated001"), 1))

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
connection.execute('''INSERT INTO usersProducts (user_id, prod_id) VALUES
                      (?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?)''',
                      (1,1, 1,2, 1,3, 1,4, 1,5, 1,6, 1,7, 1,8, 1,9, 1,10))

connection2.commit()
connection2.close()
connection.commit()
connection.close()