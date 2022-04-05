import app.connect as c
from app import app
from flask_login import login_required, current_user
from app.product import Product
#import cv2
#from pyzbar import pyzbar
#from pyzbar.pyzbar import decode

# Class to create and edit product information
class ProductAct:
    def __init__(self, shop_product_id=None):
        self.conn = c.get_db_connection() # connect to the database
        self.shops = self.conn.execute('SELECT * FROM shops').fetchall() # list of shops
        self.product = Product()
        if shop_product_id: # If edit product get its data
            self.product.set_data_by_id(shop_product_id)
    def act(self, func):
        #new = ''
        if c.request.method == 'POST':
            name = c.request.form['name']
            weight = float(c.request.form['weight'])
            weight_type = c.request.form['weight-type']
            barcode = c.request.form['barcode']
            # If required data entered then start work with it
            if name and weight and weight_type:
                # If product do not exist
                if not self.product.product_exist(name, weight, weight_type):
                    self.product.set_required_data(name, weight, weight_type)
                    # If barcode entered save it
                    if barcode:
                        self.product.set_barcode(int(barcode))
                    # If the product checked as an independent
                    try:
                        product_as_recipe = c.request.form['product_as_recipe']
                        if product_as_recipe: # and type entered add this data
                            product_type = c.request.form['ptype']
                            if product_type:
                                self.product.set_type_data(product_type)
                    except c.BadRequest:
                        pass
                    # If user open additional fields for product information
                    try:
                        shop = c.request.form['shop']
                        price = float(c.request.form['price'])
                        # If shop and price entered save information
                        if shop and price:
                            self.product.set_additional_data(shop, price)
                    except c.BadRequest:
                        pass
                    return func()
        return False

    def create(self):
        self.product.create_product()
        return True
    def edit(self):
        self.product.edit_product()
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
        products = conn.execute('''SELECT sp.id AS id, p.name AS name, weight, weight_type
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
    return c.render_template('create_p.html', shops=productAct.shops, data=productAct.product)#, prod_exist=productAct.prod_exist)
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