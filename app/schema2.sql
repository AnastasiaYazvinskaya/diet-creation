-- PRODUCTS INFO
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,               -- ID
    name TEXT NOT NULL,                                 -- Product's name
    weight NUMERIC(10, 4) NOT NULL,                     -- Selling package weight
    weight_type TEXT NOT NULL,                          -- Weight type
    user_id INTEGER REFERENCES users (id),              -- The user who created the product
    product_type_id INTEGER REFERENCES productTypes (id)-- Type of product as a separate meal
);
-- Join Shops with Products
DROP IF EXISTS shopsProducts;
CREATE TABLE shopsProducts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,       -- ID
    shop_id INTEGER REFERENCES shops (id),      -- Shop
    product_id INTEGER REFERENCES products (id) -- Product
);
-- Price
DROP IF EXISTS productPrice;
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
    frequency INTEGER                                 -- Frequency of use
);

-- RECIPES INFO
-- Simple products for recipes
DROP TABLE IF EXISTS simpleProducts;
CREATE TABLE simpleProducts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,-- ID
    name TEXT NOT NULL                   -- Product's name
);
-- Recipe types
DROP TABLE IF EXISTS recipeTypes;
CREATE TABLE recipeTypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,-- ID
    type TEXT NOT NULL                   -- Recipe's type
);
-- Recipes
DROP TABLE IF EXISTS recipes;
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,       -- ID
    name TEXT NOT NULL,                         -- Recipe's name
    recipe_type_id INTEGER REFERENCES recipeTypes (id),--Recipe's type
    description TEXT NOT NULL,                        -- Cooking instructions
    user_id INTEGER REFERENCES users (id)       -- The user who created the recipe
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

-- Menu INFO
DROP TABLE IF EXISTS menu;
CREATE TABLE menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_name TEXT NOT NULL,
    user_id INTEGER REFERENCES users (id)
);

DROP TABLE IF EXISTS week_day;
CREATE TABLE week_day (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    weekday TEXT NOT NULL
);

DROP TABLE IF EXISTS meal;
CREATE TABLE meal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rec_id INTEGER REFERENCES recipеs (id),
    weekday_id INTEGER REFERENCES week_day (id),
    week INTEGER NOT NULL,
    menu_id INTEGER REFERENCES menu (id),
    type INTEGER NOT NULL, -- 1-Breakfast, 2-Lunch, 3-Dinner, 4-Other
    place INTEGER NOT NULL
);

INSERT INTO week_day (id, weekday) VALUES
(1, "Mon"),
(2, "Tue"),
(3, "Wed"),
(4, "Thu"),
(5, "Fri"),
(6, "Sat"),
(7, "Sun");