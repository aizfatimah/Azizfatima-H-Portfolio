def view_orders(orders):
    print("\nOrders List:")
    for index, order in enumerate(orders):
        print(f"{index}. {order}")

def create_order(orders, couriers):
    name = input("Customer name: ")
    address = input("Customer address: ")
    phone = input("Customer phone: ")
    
    print("\nCouriers:")
    for i, courier in enumerate(couriers):
        print(f"{i}. {courier}")

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

def update_order_status(orders, order_status_options):
    view_orders(orders)
    try:
        order_index = int(input("Enter order index: "))
        for i, status in enumerate(order_status_options):
            print(f"{i}. {status}")
        status_index = int(input("Choose new status index: "))
        orders[order_index]["status"] = order_status_options[status_index]
        print("Order status updated.")
    except (ValueError, IndexError):
        print("Invalid input.")

def update_order_info(orders, couriers):
    view_orders(orders)
    try:
        index = int(input("Enter order index to update: "))
        for key in ["customer_name", "customer_address", "customer_phone"]:
            current = orders[index][key]
            new_value = input(f"{key.replace('_', ' ').title()} (current: {current}): ")
            if new_value:
                orders[index][key] = new_value

        print("\nCouriers:")
        for i, courier in enumerate(couriers):
            print(f"{i}. {courier}")

        new_courier = input(f"Courier index (current: {orders[index]['courier']}): ")
        if new_courier:
            orders[index]["courier"] = int(new_courier)
        print("Order updated.")
    except (ValueError, IndexError):
        print("Invalid input.")

def delete_order(orders):
    view_orders(orders)
    try:
        index = int(input("Enter order index to delete: "))
        print(f"Deleted order for {orders.pop(index)['customer_name']}")
    except (ValueError, IndexError):
        print("Invalid input.")
