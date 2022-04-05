-- Users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL DEFAULT "user",
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    icon_id INTEGER REFERENCES user_icons (id) DEFAULT 1
);
-- User's icons
DROP TABLE IF EXISTS user_icons;
CREATE TABLE user_icons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    icon TEXT
);
