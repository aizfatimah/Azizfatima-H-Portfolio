import psycopg2
import csv
import os

# PostgreSQL connection info (edit to your setup)
PG_HOST = "localhost"
PG_PORT = mysql_port = 5432 
PG_DBNAME = "postgres"
PG_USER = "postgres"
PG_PASSWORD = "mysecretpassword"


ORDERS_CSV = "orders.csv"
ORDER_STATUSES = ["preparing", "out for delivery", "delivered", "cancelled"]

def connect_db():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DBNAME,
        user=PG_USER,
        password=PG_PASSWORD
    )

def setup_db():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL NOT NULL
                );
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS couriers (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL
                );
            ''')
        conn.commit()

def get_all_products():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, price FROM products ORDER BY id")
            return cur.fetchall()

def get_all_couriers():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, phone FROM couriers ORDER BY id")
            return cur.fetchall()

def insert_product(name, price):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO products (name, price) VALUES (%s, %s)", 
                (name, price)
            )
        conn.commit()

def insert_courier(name, phone):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO couriers (name, phone) VALUES (%s, %s)", 
                (name, phone)
            )
        conn.commit()

def update_product(id, name=None, price=None):
    with connect_db() as conn:
        with conn.cursor() as cur:
            if name is not None and price is not None:
                cur.execute("UPDATE products SET name=%s, price=%s WHERE id=%s", (name, price, id))
            elif name is not None:
                cur.execute("UPDATE products SET name=%s WHERE id=%s", (name, id))
            elif price is not None:
                cur.execute("UPDATE products SET price=%s WHERE id=%s", (price, id))
        conn.commit()

def delete_product(id):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM products WHERE id=%s", (id,))
        conn.commit()

def update_courier(id, name=None, phone=None):
    with connect_db() as conn:
        with conn.cursor() as cur:
            if name is not None and phone is not None:
                cur.execute("UPDATE couriers SET name=%s, phone=%s WHERE id=%s", (name, phone, id))
            elif name is not None:
                cur.execute("UPDATE couriers SET name=%s WHERE id=%s", (name, id))
            elif phone is not None:
                cur.execute("UPDATE couriers SET phone=%s WHERE id=%s", (phone, id))
        conn.commit()

def delete_courier(id):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM couriers WHERE id=%s", (id,))
        conn.commit()

# Orders CSV functions

def load_orders():
    orders = []
    if os.path.exists(ORDERS_CSV):
        with open(ORDERS_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) != 5:
                    continue  # skip malformed rows
                customer_name, customer_address, courier_id, status, items_str = row
                orders.append({
                    "customer_name": customer_name,
                    "customer_address": customer_address,
                    "courier": int(courier_id),
                    "status": status,
                    "items": items_str  # string of comma-separated product IDs, e.g. "1,3,4"
                })
    return orders

def save_orders(orders):
    with open(ORDERS_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for o in orders:
            writer.writerow([
                o["customer_name"],
                o["customer_address"],
                o["courier"],
                o["status"],
                o["items"]
            ])

def print_products():
    products = get_all_products()
    if not products:
        print("No products found.")
        return
    print("Products:")
    for p in products:
        print(f"ID: {p[0]} | Name: {p[1]} | Price: £{p[2]:.2f}")

def print_couriers():
    couriers = get_all_couriers()
    if not couriers:
        print("No couriers found.")
        return
    print("Couriers:")
    for c in couriers:
        print(f"ID: {c[0]} | Name: {c[1]} | Phone: {c[2]}")

def print_orders(orders):
    if not orders:
        print("No orders found.")
        return
    print("Orders:")
    for idx, o in enumerate(orders):
        print(f"{idx}: Customer: {o['customer_name']}, Address: {o['customer_address']}, Courier ID: {o['courier']}, Status: {o['status']}, Items: {o['items']}")

def main_menu():
    print("""
MAIN MENU:
0 - Exit
1 - Products
2 - Couriers
3 - Orders
""")

def products_menu():
    print("""
PRODUCTS MENU:
0 - Return to main menu
1 - View all products
2 - Create new product
3 - Update product
4 - Delete product
""")

def couriers_menu():
    print("""
COURIERS MENU:
0 - Return to main menu
1 - View all couriers
2 - Create new courier
3 - Update courier
4 - Delete courier
""")

def orders_menu():
    print("""
ORDERS MENU:
0 - Return to main menu
1 - View all orders
2 - Create new order
3 - Update order status
4 - Update order details
5 - Delete order
""")

def main():
    setup_db()
    orders = load_orders()

    while True:
        main_menu()
        choice = input("Choose option: ").strip()
        if choice == "0":
            save_orders(orders)
            print("Goodbye!")
            break
        elif choice == "1":
            while True:
                products_menu()
                p_choice = input("Choose product option: ").strip()
                if p_choice == "0":
                    break
                elif p_choice == "1":
                    print_products()
                elif p_choice == "2":
                    name = input("Enter product name: ").strip()
                    price_str = input("Enter product price: ").strip()
                    try:
                        price = float(price_str)
                        insert_product(name, price)
                        print("Product added.")
                    except ValueError:
                        print("Invalid price.")
                elif p_choice == "3":
                    products = get_all_products()
                    if not products:
                        print("No products to update.")
                        continue
                    print_products()
                    id_str = input("Enter product ID to update: ").strip()
                    if not id_str.isdigit():
                        print("Invalid ID.")
                        continue
                    id = int(id_str)
                    name = input("Enter new product name (leave blank to keep current): ").strip()
                    price_str = input("Enter new product price (leave blank to keep current): ").strip()
                    price = None
                    if price_str != "":
                        try:
                            price = float(price_str)
                        except ValueError:
                            print("Invalid price entered, skipping price update.")
                    update_product(id, name if name != "" else None, price)
                    print("Product updated.")
                elif p_choice == "4":
                    print_products()
                    id_str = input("Enter product ID to delete: ").strip()
                    if not id_str.isdigit():
                        print("Invalid ID.")
                        continue
                    id = int(id_str)
                    delete_product(id)
                    print("Product deleted.")
                else:
                    print("Invalid option.")
        elif choice == "2":
            while True:
                couriers_menu()
                c_choice = input("Choose courier option: ").strip()
                if c_choice == "0":
                    break
                elif c_choice == "1":
                    print_couriers()
                elif c_choice == "2":
                    name = input("Enter courier name: ").strip()
                    phone = input("Enter courier phone: ").strip()
                    insert_courier(name, phone)
                    print("Courier added.")
                elif c_choice == "3":
                    couriers = get_all_couriers()
                    if not couriers:
                        print("No couriers to update.")
                        continue
                    print_couriers()
                    id_str = input("Enter courier ID to update: ").strip()
                    if not id_str.isdigit():
                        print("Invalid ID.")
                        continue
                    id = int(id_str)
                    name = input("Enter new courier name (leave blank to keep current): ").strip()
                    phone = input("Enter new courier phone (leave blank to keep current): ").strip()
                    update_courier(id, name if name != "" else None, phone if phone != "" else None)
                    print("Courier updated.")
                elif c_choice == "4":
                    print_couriers()
                    id_str = input("Enter courier ID to delete: ").strip()
                    if not id_str.isdigit():
                        print("Invalid ID.")
                        continue
                    id = int(id_str)
                    delete_courier(id)
                    print("Courier deleted.")
                else:
                    print("Invalid option.")
        elif choice == "3":
            while True:
                orders_menu()
                o_choice = input("Choose order option: ").strip()
                if o_choice == "0":
                    break
                elif o_choice == "1":
                    print_orders(orders)
                elif o_choice == "2":
                    customer_name = input("Customer name: ").strip()
                    customer_address = input("Customer address: ").strip()
                    customer_phone = input("Customer phone: ").strip()

                    print_products()
                    product_ids_str = input("Enter product IDs (comma separated): ").strip()
                    # Validate product IDs
                    product_ids = product_ids_str.replace(" ", "").split(",")
                    if any(not pid.isdigit() for pid in product_ids):
                        print("Invalid product IDs entered.")
                        continue
                    product_ids_str_clean = ",".join(product_ids)

                    print_couriers()
                    courier_id_str = input("Enter courier ID: ").strip()
                    if not courier_id_str.isdigit():
                        print("Invalid courier ID.")
                        continue
                    courier_id = int(courier_id_str)

                    new_order = {
                        "customer_name": customer_name,
                        "customer_address": customer_address,
                        "customer_phone": customer_phone,
                        "courier": courier_id,
                        "status": "preparing",
                        "items": product_ids_str_clean
                    }
                    orders.append(new_order)
                    print("Order added.")
                elif o_choice == "3":
                    if not orders:
                        print("No orders to update.")
                        continue
                    print_orders(orders)
                    index_str = input("Enter order index to update status: ").strip()
                    if not index_str.isdigit() or int(index_str) >= len(orders):
                        print("Invalid order index.")
                        continue
                    idx = int(index_str)

                    print("Order statuses:")
                    for i, status in enumerate(ORDER_STATUSES):
                        print(f"{i} - {status}")
                    status_idx_str = input("Choose new status index: ").strip()
                    if not status_idx_str.isdigit() or int(status_idx_str) >= len(ORDER_STATUSES):
                        print("Invalid status index.")
                        continue
                    new_status = ORDER_STATUSES[int(status_idx_str)]
                    orders[idx]["status"] = new_status
                    print("Order status updated.")
                elif o_choice == "4":
                    if not orders:
                        print("No orders to update.")
                        continue
                    print_orders(orders)
                    index_str = input("Enter order index to update details: ").strip()
                    if not index_str.isdigit() or int(index_str) >= len(orders):
                        print("Invalid order index.")
                        continue
                    idx = int(index_str)
                    order = orders[idx]

                    new_name = input(f"Customer name [{order['customer_name']}]: ").strip()
                    if new_name != "":
                        order['customer_name'] = new_name
                    new_address = input(f"Customer address [{order['customer_address']}]: ").strip()
                    if new_address != "":
                        order['customer_address'] = new_address
                    new_phone = input(f"Customer phone [{order['customer_phone']}]: ").strip()
                    if new_phone != "":
                        order['customer_phone'] = new_phone

                    print_products()
                    new_items = input(f"Product IDs [{order['items']}]: ").strip()
                    if new_items != "":
                        product_ids = new_items.replace(" ", "").split(",")
                        if any(not pid.isdigit() for pid in product_ids):
                            print("Invalid product IDs entered, skipping update.")
                        else:
                            order['items'] = ",".join(product_ids)

                    print_couriers()
                    new_courier_str = input(f"Courier ID [{order['courier']}]: ").strip()
                    if new_courier_str != "":
                        if not new_courier_str.isdigit():
                            print("Invalid courier ID, skipping update.")
                        else:
                            order['courier'] = int(new_courier_str)

                    new_status_str = input(f"Status [{order['status']}]: ").strip()
                    if new_status_str != "":
                        if new_status_str in ORDER_STATUSES:
                            order['status'] = new_status_str
                        else:
                            print("Invalid status, skipping update.")

                    print("Order updated.")
                elif o_choice == "5":
                    if not orders:
                        print("No orders to delete.")
                        continue
                    print_orders(orders)
                    index_str = input("Enter order index to delete: ").strip()
                    if not index_str.isdigit() or int(index_str) >= len(orders):
                        print("Invalid order index.")
                        continue
                    idx = int(index_str)
                    orders.pop(idx)
                    print("Order deleted.")
                else:
                    print("Invalid option.")
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
