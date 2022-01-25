
-- Products INFO
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
    weight NUMERIC(10, 4) NOT NULL,
    weightType TEXT NOT NULL,
    price NUMERIC(10, 4),
    shop_id INTEGER REFERENCES shops (id)
);

-- Recipes INFO
DROP TABLE IF EXISTS recipeTypes;
CREATE TABLE recipeTypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL
);

DROP TABLE IF EXISTS recipes;
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    type_id INTEGER REFERENCES recipeTypes (id),
    descr TEXT NOT NULL
);

DROP TABLE IF EXISTS ingredients;
CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rec_id INTEGER REFERENCES recipеs (id),
    prod_id INTEGER REFERENCES products (id),
    --prod_name TEXT NOT NULL,
    weight NUMERIC(10, 4) NOT NULL
);

-- Menu INFO
DROP TABLE IF EXISTS menu;
CREATE TABLE menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_name TEXT NOT NULL
);

DROP TABLE IF EXISTS week;
CREATE TABLE week (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    --week_num INTEGER NOT NULL,
    --menu_id INTEGER REFERENCES menu (id)
);

DROP TABLE IF EXISTS week_day;
CREATE TABLE week_day (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    weekday TEXT NOT NULL
    --week_id INTEGER REFERENCES week (id)
);

DROP TABLE IF EXISTS meal;
CREATE TABLE meal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rec_id INTEGER REFERENCES recipеs (id),
    --recipe TEXT,
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

-- Test INFO
--INSERT INTO menu (id, menu_name) VALUES
--(1, "Menu1"),
--(2, "Menu2");
--INSERT INTO meal (id, recipe, weekday_id, week, menu_id, type, place) VALUES
--(1, "RecipeM1_Mon_B0", 0, 1, 1, 1, 0),
--(2, "RecipeM1_Mon_B1", 0, 1, 1, 1, 1),
--(3, "RecipeM2_Fri_L", 4, 1, 2, 2, 0),
--(4, "RecipeM2_Mon_D", 0, 1, 2, 3, 0),
--(5, "RecipeM1_Wed_L", 2, 1, 1, 2, 0);


--INSERT INTO recipeTypes (id, type) VALUES
--(1, "Breakfast"),
--(2, "Lunch"),
--(3, "Dinner"),
--(4, "Drink");

--INSERT INTO recipes (id, name, type_id, descr) VALUES
--(1, "Recipe1B", 1, "Recipe1"),
--(2, "Recipe2D", 3, "Recipe2"),
--(3, "Recipe3B", 1, "Recipe3"),
--(4, "Recipe4L", 2, "Recipe4"),
--(5, "Recipe5O", 4, "Recipe5");