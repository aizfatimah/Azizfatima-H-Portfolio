def view_list(title, data_list):
    print(f"\n{title}:")
    for index, item in enumerate(data_list):
        print(f"{index}. {item}")

def add_product(products):
    name = input("Enter new product name: ")
    products.append(name)
    print("Product added.")

def update_product(products):
    view_list("Products", products)
    try:
        index = int(input("Enter product index to update: "))
        new_name = input("Enter new product name: ")
        products[index] = new_name
        print("Product updated.")
    except (ValueError, IndexError):
        print("Invalid input.")

def delete_product(products):
    view_list("Products", products)
    try:
        index = int(input("Enter product index to delete: "))
        print(f"Deleted: {products.pop(index)}")
    except (ValueError, IndexError):
        print("Invalid input.")
