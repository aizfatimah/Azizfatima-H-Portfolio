# Simple product list
products = ["Bubble Tea", "Pizza", "Dumplings", "Sandwiches"]

print("\nMain Menu")
print("1. View products")
print("2. Add a product")
print("3. Replace the first product")
print("4. Delete the last product")
print("0. Exit")

choice = input("Choose an option: ")

if choice == "0":
    print("Goodbye!")

elif choice == "1":
    print("\nProducts:")
    print(products)

elif choice == "2":
    new_product = input("Enter a new product: ")
    products.append(new_product)
    print("Updated products:", products)

elif choice == "3":
    new_name = input("Enter a new name to replace the first product: ")
    if products:
        products[0] = new_name
        print("Updated products:", products)
    else:
        print("No products to replace.")

elif choice == "4":
    if products:
        removed = products.pop()
        print(f"Removed '{removed}'. Updated products:", products)
    else:
        print("No products to delete.")

else:
    print("Invalid option.")
