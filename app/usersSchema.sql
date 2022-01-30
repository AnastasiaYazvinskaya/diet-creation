-- Users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    icon TEXT
);
--INSERT INTO users (username,email, password) VALUES
--("TestUser", "diet.creation.sendler@gmail.com", "TestUserCreated001");