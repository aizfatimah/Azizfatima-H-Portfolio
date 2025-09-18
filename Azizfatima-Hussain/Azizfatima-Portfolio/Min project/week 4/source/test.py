import csv

COURIERS_FILE = r"C:\Users\AzizfatimaH(DE-X6-LM\Documents\Data-Engineeringreal\Azizfatima-Portfolio\Min project\week 4\data\couriers.csv"

def load_couriers(filename=COURIERS_FILE):
    couriers = []
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                couriers.append({'name': row['name'].strip(), 'phone': row['phone'].strip()})
    except FileNotFoundError:
        pass
    return couriers

def save_couriers(couriers, filename=COURIERS_FILE):
    with open(filename, mode='w', newline='') as file:
        fieldnames = ['name', 'phone']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for c in couriers:
            writer.writerow(c)

def view_list(title, lst, show_phone=False):
    print(f"\n--- {title} List ---")
    if not lst:
        print(f"No {title.lower()} available.")
        return
    for i, item in enumerate(lst):
        if show_phone:
            print(f"{i}: {item['name']} - Phone: {item['phone']}")
        else:
            print(f"{i}: {item}")

def print_couriers_menu():
    print("\n--- COURIERS MENU ---")
    print("1. View Couriers")
    print("2. Add Courier")
    print("3. Update Courier")
    print("4. Delete Courier")
    print("0. Return to Main Menu")

def add_courier(couriers):
    name = input("Enter courier name: ").strip()
    phone = input("Enter courier phone: ").strip()
    if name and phone:
        couriers.append({'name': name, 'phone': phone})
        print(f"Courier '{name}' added.")
    else:
        print("Name and phone cannot be empty.")

def update_courier(couriers):
    if not couriers:
        print("No couriers to update.")
        return
    view_list("Couriers", couriers, show_phone=True)
    try:
        idx = int(input("Enter courier index to update: "))
        if idx < 0 or idx >= len(couriers):
            print("Invalid index.")
            return
    except ValueError:
        print("Invalid input.")
        return
    name = input(f"Enter new name (leave blank to keep '{couriers[idx]['name']}'): ").strip()
    phone = input(f"Enter new phone (leave blank to keep '{couriers[idx]['phone']}'): ").strip()
    if name:
        couriers[idx]['name'] = name
    if phone:
        couriers[idx]['phone'] = phone
    print("Courier updated.")

def delete_courier(couriers):
    if not couriers:
        print("No couriers to delete.")
        return
    view_list("Couriers", couriers, show_phone=True)
    try:
        idx = int(input("Enter courier index to delete: "))
        if idx < 0 or idx >= len(couriers):
            print("Invalid index.")
            return
    except ValueError:
        print("Invalid input.")
        return
    removed = couriers.pop(idx)
    print(f"Courier '{removed['name']}' deleted.")

def handle_couriers_menu(couriers):
    while True:
        print_couriers_menu()
        choice = input("Choose a courier option: ").strip()
        if choice == "1":
            view_list("Couriers", couriers, show_phone=True)
        elif choice == "2":
            add_courier(couriers)
        elif choice == "3":
            update_courier(couriers)
        elif choice == "4":
            delete_courier(couriers)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")

def print_main_menu():
    print("\n--- MAIN MENU ---")
    print("1. Products Menu")
    print("2. Couriers Menu")
    print("3. Orders Menu")
    print("0. Save & Exit")

def main():
    couriers = load_couriers()
    while True:
        print_main_menu()
        choice = input("Choose an option: ").strip()
        if choice == "2":
            handle_couriers_menu(couriers)
        elif choice == "0":
            print("Saving couriers and exiting...")
            save_couriers(couriers)
            break
        else:
            print("Option not implemented or invalid. Try again.")

if __name__ == "__main__":
    main()
