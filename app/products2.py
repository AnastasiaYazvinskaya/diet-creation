import app.connect as c
from app import app
from flask_login import login_required, current_user

#import cv2
#from pyzbar import pyzbar
#from pyzbar.pyzbar import decode

# Class to create and edit product information
class ProductAct:
    def __init__(self, sp_id=None):
        self.sp_id = sp_id # shopProduct.id
        self.conn = c.get_db_connection() # connect to the database
        self.shops = self.conn.execute('SELECT * FROM shops').fetchall() # list of shops
        self.data = {'name': '', 'weight': '', 'weight_type': '', 'price': '', 'shop': 'unknown', 'product_type': 1, 'checked': False} # Save data
        self.prod_exist = None #
        if sp_id: # If edit product get its data
            product = get_product(self.sp_id) #(shopProduct.id, product_id, name, weight, weight_type, price, shop, product_type_id)
            self.data['name'] = product['name']
            self.data['weight'] = product['weight']
            self.data['weight_type'] = product['weight_type']
            self.data['price'] = product['price']
            self.data['shop'] = product['shop']
            self.data['product_type_id'] = product['product_type_id']
            if product['product_type_id'] != 1:
                self.data['checked'] = True
    def act(self, func):
        finish = False
        new = ''
        if c.request.method == 'POST':
            self.data['name'] = c.request.form['name'] # REQUIRED
            self.data['weight'] = c.request.form['weight'] # REQUIRED
            self.data['weight-type'] = c.request.form['weight-type'] # REQUIRED
            self.data['price'] = c.request.form['price'] # ADDITIONAL
            self.data['shop'] = c.request.form['shop'] # ADDITIONAL (GOES WITH PRICE)
            # (HERE) Checking for the presence of the same product
            self.prod_exist = self.conn.execute('''SELECT p.id AS id, p.name AS name, weight, weight_type, price, s.name AS shop
                                         FROM products p JOIN shops s
                                         ON p.shop_id = s.id
                                         WHERE p.name=? AND s.name=?''',
                                        (self.data['name'], self.data['shop'])).fetchall()
            try:
                if self.prod_exist:
                    new = c.request.form['exist'] # id or 'new'
                else:
                    new = 'new'
            except c.BadRequest:
                pass
            # If one of the REQUIRED field is empty then refresh page with saving data in the fields
            if not self.data['name'] or not self.data['weight'] or not self.data['weight-type']:
                c.flash('Name and weight information is requered!')
            elif new == 'new' or (new == '' and (not len(self.prod_exist) or len(self.prod_exist)==1 and self.prod_exist[0]['id']==self.sp_id)):
                if self.data['shop']:
                    shop_exist = self.conn.execute('SELECT id FROM shops WHERE name=?',
                                                (self.data['shop'],)).fetchone()
                    if not shop_exist:
                        add = self.conn.execute('INSERT INTO shops (name) VALUES (?)',
                                            (self.data['shop'],))
                    shop_id = self.conn.execute('SELECT id FROM shops WHERE name=?',
                                            (self.data['shop'],)).fetchone()
                    finish = func(shop_id[0])
                else:
                    finish = func()
            elif new.isnumeric():
                finish = True
        return finish
    def create(self, shop_id=1):
        if c.request.form['product_as_recipe']:
            self.data['product_type'] = c.request.form['ptype']
            type_exist = self.conn.execute('SELECT id FROM productTypes WHERE type=?', (self.data['product_type'],)).fetchone()
            if not type_exist:
                self.conn.execute('INSERT INTO productTypes (type) VALUES (?)', (self.data['product_type'],))
            type_id = self.conn.execute('SELECT id FROM productTypes WHERE type=?', (self.data['product_type'],)).fetchone()

        # Inserting product to the db
        self.conn.execute('INSERT INTO products (name, weight, weight_type, user_id, product_type_id) VALUES (?, ?, ?, ?, ?)',
                    (self.data['name'], self.data['weight'], self.data['weight-type'], current_user.id, type_id))

        prod_id = self.conn.execute('''SELECT id FROM products 
                                        WHERE name=? AND weight=? AND weightType=? AND price=? AND shop_id=?''',
                                        (self.data['name'], self.data['weight'], self.data['weight-type'], self.data['price'], shop_id)).fetchone()
        self.conn.execute('INSERT INTO usersProducts (user_id, prod_id) VALUES (?,?)',
                            (current_user.id, prod_id[0]))
        self.conn.commit()
        self.conn.close()
        return True
    def edit(self, shop_id=None):
        # Updating product information
        self.conn.execute('''UPDATE products SET name=?, weight=?, weightType=?, price=?, shop_id=?
                            WHERE id=?''',
                         (self.data['name'], self.data['weight'], self.data['weight-type'], self.data['price'], shop_id, self.product['id']))
        self.conn.commit()
        self.conn.close()
        return True
# Get product information by id (id, name, weight, price, shop_name)
def get_product(product_id):
    conn = c.get_db_connection()
    product = conn.execute('''SELECT sp.id AS id, p.id AS product_id, p.name AS name, p.weight AS weight, p.weight_type AS weight_type, pp.price AS price, s.name AS shop, p.product_type_id AS product_type_id
                              FROM products p JOIN shopsProducts sp
                              ON p.id = sp.product_id
                              JOIN shops s
                              ON s.id = sp.shop_id
                              JOIN productPrice pp
                              ON pp.product_id = sp.id
                              JOIN usersProducts u
                              ON u.product_id = sp.id
                              WHERE sp.id = ? AND u.user_id=?''', (product_id, current_user.id)).fetchone()
    conn.close()
    if product is None:
        c.abort(404)
    return product #(sp.id, product_id, name, weight, weight_type, price, shop, product_type_id)
# List of products page (open)
@app.route('/products')
def products():
    products = None
    if current_user.is_authenticated:
        conn = c.get_db_connection()
        products = conn.execute('''SELECT p.id AS id, p.name AS name, weight, weight_type
                                FROM products p JOIN shopsProducts sp
                                ON p.id == sp.product_id
                                JOIN usersProducts u
                                ON u.product_id = sp.id
                                WHERE u.user_id=?''', (current_user.id,)).fetchall()
        conn.commit()
        conn.close()
    return c.render_template('products.html', products = products)
# Page with all availiable data about the product
@app.route('/product<int:product_id>')
@login_required
def product(product_id):
    conn = c.get_db_connection()
    prod_id_exist = conn.execute('''SELECT sp.id FROM usersProducts u 
                                    JOIN shopsProducts sp ON u.product_id=sp.id WHERE u.user_id=? AND sp.product_id=?''', (current_user.id, product_id)).fetchone()
    if not prod_id_exist:
        conn.commit()
        conn.close()
        return c.redirect(c.url_for('products'))
    else:
        product = get_product(product_id) #(sp.id, product_id, name, weight, weight_type, price, shop, product_type_id)
        #recipes = conn.execute('''SELECT r.id, r.name, rt.type, i.prod_id, i.weight
        #                        FROM recipes r JOIN recipeTypes rt
        #                        ON r.type_id = rt.id
        #                        JOIN ingredients i
        #                        ON r.id = i.rec_id
        #                        JOIN usersRecipes u
        #                        ON u.rec_id = r.id
        #                        WHERE i.prod_id = ? AND u.user_id=?''', (product_id, current_user.id)).fetchall()
        conn.close()
        return c.render_template('product.html', product=product)#, recipes=recipes)
# Create new product page (open, form handling)
@app.route('/create_product', methods=('GET', 'POST'))
@login_required
def create_p():
    productAct = ProductAct()
    if productAct.act(productAct.create):
        return c.redirect(c.url_for('products'))
    productAct.conn.commit()
    productAct.conn.close()
    return c.render_template('create_p.html', shops=productAct.shops, data=productAct.data, prod_exist=productAct.prod_exist)
# Edit product page (open, form handling)
@app.route('/<int:product_id>_product_edit', methods=('GET', 'POST'))
@login_required
def edit_p(product_id):
    conn = c.get_db_connection()
    prod_id_exist = conn.execute('SELECT id FROM usersProducts WHERE user_id=? AND prod_id=?', (current_user.id, product_id)).fetchone()
    if not prod_id_exist:
        conn.commit()
        conn.close()
        return c.redirect(c.url_for('products'))
    else:
        productAct = ProductAct(product_id)
        if productAct.act(productAct.edit):
            return c.redirect(c.url_for('products'))
        return c.render_template('edit_p.html', shops=productAct.shops, product=productAct.data)
# Delete product
@app.route('/<int:product_id>/delete_product', methods=('POST',))
@login_required
def delete_p(product_id):
    conn = c.get_db_connection()
    prod_id_exist = conn.execute('SELECT id FROM usersProducts WHERE user_id=? AND prod_id=?', (current_user.id, product_id)).fetchone()
    if not prod_id_exist:
        conn.commit()
        conn.close()
        return c.redirect(c.url_for('products'))
    else:
        product = get_product(product_id)
        conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()
        c.flash('"{}" was successfully deleted!'.format(product['name']))
        return c.redirect(c.url_for('products'))


#def read_barcodes(frame, data):
#    barcodes = decode(frame)
#    for barcode in barcodes:
#        barcode_info = barcode.data.decode('utf-8')
#        data['barcode'] = barcode_info  
#    return frame
#@app.route('/read_barcode', methods=('GET', 'POST'))
#@login_required
#def read_barcode():
#    data={'barcode': None}
#    camera = cv2.VideoCapture(0)
#    ret, frame = camera.read()
#    while ret:
#        ret, frame = camera.read()
#        frame = read_barcodes(frame, data)
#        cv2.imshow('Barcode/QR code reader', frame)
#        if data['barcode']:
#            break
#    camera.release()
#    cv2.destroyAllWindows()
#    return c.jsonify(data)
