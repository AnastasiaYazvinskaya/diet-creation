-- Users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    --icon TEXT
    icon_id INTEGER REFERENCES user_icons (id)
);

DROP TABLE IF EXISTS user_icons;
CREATE TABLE user_icons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    icon TEXT
);
--INSERT INTO users (username,email, password) VALUES
--("TestUser", "diet.creation.sendler@gmail.com", "TestUserCreated001");