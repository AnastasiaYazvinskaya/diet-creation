import app.connect as c
from app import app
from flask_login import login_required, current_user

import cv2
from pyzbar import pyzbar
from pyzbar.pyzbar import decode
# Class for creating and editing product information
class ProductAct:
    def __init__(self, product_id=None):
        self.product_id = product_id
        self.conn = c.get_db_connection()
        self.shops = self.conn.execute('SELECT * FROM shops').fetchall()
        self.data = {'name': '', 'weight': '', 'weight-type': '', 'price': '', 'shop': 'unknown'}
        self.prod_exist = None
        if product_id:
            self.product = get_product(self.product_id)
            self.data = {'name': self.product['name'], 
                         'weight': self.product['weight'],
                         'weight-type': self.product['weightType'], 
                         'price': self.product['price'], 
                         'shop': self.product['shop']}
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
            self.prod_exist = self.conn.execute('''SELECT p.id AS id, p.name AS name, weight, weightType, price, s.name AS shop
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
            elif new == 'new' or (new == '' and (not len(self.prod_exist) or len(self.prod_exist)==1 and self.prod_exist[0]['id']==self.product_id)):
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
        # Inserting product to the db
        self.conn.execute('INSERT INTO products (name, weight, weightType, price, shop_id) VALUES (?, ?, ?, ?, ?)',
                    (self.data['name'], self.data['weight'], self.data['weight-type'], self.data['price'], shop_id))

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
    product = conn.execute('''SELECT p.id AS id, p.name AS name, weight, weightType, price, s.name AS shop
                              FROM products p JOIN shops s
                              ON p.shop_id = s.id
                              JOIN usersProducts u
                              ON u.prod_id = p.id
                              WHERE p.id = ? AND u.user_id=?''', (product_id, current_user.id)).fetchone()
    conn.close()
    if product is None:
        c.abort(404)
    return product
# List of products page (open)
@app.route('/products')
def products():
    products = None
    if current_user.is_authenticated:
        conn = c.get_db_connection()
        products = conn.execute('''SELECT p.id AS id, p.name AS name, weight, weightType, price, s.name AS shop
                                FROM products p JOIN shops s
                                ON p.shop_id = s.id
                                JOIN usersProducts u
                                ON u.prod_id = p.id
                                WHERE u.user_id=?''', (current_user.id,)).fetchall()
        conn.commit()
        conn.close()
    return c.render_template('products.html', products = products)

@app.route('/product<int:product_id>')
@login_required
def product(product_id):
    conn = c.get_db_connection()
    prod_id_exist = conn.execute('SELECT id FROM usersProducts WHERE user_id=? AND prod_id=?', (current_user.id, product_id)).fetchone()
    if not prod_id_exist:
        conn.commit()
        conn.close()
        return c.redirect(c.url_for('products'))
    else:
        product = get_product(product_id)
        recipes = conn.execute('''SELECT r.id, r.name, rt.type, i.prod_id, i.weight
                                FROM recipes r JOIN recipeTypes rt
                                ON r.type_id = rt.id
                                JOIN ingredients i
                                ON r.id = i.rec_id
                                JOIN usersRecipes u
                                ON u.rec_id = r.id
                                WHERE i.prod_id = ? AND u.user_id=?''', (product_id, current_user.id)).fetchall()
        conn.close()
        return c.render_template('product.html', product=product, recipes=recipes)
# Create new product page (open, form handling)
@app.route('/create_product', methods=('GET', 'POST'))
@login_required
def create_p():
    productAct = ProductAct()
    if productAct.act(productAct.create):
        return c.redirect(c.url_for('products'))
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


def read_barcodes(frame, data):
    barcodes = decode(frame)
    for barcode in barcodes:
        barcode_info = barcode.data.decode('utf-8')
        data['barcode'] = barcode_info  
    return frame
@app.route('/read_barcode', methods=('GET', 'POST'))
@login_required
def read_barcode():
    data={'barcode': None}
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame, data)
        cv2.imshow('Barcode/QR code reader', frame)
        if data['barcode']:
            break
    camera.release()
    cv2.destroyAllWindows()
    return c.jsonify(data)