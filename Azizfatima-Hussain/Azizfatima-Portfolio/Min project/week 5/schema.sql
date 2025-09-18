CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS couriers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL
);


INSERT INTO couriers (name, phone) VALUES ('Derek', '07123456789');
INSERT INTO couriers (name, phone) VALUES ('Sully', '07123456789');
INSERT INTO couriers (name, phone) VALUES ('Arjun', '07123456789');
INSERT INTO couriers (name, phone) VALUES ('Iyad', '07123456789');
INSERT INTO couriers (name, phone) VALUES ('Ayuuub', '07123456789');

INSERT INTO products (name, price) VALUES ('Iced Coffee', 0.8);
INSERT INTO products (name, price) VALUES ('Latte', 2.5);
INSERT INTO products (name, price) VALUES ('Cappuccino', 3.0);
INSERT INTO products (name, price) VALUES ('bubble tea', 2.0);
INSERT INTO products (name, price) VALUES ('Mango ice cream', 2.5);
INSERT INTO products (name, price) VALUES ('Strawberry milkshake', 3.0);
