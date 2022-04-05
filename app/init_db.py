import sqlite3

connection = sqlite3.connect('database.db')

with open('app/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
restart = False

if not connection.execute('SELECT id FROM simpleProducts').fetchall() or restart:
    # Insert basic test simple products
    connection.execute('''INSERT INTO simpleProducts (id, name) VALUES
                        (?,?), (?,?), (?,?)''',
                        (2, "Картофель", 3, "Мандарин", 4, "Фарш"))

if not connection.execute('SELECT id FROM products').fetchall() or restart:
    # Insert basic test product's types
    connection.execute('INSERT INTO productTypes (id, type) VALUES (?,?), (?,?), (?,?)',
                        (2, "Фрукты", 3, "Овощи", 4, "Напитки"))
    # Insert test shop
    connection.execute('INSERT INTO shops (id, name) VALUES (?,?)', (2, "Магнит"))
    # Insert test products
    connection.execute('''INSERT INTO products (id, name, weight, weight_type, user_id, product_type_id) VALUES
                        (?,?,?,?,?,?), (?,?,?,?,?,?), (?,?,?,?,?,?), (?,?,?,?,?,?), (?,?,?,?,?,?),
                        (?,?,?,?,?,?), (?,?,?,?,?,?), (?,?,?,?,?,?), (?,?,?,?,?,?), (?,?,?,?,?,?)''',
                        (1, "Мандарины", 1, "кг", 4, 2,
                        2, "Фарш домашний натуральный", 1, "кг", 4, 1,
                        3, "Картофель для варки", 3, "кг", 4, 1, 
                        4, "Крупа Гречневая", 800, "г", 4, 1, 
                        5, "Пельмени Классические", 1, "кг", 4, 1, 
                        6, "Лук репчатый", 1, "кг", 4, 1, 
                        7, "Морковь", 1, "кг", 4, 3, 
                        8, "Яйцо куриное С1", 15, "шт", 4, 1, 
                        9, "Яблоки Новый урожай", 1, "кг", 4, 2, 
                        10, "Сердечки куриные охл", 1, "кг", 4, 1))
    connection.execute('''INSERT INTO shopsProducts (shop_id, product_id) VALUES
                        (?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?)''',
                        (2,1, 2,2, 2,3, 2,4, 2,5, 2,6, 2,7, 2,8, 2,9, 2,10))
    connection.execute('''INSERT INTO productPrice (product_id, price) VALUES
                        (?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?)''',
                        (1,68.99, 2,329.98, 3,239.99, 4,76.98, 5,125.88, 6,18.99, 7,29.49, 8,114.99, 9,79.38, 10,349.99))
    connection.execute('''INSERT INTO usersProducts (user_id, product_id) VALUES
                        (?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?)''',
                        (4,1, 4,2, 4,3, 4,4, 4,5, 4,6, 4,7, 4,8, 4,9, 4,10))
if not connection.execute('SELECT id FROM recipes').fetchall() or restart:
    # Insert basic recipe's types
    connection.execute('INSERT INTO recipeTypes (recipe_type, type) VALUES (?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?)',
                        (2,"завтрак", 2,"перекус", 2,"обед", 2,"полдник", 2,"ужин", 1,"суп", 1,"второе блюдо", 1,"десерт", 1,"закуска", 1,"напиток", 1,"гарнир"))

    connection.execute('INSERT INTO recipes (name, description, user_id) VALUES (?,?,?)',
                        ("Пюре", "Сварить картофель, слить лишнюю воду и размять его. Можно добавить молока и масла.", 4))
    connection.execute('INSERT INTO recipeTypesRecipes (recipe_id, recipe_type_id) VALUES (?,?), (?,?)',
                        (1, 6, 1, 12))
    connection.execute('INSERT INTO ingredients (recipe_id, product_id, weight, weight_type) VALUES (?,?,?,?)',
                        (1, 2, 150, "г"))
    connection.execute('INSERT INTO usersRecipes (user_id, recipe_id) VALUES (?,?)',
                        (4, 1))

connection.commit()
connection.close()