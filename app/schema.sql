DROP TABLE IF EXISTS shops;

CREATE TABLE shops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    weight NUMERIC(10, 2) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    shop TEXT NOT NULL
    --shop_id INTEGER REFERENCES shops (id)
);

DROP TABLE IF EXISTS recipes;

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    type TEXT,
    descr TEXT NOT NULL
);

DROP TABLE IF EXISTS ingredients;

CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rec_id INTEGER REFERENCES recipеs (id),
    --prod_id INTEGER REFERENCES products (id),
    prod_name TEXT,
    weight NUMERIC(10, 2)
);