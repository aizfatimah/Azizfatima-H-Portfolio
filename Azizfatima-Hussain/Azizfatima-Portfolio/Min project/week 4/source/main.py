import os
import csv

# --------- Constants ---------
BASE_PATH = r"C:\Users\AzizfatimaH(DE-X6-LM\Documents\Data-Engineeringreal\Azizfatima-Portfolio\Min project\Week 4\data"
PRODUCTS_FILE = os.path.join(BASE_PATH, "products.csv")
COURIERS_FILE = os.path.join(BASE_PATH, "couriers.csv")
ORDERS_FILE = os.path.join(BASE_PATH, "orders.csv")

ORDER_STATUS_OPTIONS = ["PREPARING", "OUT FOR DELIVERY", "DELIVERED"]

# --------- File Handling ---------
def load_products():
    products = []
    if not os.path.exists(PRODUCTS_FILE):
        return products
    with open(PRODUCTS_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert price to float
            row['price'] = float(row['price'])
            products.append(row)
    return products

def save_products(products):
    with open(PRODUCTS_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['name', 'price']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

def load_couriers():
    couriers = []
    if not os.path.exists(COURIERS_FILE):
        return couriers
    with open(COURIERS_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            couriers.append(row)
    return couriers

def save_couriers(couriers):
    with open(COURIERS_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['name', 'phone']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(couriers)

def load_orders():
    orders = []
    if not os.path.exists(ORDERS_FILE):
        return orders
    with open(ORDERS_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert courier to int, items to list of ints
            row['courier'] = int(row['courier'])
            row['items'] = [int(i) for i in row['items'].split(',') if i]
            orders.append(row)
    return orders

def save_orders(orders):
    with open(ORDERS_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['customer_name', 'customer_address', 'customer_phone', 'courier', 'status', 'items']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for order in orders:
            row = order.copy()
            row['courier'] = str(row['courier'])
            row['items'] = ",".join(str(i) for i in row['items'])
            writer.writerow(row)

# --------- Display Functions ---------
def view_list(title, data_list, show_price=False, show_phone=False):
    print(f"\n{title}:")
    if not data_list:
        print("  (empty)")
    else:
        for i, item in enumerate(data_list):
            if show_price:
                print(f"  {i}. {item['name']} - ${item['price']:.2f}")
            elif show_phone:
                print(f"  {i}. {item['name']} - Phone: {item['phone']}")
            else:
                print(f"  {i}. {item['name']}")

def view_orders(orders, couriers, products):
    print("\nOrders List:")
    if not orders:
        print("  (no orders)")
    else:
        for i, order in enumerate(orders):
            courier_name = couriers[order['courier']]['name'] if 0 <= order['courier'] < len(couriers) else "Unknown"
            product_names = [products[idx]['name'] if 0 <= idx < len(products) else "Unknown" for idx in order['items']]
            print(f"  {i}. Customer: {order['customer_name']} | Address: {order['customer_address']} | Phone: {order['customer_phone']} | "
                  f"Courier: {courier_name} | Status: {order['status']} | Products: {', '.join(product_names)}")

# --------- Products Functions ---------
def add_product(products):
    name = input("Enter new product name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return
    try:
        price = float(input("Enter product price: "))
    except ValueError:
        print("Invalid price.")
        return
    products.append({"name": name, "price": price})
    print("Product added.")

def update_product(products):
    view_list("Products", products, show_price=True)
    try:
        index = int(input("Enter product index to update: "))
        if index < 0 or index >= len(products):
            raise IndexError
        name = input(f"Enter new product name (blank to keep '{products[index]['name']}'): ").strip()
        price_input = input(f"Enter new product price (blank to keep {products[index]['price']}): ").strip()
        if name:
            products[index]['name'] = name
        if price_input:
            try:
                products[index]['price'] = float(price_input)
            except ValueError:
                print("Invalid price input. Price not updated.")
        print("Product updated.")
    except (ValueError, IndexError):
        print("Invalid product index.")

def delete_product(products):
    view_list("Products", products, show_price=True)
    try:
        index = int(input("Enter product index to delete: "))
        if index < 0 or index >= len(products):
            raise IndexError
        removed = products.pop(index)
        print(f"Deleted product: {removed['name']}")
    except (ValueError, IndexError):
        print("Invalid product index.")

# --------- Couriers Functions ---------
def add_courier(couriers):
    name = input("Enter new courier name: ").strip()
    if not name:
        print("Courier name cannot be empty.")
        return
    phone = input("Enter courier phone number: ").strip()
    couriers.append({"name": name, "phone": phone})
    print("Courier added.")

def update_courier(couriers):
    view_list("Couriers", couriers, show_phone=True)
    try:
        index = int(input("Enter courier index to update: "))
        if index < 0 or index >= len(couriers):
            raise IndexError
        name = input(f"Enter new courier name (blank to keep '{couriers[index]['name']}'): ").strip()
        phone = input(f"Enter new courier phone (blank to keep '{couriers[index]['phone']}'): ").strip()
        if name:
            couriers[index]['name'] = name
        if phone:
            couriers[index]['phone'] = phone
        print("Courier updated.")
    except (ValueError, IndexError):
        print("Invalid courier index.")

def delete_courier(couriers):
    view_list("Couriers", couriers, show_phone=True)
    try:
        index = int(input("Enter courier index to delete: "))
        if index < 0 or index >= len(couriers):
            raise IndexError
        removed = couriers.pop(index)
        print(f"Deleted courier: {removed['name']}")
    except (ValueError, IndexError):
        print("Invalid courier index.")

# --------- Orders Functions ---------
def create_order(orders, couriers, products):
    name = input("Customer name: ").strip()
    address = input("Customer address: ").strip()
    phone = input("Customer phone: ").strip()
    if not (name and address and phone):
        print("Customer info cannot be empty.")
        return

    view_list("Products", products, show_price=True)
    product_input = input("Enter comma-separated product indexes: ").strip()
    try:
        product_indexes = [int(i) for i in product_input.split(",") if i.strip()]
        if any(i < 0 or i >= len(products) for i in product_indexes):
            raise IndexError
    except (ValueError, IndexError):
        print("Invalid product indexes.")
        return

    view_list("Couriers", couriers, show_phone=True)
    try:
        courier_index = int(input("Choose courier index: "))
        if courier_index < 0 or courier_index >= len(couriers):
            raise IndexError
    except (ValueError, IndexError):
        print("Invalid courier selection.")
        return

    order = {
        "customer_name": name,
        "customer_address": address,
        "customer_phone": phone,
        "courier": courier_index,
        "status": "PREPARING",
        "items": product_indexes
    }
    orders.append(order)
    print("Order created.")

def update_order_status(orders):
    if not orders:
        print("No orders to update.")
        return
    view_orders(orders, couriers, products)
    try:
        order_index = int(input("Enter order index: "))
        if order_index < 0 or order_index >= len(orders):
            raise IndexError
        print("Order Status Options:")
        for i, status in enumerate(ORDER_STATUS_OPTIONS):
            print(f"  {i}. {status}")
        status_index = int(input("Choose new status index: "))
        if status_index < 0 or status_index >= len(ORDER_STATUS_OPTIONS):
            raise IndexError
        orders[order_index]["status"] = ORDER_STATUS_OPTIONS[status_index]
        print("Order status updated.")
    except (ValueError, IndexError):
        print("Invalid input.")

def update_order_info(orders, couriers, products):
    if not orders:
        print("No orders to update.")
        return
    view_orders(orders, couriers, products)
    try:
        index = int(input("Enter order index to update: "))
        if index < 0 or index >= len(orders):
            raise IndexError
        order = orders[index]
        for key in ["customer_name", "customer_address", "customer_phone"]:
            current = order[key]
            new_val = input(f"{key.replace('_', ' ').title()} (current: {current}): ").strip()
            if new_val:
                order[key] = new_val

        view_list("Products", products, show_price=True)
        new_items = input(f"Product indexes (comma separated) (current: {','.join(map(str, order['items']))}): ").strip()
        if new_items:
            try:
                new_item_indexes = [int(i) for i in new_items.split(",") if i.strip()]
                if any(i < 0 or i >= len(products) for i in new_item_indexes):
                    raise IndexError
                order['items'] = new_item_indexes
            except (ValueError, IndexError):
                print("Invalid product indexes. Products not updated.")

        view_list("Couriers", couriers, show_phone=True)
        new_courier = input(f"Courier index (current: {order['courier']}): ").strip()
        if new_courier:
            try:
                new_courier_index = int(new_courier)
                if 0 <= new_courier_index < len(couriers):
                    order["courier"] = new_courier_index
                else:
                    print("Invalid courier index. Courier not updated.")
            except ValueError:
                print("Invalid input for courier index. Courier not updated.")
        print("Order updated.")
    except (ValueError, IndexError):
        print("Invalid input.")

def delete_order(orders):
    if not orders:
        print("No orders to delete.")
        return
    view_orders(orders, couriers, products)
    try:
        index = int(input("Enter order index to delete: "))
        if index < 0 or index >= len(orders):
            raise IndexError
        removed_order = orders.pop(index)
        print(f"Deleted order for {removed_order['customer_name']}")
    except (ValueError, IndexError):
        print("Invalid order index.")

# --------- Menu Printing Functions ---------
def print_main_menu():
    print("\n--- Main Menu ---")
    print("1. Products Menu")
    print("2. Couriers Menu")
    print("3. Orders Menu")
    print("0. Exit")

def print_products_menu():
    print("\n--- Products Menu ---")
    print("1. View Products")
    print("2. Add Product")
    print("3. Update Product")
    print("4. Delete Product")
    print("0. Return to Main Menu")

def print_couriers_menu():
    print("\n--- Couriers Menu ---")
    print("1. View Couriers")
    print("2. Add Courier")
    print("3. Update Courier")
    print("4. Delete Courier")
    print("0. Return to Main Menu")

def print_orders_menu():
    print("\n--- Orders Menu ---")
    print("1. View Orders")
    print("2. Create Order")
    print("3. Update Order Status")
    print("4. Update Order Info")
    print("5. Delete Order")
    print("0. Return to Main Menu")

# --------- Main ---------
def main():
    global products, couriers, orders
    products = load_products()
    couriers = load_couriers()
    orders = load_orders()

    while True:
        print_main_menu()
        choice = input("Choose an option: ").strip()
        if choice == "0":
            save_products(products)
            save_couriers(couriers)
            save_orders(orders)
            print("Goodbye!")
            break
        elif choice == "1":
            while True:
                print_products_menu()
                prod_choice = input("Choose an option: ").strip()
                if prod_choice == "0":
                    break
                elif prod_choice == "1":
                    view_list("Products", products, show_price=True)
                elif prod_choice == "2":
                    add_product(products)
                elif prod_choice == "3":
                    update_product(products)
                elif prod_choice == "4":
                    delete_product(products)
                else:
                    print("Invalid option.")
        elif choice == "2":
            while True:
                print_couriers_menu()
                courier_choice = input("Choose an option: ").strip()
                if courier_choice == "0":
                    break
                elif courier_choice == "1":
                    view_list("Couriers", couriers, show_phone=True)
                elif courier_choice == "2":
                    add_courier(couriers)
                elif courier_choice == "3":
                    update_courier(couriers)
                elif courier_choice == "4":
                    delete_courier(couriers)
                else:
                    print("Invalid option.")
        elif choice == "3":
            while True:
                print_orders_menu()
                order_choice = input("Choose an option: ").strip()
                if order_choice == "0":
                    break
                elif order_choice == "1":
                    view_orders(orders, couriers, products)
                elif order_choice == "2":
                    create_order(orders, couriers, products)
                elif order_choice == "3":
                    update_order_status(orders)
                elif order_choice == "4":
                    update_order_info(orders, couriers, products)
                elif order_choice == "5":
                    delete_order(orders)
                else:
                    print("Invalid option.")
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()