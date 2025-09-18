def load_list_from_file(filename):
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def save_list_to_file(filename, data_list):
    with open(filename, "w") as file:
        for item in data_list:
            file.write(f"{item}\n")

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

def view_list(title, data_list):
    print(f"\n{title}:")
    for i, item in enumerate(data_list):
        print(f"{i}. {item}")

def view_orders(orders):
    print("\nOrders List:")
    for i, order in enumerate(orders):
        print(f"{i}. {order}")

def products_menu(products):
    while True:
        print_products_menu()
        choice = input("Choose an option: ")
        if choice == "0":
            break
        elif choice == "1":
            view_list("Products", products)
        elif choice == "2":
            name = input("Enter new product name: ")
            products.append(name)
            print("Product added.")
        elif choice == "3":
            view_list("Products", products)
            try:
                idx = int(input("Enter product index to update: "))
                new_name = input("Enter new product name: ")
                products[idx] = new_name
                print("Product updated.")
            except (ValueError, IndexError):
                print("Invalid input.")
        elif choice == "4":
            view_list("Products", products)
            try:
                idx = int(input("Enter product index to delete: "))
                deleted = products.pop(idx)
                print(f"Deleted product: {deleted}")
            except (ValueError, IndexError):
                print("Invalid input.")
        else:
            print("Invalid option.")

def couriers_menu(couriers):
    while True:
        print_couriers_menu()
        choice = input("Choose an option: ")
        if choice == "0":
            break
        elif choice == "1":
            view_list("Couriers", couriers)
        elif choice == "2":
            name = input("Enter new courier name: ")
            couriers.append(name)
            print("Courier added.")
        elif choice == "3":
            view_list("Couriers", couriers)
            try:
                idx = int(input("Enter courier index to update: "))
                new_name = input("Enter new courier name: ")
                couriers[idx] = new_name
                print("Courier updated.")
            except (ValueError, IndexError):
                print("Invalid input.")
        elif choice == "4":
            view_list("Couriers", couriers)
            try:
                idx = int(input("Enter courier index to delete: "))
                deleted = couriers.pop(idx)
                print(f"Deleted courier: {deleted}")
            except (ValueError, IndexError):
                print("Invalid input.")
        else:
            print("Invalid option.")

def orders_menu(orders, couriers, order_status_options):
    while True:
        print_orders_menu()
        choice = input("Choose an option: ")
        if choice == "0":
            break
        elif choice == "1":
            view_orders(orders)
        elif choice == "2":
            customer_name = input("Customer name: ")
            customer_address = input("Customer address: ")
            customer_phone = input("Customer phone: ")
            view_list("Couriers", couriers)
            try:
                courier_idx = int(input("Choose courier index: "))
                if courier_idx < 0 or courier_idx >= len(couriers):
                    raise IndexError
            except (ValueError, IndexError):
                print("Invalid courier selection.")
                continue
            order = {
                "customer_name": customer_name,
                "customer_address": customer_address,
                "customer_phone": customer_phone,
                "courier": courier_idx,
                "status": "PREPARING"
            }
            orders.append(order)
            print("Order created.")
        elif choice == "3":
            view_orders(orders)
            try:
                order_idx = int(input("Enter order index: "))
                view_list("Order Status Options", order_status_options)
                status_idx = int(input("Choose new status index: "))
                orders[order_idx]["status"] = order_status_options[status_idx]
                print("Order status updated.")
            except (ValueError, IndexError):
                print("Invalid input.")
        elif choice == "4":
            view_orders(orders)
            try:
                order_idx = int(input("Enter order index to update: "))
                order = orders[order_idx]
                for key in ["customer_name", "customer_address", "customer_phone"]:
                    current = order[key]
                    new_val = input(f"{key.replace('_', ' ').title()} (current: {current}): ")
                    if new_val.strip():
                        order[key] = new_val.strip()
                view_list("Couriers", couriers)
                new_courier = input(f"Courier index (current: {order['courier']}): ")
                if new_courier.strip():
                    order["courier"] = int(new_courier)
                print("Order updated.")
            except (ValueError, IndexError):
                print("Invalid input.")
        elif choice == "5":
            view_orders(orders)
            try:
                order_idx = int(input("Enter order index to delete: "))
                deleted_order = orders.pop(order_idx)
                print(f"Deleted order for {deleted_order['customer_name']}")
            except (ValueError, IndexError):
                print("Invalid input.")
        else:
            print("Invalid option.")

def main():
    products = load_list_from_file("products.txt")
    couriers = load_list_from_file("couriers.txt")
    orders = []
    order_status_options = ["PREPARING", "DISPATCHED", "DELIVERED"]

    while True:
        print_main_menu()
        choice = input("Choose an option: ")
        if choice == "0":
            save_list_to_file("products.txt", products)
            save_list_to_file("couriers.txt", couriers)
            print("Goodbye!")
            break
        elif choice == "1":
            products_menu(products)
        elif choice == "2":
            couriers_menu(couriers)
        elif choice == "3":
            orders_menu(orders, couriers, order_status_options)
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
