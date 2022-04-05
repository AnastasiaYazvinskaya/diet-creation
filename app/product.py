import app.connect as c
from flask_login import current_user
class Product:
    def __init__(self):
        self.name = None
        self.weight = None
        self.weight_type = None
        self.barcode = None
        self.product_type = "cook"
        self.shop = "unknown"
        self.price = None
        self.conn = c.get_db_connection() # connect to the database

    def set_required_data(self, name, weight, weight_type):
        self.name = name
        self.weight = weight
        self.weight_type = weight_type
    
    def set_barcode(self, barcode):
        self.barcode = barcode

    def set_type_data(self, product_type="cook"):
        self.product_type = product_type

    def set_additional_data(self, shop="unknown", price=None):
        self.shop = shop
        self.price = price

    def set_data_by_id(self, shop_product_id):
        data = self.conn.execute('''SELECT p.name, weight, weight_type, pt.type, s.name, pp.price
                               FROM shopsProducts sp
                               JOIN shops s ON sp.shop_id=s.id
                               JOIN product p ON sp.product_id=p.id
                               JOIN productPrice pp ON sp.id=pp.product_id
                               WHERE sp.id=?''', (shop_product_id))
        self.name = data[0]
        self.weight = data[1]
        self.weight_type = data[2]
        self.product_type = data[3]
        self.shop = data[4]
        self.price = data[5]

    def get_product_type_id(self):
        id = self.conn.execute('SELECT id FROM productTypes WHERE type=?', (self.product_type,)).fetchone()
        if not id: # if type is not found
            self.conn.execute('INSERT INTO productTypes (type) VALUES (?)', (self.product_type,))
            id = self.conn.execute('SELECT id FROM productTypes WHERE type=?', (self.product_type,)).fetchone()
        return id[0]
    
    def get_product_id(self):
        id = self.conn.execute('SELECT id FROM products WHERE name=? AND weight=? AND weight_type=? AND product_type_id=?', (self.name, self.weight, self.weight_type, self.get_product_type_id())).fetchone()
        return id[0]

    def get_shop_id(self):
        id = self.conn.execute('SELECT id FROM shops WHERE name=?', (self.shop,)).fetchone()
        if not id: # if type is not found
            self.conn.execute('INSERT INTO shops (name) VALUES (?)', (self.shop,))
            id = self.conn.execute('SELECT id FROM shops WHERE name=?', (self.shop,)).fetchone()
        return id[0]

    def get_shop_product_id(self):
        id = self.conn.execute('SELECT id FROM shopsProducts WHERE shop_id=? AND product_id=?', (self.get_shop_id(), self.get_product_id())).fetchone()
        return id[0]

    def get_shop_product_data(self, shop_product_id):
        data = self.conn.execute('''SELECT sp.id AS id, p.id AS product_id, p.name AS name, p.weight AS weight, p.weight_type AS weight_type, pp.price AS price, s.name AS shop, p.product_type_id AS product_type_id
                              FROM products p JOIN shopsProducts sp
                              ON p.id = sp.product_id
                              JOIN shops s
                              ON s.id = sp.shop_id
                              JOIN productPrice pp
                              ON pp.product_id = sp.id
                              JOIN usersProducts u
                              ON u.product_id = sp.id
                              WHERE sp.id = ? AND u.user_id=?''', (shop_product_id, current_user.id)).fetchone()
        if data is None:
            c.abort(404)
        return data

    def create_product(self):
        # Insert into products table
        self.conn.execute('''INSERT INTO products
                        (name, weight, weight_type, user_id, product_type_id)
                        VALUES (?,?,?,?,?)''',
                        (self.name, self.weight, self.weight_type, current_user.id, self.get_product_type_id()))
        # Insert into productsSimpleProducts table
        #self.conn.execute('''INSERT INTO 
        #                ()
        #                VALUES ()''',
        #                ())
        # Insert into shopsProducts table
        self.conn.execute('''INSERT INTO shopsProducts
                        (shop_id, product_id)
                        VALUES (?,?)''',
                        (self.get_shop_id(), self.get_product_id()))
        # Insert into productPrice table
        self.conn.execute('''INSERT INTO productPrice
                        (product_id, price)
                        VALUES (?,?)''',
                        (self.get_shop_product_id(), self.price))
        # Insert into usersProducts table
        self.conn.execute('''INSERT INTO usersProducts
                        (user_id, product_id)
                        VALUES (?,?)''',
                        (current_user.id, self.get_shop_product_id()))
        self.conn.commit()
        self.conn.close()

    def edit_product(self):
        pass

    def product_exist(self, name, weight, weight_type):
        exist = self.conn.execute('SELECT id FROM products WHERE name=? AND weight=? AND weight_type=?', (name, weight, weight_type)).fetchall()
        return exist