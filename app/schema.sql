-- PRODUCTS INFO
-- Simple products for recipes
DROP TABLE IF EXISTS simpleProducts;
CREATE TABLE simpleProducts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,-- ID
    name TEXT NOT NULL                   -- Product's simple name
);
INSERT INTO simpleProducts (id, name) VALUES
(1, "unknown");
-- Shops
DROP TABLE IF EXISTS shops;
CREATE TABLE shops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,-- ID
    name TEXT NOT NULL                   -- Shop's name
);
-- Default shop
INSERT INTO shops (id, name) VALUES
(1, "unknown");
-- Product types
DROP TABLE IF EXISTS productTypes;
CREATE TABLE productTypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,-- ID
    type TEXT NOT NULL                   -- Product's type
);
-- Default product type
INSERT INTO productTypes (id, type) VALUES
(1, "cook");
-- Products
DROP TABLE IF EXISTS products;
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,                -- ID
    name TEXT NOT NULL,                                  -- Product's name
    weight NUMERIC(10, 4) NOT NULL,                      -- Selling package weight
    weight_type TEXT NOT NULL,                           -- Weight type
    user_id INTEGER REFERENCES users (id),               -- The user who created the product
    product_type_id INTEGER REFERENCES productTypes (id),-- Type of product as a separate meal
    --simple_name INTEGER REFERENCES simpleProducts (id)   -- Simple name for product
    barcode INTEGER                                      -- Barcode number
);
-- Join Products with Simple Products
DROP TABLE IF EXISTS productsSimpleProducts;
CREATE TABLE productsSimpleProducts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,                  -- ID
    simple_name_id INTEGER REFERENCES simpleProducts (id), --Simple Product's name
    product_id INTEGER REFERENCES products (id)            -- Product
);
-- Join Shops with Products
DROP TABLE IF EXISTS shopsProducts;
CREATE TABLE shopsProducts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,       -- ID
    shop_id INTEGER REFERENCES shops (id),      -- Shop
    product_id INTEGER REFERENCES products (id) -- Product
);
-- Price
DROP TABLE IF EXISTS productPrice;
CREATE TABLE productPrice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,                -- ID
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,-- Time when the product was created
    product_id INTEGER REFERENCES shopsProducts (id),    -- Product in the shop
    price NUMERIC(10, 4)                                 -- Price
);
-- Join Users with Products
DROP TABLE IF EXISTS usersProducts;
CREATE TABLE usersProducts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,             -- ID
    user_id INTEGER REFERENCES users (id),            -- User
    product_id INTEGER REFERENCES shopsProducts (id), -- Product in the shop
    frequency INTEGER DEFAULT 0                       -- Frequency of use
);

-- RECIPES INFO
-- Recipe types
DROP TABLE IF EXISTS recipeTypes;
CREATE TABLE recipeTypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,-- ID
    recipe_type INTEGER NOT NULL,        -- 1-dish, 2-meal, 3-kitchen, 4-other
    type TEXT NOT NULL                   -- Recipe's type
);
INSERT INTO recipeTypes (recipe_type, type) VALUES
(4, "general");
-- Recipes
DROP TABLE IF EXISTS recipes;
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,       -- ID
    name TEXT NOT NULL,                         -- Recipe's name
    photo TEXT,
    description TEXT NOT NULL,                  -- Cooking instructions
    as_product NUMBER(1) DEFAULT 0,
    cooking_time TEXT,
    portions INTEGER,
    portion_weight NUMERIC(10, 4),
    kcal NUMERIC(10, 4),
    average_price NUMERIC(10,4),
    user_id INTEGER REFERENCES users (id)       -- The user who created the recipe
);
-- Join Recipe Types with Recipes
DROP TABLE IF EXISTS recipeTypesRecipes;
CREATE TABLE recipeTypesRecipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- ID
    recipe_id INTEGER REFERENCES recipes (id),
    recipe_type_id INTEGER REFERENCES recipeTypes (id)
);
-- Ingredients
DROP TABLE IF EXISTS ingredients;
CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,             -- ID
    recipe_id INTEGER REFERENCES recipеs (id),        -- Recipe
    product_id INTEGER REFERENCES simpleProducts (id),-- Simple product
    weight NUMERIC(10, 4) NOT NULL,                   -- Product's weight for recipe
    weight_type TEXT NOT NULL                         -- Weight type
);
-- Join Users with Recipes
DROP TABLE IF EXISTS usersRecipes;
CREATE TABLE usersRecipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- ID
    user_id INTEGER REFERENCES users (id),-- User
    recipe_id INTEGER REFERENCES recipes (id)-- Recipe
);