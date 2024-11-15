-- Add password for users
-- depends: 20230604_02_wFx8Z-add-room-tables

ALTER TABLE chat_user ADD COLUMN password TEXT NOT NULL;
