import sqlite3

DB_NAME = "database.db"

def connect():
    return sqlite3.connect(DB_NAME)

def get_all(table):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    conn.close()
    return rows

def insert_product(name, price):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    conn.close()

def insert_courier(name, phone):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO couriers (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()
def update_product(product_id, name=None, price=None):
    conn = connect()
    cursor = conn.cursor()
    if name:
        cursor.execute("UPDATE products SET name=? WHERE id=?", (name, product_id))
    if price:
        cursor.execute("UPDATE products SET price=? WHERE id=?", (price, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()

def update_courier(courier_id, name=None, phone=None):
    conn = connect()
    cursor = conn.cursor()
    if name:
        cursor.execute("UPDATE couriers SET name=? WHERE id=?", (name, courier_id))
    if phone:
        cursor.execute("UPDATE couriers SET phone=? WHERE id=?", (phone, courier_id))
    conn.commit()
    conn.close()

def delete_courier(courier_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM couriers WHERE id=?", (courier_id,))
    conn.commit()
    conn.close()

def export_table_to_csv(table, filename):
    rows = get_all(table)
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def import_products_from_csv(filename):
    with open(filename, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            name, price = row
            insert_product(name, float(price))
