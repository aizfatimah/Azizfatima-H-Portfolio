
import os

# --------- Constants ---------
PRODUCTS_FILE = r"C:\Users\AzizfatimaH(DE-X6-LM\Documents\Data-Engineeringreal\Azizfatima-Portfolio\Min project\Week 3\data\products.txt"
COURIERS_FILE = r"C:\Users\AzizfatimaH(DE-X6-LM\Documents\Data-Engineeringreal\Azizfatima-Portfolio\Min project\Week 3\data\couriers.txt"

ORDER_STATUS_OPTIONS = ["preparing", "dispatched", "delivered"]

# --------- File Handling ---------
def load_list_from_file(filename):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []

def save_list_to_file(filename, data_list):
    with open(filename, "w") as f:
        for item in data_list:
            f.write(f"{item}\n")

# --------- Display Functions ---------
def view_list(title, data_list):
    print(f"\n{title}:")
    if not data_list:
        print("  (empty)")
    for i, item in enumerate(data_list):
        print(f"  {i}. {item}")

def view_orders(orders):
    print("\nOrders List:")
    if not orders:
        print("  (no orders)")
    for i, order in enumerate(orders):
        courier_name = couriers[order['courier']] if 0 <= order['courier'] < len(couriers) else "Unknown"
        print(f"  {i}. {order['customer_name']} | {order['customer_address']} | {order['customer_phone']} | Courier: {courier_name} | Status: {order['status']}")

# --------- Products Functions ---------
def add_product(products):
    name = input("Enter new product name: ").strip()
    if name:
        products.append(name)
        save_list_to_file(PRODUCTS_FILE, products)
        print("Product added.")
    else:
        print("Product name cannot be empty.")

def update_product(products):
    view_list("Products", products)
    try:
        index = int(input("Enter product index to update: "))
        if index < 0 or index >= len(products):
            raise IndexError
        new_name = input("Enter new product name: ").strip()
        if new_name:
            products[index] = new_name
            save_list_to_file(PRODUCTS_FILE, products)
            print("Product updated.")
        else:
            print("Product name cannot be empty.")
    except (ValueError, IndexError):
        print("Invalid product index.")

def delete_product(products):
    view_list("Products", products)
    try:
        index = int(input("Enter product index to delete: "))
        if index < 0 or index >= len(products):
            raise IndexError
        removed = products.pop(index)
        save_list_to_file(PRODUCTS_FILE, products)
        print(f"Deleted product: {removed}")
    except (ValueError, IndexError):
        print("Invalid product index.")

# --------- Couriers Functions ---------
def add_courier(couriers):
    name = input("Enter new courier name: ").strip()
    if name:
        couriers.append(name)
        save_list_to_file(COURIERS_FILE, couriers)
        print("Courier added.")
    else:
        print("Courier name cannot be empty.")

def update_courier(couriers):
    view_list("Couriers", couriers)
    try:
        index = int(input("Enter courier index to update: "))
        if index < 0 or index >= len(couriers):
            raise IndexError
        new_name = input("Enter new courier name: ").strip()
        if new_name:
            couriers[index] = new_name
            save_list_to_file(COURIERS_FILE, couriers)
            print("Courier updated.")
        else:
            print("Courier name cannot be empty.")
    except (ValueError, IndexError):
        print("Invalid courier index.")

def delete_courier(couriers):
    view_list("Couriers", couriers)
    try:
        index = int(input("Enter courier index to delete: "))
        if index < 0 or index >= len(couriers):
            raise IndexError
        removed = couriers.pop(index)
        save_list_to_file(COURIERS_FILE, couriers)
        print(f"Deleted courier: {removed}")
    except (ValueError, IndexError):
        print("Invalid courier index.")

# --------- Orders Functions ---------
def create_order(orders, couriers):
    name = input("Customer name: ").strip()
    address = input("Customer address: ").strip()
    phone = input("Customer phone: ").strip()
    if not (name and address and phone):
        print("Customer info cannot be empty.")
        return

    view_list("Couriers", couriers)
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
        "status": "preparing"
    }
    orders.append(order)
    print("Order created.")

def update_order_status(orders):
    if not orders:
        print("No orders to update.")
        return
    view_orders(orders)
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

def update_order_info(orders, couriers):
    if not orders:
        print("No orders to update.")
        return
    view_orders(orders)
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

        view_list("Couriers", couriers)
        new_courier = input(f"Courier index (current: {order['courier']}): ").strip()
        if new_courier:
            new_courier_index = int(new_courier)
            if 0 <= new_courier_index < len(couriers):
                order["courier"] = new_courier_index
            else:
                print("Invalid courier index. Courier not updated.")
        print("Order updated.")
    except (ValueError, IndexError):
        print("Invalid input.")

def delete_order(orders):
    if not orders:
        print("No orders to delete.")
        return
    view_orders(orders)
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
    products = load_list_from_file(PRODUCTS_FILE)
    couriers = load_list_from_file(COURIERS_FILE)
    orders = []

    # Debug info for files (optional)
    print(f"Products file found? {os.path.exists(PRODUCTS_FILE)}")
    print(f"Couriers file found? {os.path.exists(COURIERS_FILE)}")

    while True:
        print_main_menu()
        choice = input("Choose an option: ").strip()
        if choice == "0":
            save_list_to_file(PRODUCTS_FILE, products)
            save_list_to_file(COURIERS_FILE, couriers)
            print("Goodbye!")
            break
        elif choice == "1":
            while True:
                print_products_menu()
                prod_choice = input("Choose an option: ").strip()
                if prod_choice == "0":
                    break
                elif prod_choice == "1":
                    view_list("Products", products)
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
                    view_list("Couriers", couriers)
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
                    view_orders(orders)
                elif order_choice == "2":
                    create_order(orders, couriers)
                elif order_choice == "3":
                    update_order_status(orders)
                elif order_choice == "4":
                    update_order_info(orders, couriers)
                elif order_choice == "5":
                    delete_order(orders)
                else:
                    print("Invalid option.")
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
