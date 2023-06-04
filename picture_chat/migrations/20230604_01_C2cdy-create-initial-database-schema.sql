-- Create initial database schema

CREATE TABLE user (
    uuid TEXT PRIMARY KEY UNIQUE NOT NULL,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE message (
    uuid TEXT PRIMARY KEY UNIQUE NOT NULL,
    text TEXT,
    image TEXT,
    datetime TEXT NOT NULL,
    user_uuid TEXT REFERENCES user(uuid) ON DELETE SET NULL
);
