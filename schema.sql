-- schema.sql
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    visit_count INTEGER NOT NULL DEFAULT 0
);