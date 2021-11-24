import app.connect as c
from app import app
# Class for creating and editing product information
class ProductAct:
    def __init__(self, product_id=None):
        self.conn = c.get_db_connection()
        self.shops = self.conn.execute('SELECT * FROM shops').fetchall()
        self.data = {'name': '', 'weight': '', 'price': '', 'shop': ''}
        self.prod_exist = None
        if product_id:
            self.product = get_product(product_id)
            self.data = {'name': self.product['name'], 
                         'weight': self.product['weight'], 
                         'price': self.product['price'], 
                         'shop': self.product['shop']}
    def act(self, func):
        finish = False
        new = ''
        if c.request.method == 'POST':
            self.data['name'] = c.request.form['name']
            self.data['weight'] = c.request.form['weight']
            self.data['price'] = c.request.form['price']
            self.data['shop'] = c.request.form['shop']
            # (HERE) Checking for the presence of the same product
            self.prod_exist = self.conn.execute('''SELECT p.id AS id, p.name AS name, weight, price, s.name AS shop
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
            # If one of the field is empty then refresh page with saving data in the fields
            print(new)
            if not self.data['name'] or not self.data['weight'] or not self.data['price'] or not self.data['shop']:
                c.flash('Name is requered!')
            elif new == 'new' or new == '':
                shop_exist = self.conn.execute('SELECT id FROM shops WHERE name=?',
                                            (self.data['shop'],)).fetchone()
                if not shop_exist:
                    add = self.conn.execute('INSERT INTO shops (name) VALUES (?)',
                                        (self.data['shop'],))
                shop_id = self.conn.execute('SELECT id FROM shops WHERE name=?',
                                        (self.data['shop'],)).fetchone()
                finish = func(shop_id)
            elif new.isnumeric():
                finish = True
        return finish
    def create(self, shop_id):
        # Inserting product to the db
        self.conn.execute('INSERT INTO products (name, weight, price, shop_id) VALUES (?, ?, ?, ?)',
                    (self.data['name'], self.data['weight'], self.data['price'], shop_id[0]))
        self.conn.commit()
        self.conn.close()
        return True
    def edit(self, shop_id):
        # Updating product information
        print("Updated")
        self.conn.execute('''UPDATE products SET name=?, weight=?, price=?, shop_id=?
                            WHERE id=?''',
                         (self.data['name'], self.data['weight'], self.data['price'], shop_id[0], self.product['id']))
        self.conn.commit()
        self.conn.close()
        return True
# Get product information by id (id, name, weight, price, shop_name)
def get_product(product_id):
    conn = c.get_db_connection()
    product = conn.execute('''SELECT p.id AS id, p.name AS name, weight, price, s.name AS shop
                              FROM products p JOIN shops s
                              ON p.shop_id = s.id
                              WHERE p.id = ?''', (product_id,)).fetchone()
    conn.close()
    if product is None:
        c.abort(404)
    return product
# List of products page (open)
@app.route('/products')
def products():
    conn = c.get_db_connection()
    products = conn.execute('''SELECT p.id AS id, p.name AS name, weight, price, s.name AS shop
                               FROM products p JOIN shops s
                               ON p.shop_id = s.id''').fetchall()
    conn.close()
    return c.render_template('products.html', products = products)
# Create new product page (open, form handling)
@app.route('/create_product', methods=('GET', 'POST'))
def create_p():
    productAct = ProductAct()
    if productAct.act(productAct.create):
        return c.redirect(c.url_for('products'))
    return c.render_template('create_p.html', shops=productAct.shops, data=productAct.data, prod_exist=productAct.prod_exist)
# Edit product page (open, form handling)
@app.route('/<int:id>_product_edit', methods=('GET', 'POST'))
def edit_p(id):
    productAct = ProductAct(id)
    if productAct.act(productAct.edit):
        return c.redirect(c.url_for('products'))
    return c.render_template('edit_p.html', shops=productAct.shops, product=productAct.data)
# Delete product
@app.route('/<int:id>/delete_product', methods=('POST',))
def delete_p(id):
    product = get_product(id)
    conn = c.get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    c.flash('"{}" was successfully deleted!'.format(product['name']))
    return c.redirect(c.url_for('products'))