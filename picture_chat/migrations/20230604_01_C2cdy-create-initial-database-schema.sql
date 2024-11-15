-- Create initial database schema
-- depends:

CREATE TABLE chat_user (
    uuid TEXT PRIMARY KEY UNIQUE NOT NULL,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE message (
    uuid TEXT PRIMARY KEY UNIQUE NOT NULL,
    text TEXT,
    image TEXT,
    datetime TEXT NOT NULL,
    user_uuid TEXT REFERENCES chat_user(uuid) ON DELETE SET NULL
);
