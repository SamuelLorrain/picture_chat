-- Add room tables
-- depends: 20230604_01_C2cdy-create-initial-database-schema

CREATE TABLE room (
    uuid TEXT PRIMARY KEY UNIQUE NOT NULL,
    name TEXT UNIQUE NOT NULL
);

ALTER TABLE message ADD COLUMN room_uuid TEXT REFERENCES room(uuid) ON DELETE CASCADE;
