-- Run this while connected to your MySQL server as a user with CREATE DATABASE permission.
CREATE DATABASE IF NOT EXISTS banking_etl CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- The pipeline creates the transactions table automatically on the first load.
-- Subsequent runs atomically refresh the rows in that table.
