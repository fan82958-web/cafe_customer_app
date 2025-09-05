-- schema.sql
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS visits;

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    visit_count INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    visit_date TEXT NOT NULL,
    orders TEXT,
    memo TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers (id)
);