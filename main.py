import json
import os

from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

INVENTORY_FILE = "inventory.json"


def get_or_create_supplier(suppliers: dict[str, Supplier], data: dict) -> Supplier:
    """Reuse a Supplier already loaded so products share one object."""
    supplier_id = data["id"]
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, data["name"],
                                          data["contact_email"])
    return suppliers[supplier_id]


def load_inventory(suppliers: dict[str, Supplier]) -> Inventory:
    inventory = Inventory()

    if os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} found.")

        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)

        for item in data:
            supplier = get_or_create_supplier(suppliers, item["supplier"])

            if item["type"] == "physical":
                product: Product = PhysicalProduct(
                    item["id"], item["name"], item["price"],
                    item["stock"], supplier, item["weight"]
                )
            elif item["type"] == "digital":
                product = DigitalProduct(
                    item["id"], item["name"], item["price"],
                    item["stock"], supplier, item["download_size"]
                )
            else:
                print(f"Unknown product type for {item['id']}. Skipping.")
                continue

            inventory.add_product(product)

        print("Inventory loaded successfully.")
    else:
        print(f"{INVENTORY_FILE} not found.")
        print("Starting with an empty inventory.")

    return inventory


def save_inventory(inventory: Inventory) -> None:
    print("Saving inventory...")

    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory.get_all_products(), file, indent=4)

    print(f"Inventory saved successfully to {INVENTORY_FILE}.")


def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier:
    """Pick an existing supplier or create a new independent one."""
    supplier_id = input("Supplier ID: ")

    if supplier_id in suppliers:
        print("Existing supplier selected.")
        return suppliers[supplier_id]

    name = input("Supplier Name: ")
    email = input("Supplier Contact Email: ")
    supplier = Supplier(supplier_id, name, email)
    suppliers[supplier_id] = supplier
    print("New supplier created.")
    return supplier


def show_product_details(product: Product) -> None:
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")


def create_order(inventory: Inventory) -> Order | None:
    order_id = input("Order ID: ")
    order = Order(order_id)

    while True:
        product_id = input("Product ID to add (or press Enter to finish): ")
        if product_id == "":
            break

        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue

        quantity = int(input("Quantity: "))
        order.add_order_line(product, quantity)
        print("Order line added.")

    if len(order.get_order_lines()) == 0:
        print("No order lines added. Order discarded.")
        return None

    return order


def main() -> None:
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")

    suppliers: dict[str, Supplier] = {}
    orders: list[Order] = []
    inventory = load_inventory(suppliers)

    while True:
        print("----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Remove Product")
        print("6. Display Suppliers")
        print("7. Create Order")
        print("8. Display Orders")
        print("9. Save Inventory")
        print("10. Exit")
        print("----------------------------")

        option = input("Enter option: ")

        if option == "1":
            inventory.display_all()

        elif option == "2":
            print("Add New Product")
            product_id = input("Product ID: ")

            if inventory.find_product(product_id) is not None:
                print("Product ID already exists.")
                continue

            product_name = input("Product Name: ")
            price = float(input("Price: "))
            stock = int(input("Stock Quantity: "))
            supplier = choose_supplier(suppliers)

            print("Select Product Type:")
            print("1. Physical Product")
            print("2. Digital Product")
            product_type = input("Enter option: ")

            if product_type == "1":
                weight = float(input("Weight (kg): "))
                product = PhysicalProduct(product_id, product_name, price,
                                          stock, supplier, weight)
                print("Physical product created successfully!")
            elif product_type == "2":
                download_size = float(input("Download Size (MB): "))
                product = DigitalProduct(product_id, product_name, price,
                                         stock, supplier, download_size)
                print("Digital product created successfully!")
            else:
                print("Invalid product type.")
                continue

            inventory.add_product(product)
            print("Product added successfully!")

        elif option == "3":
            print("Update Stock")
            product_id = input("Enter Product ID: ")
            found = inventory.find_product(product_id)

            if found is not None:
                print("Product Found:")
                print(f"Name: {found.get_name()}")
                print(f"Current Stock: {found.get_stock()}")
                new_stock = int(input("New Stock Quantity: "))
                found.update_stock(new_stock)
                print("Stock updated successfully!")
            else:
                print("Product not found.")

        elif option == "4":
            print("Search Product")
            product_id = input("Enter Product ID: ")
            found = inventory.find_product(product_id)

            if found is not None:
                print("Product Found")
                print("------------------------------------------------")
                show_product_details(found)
                print("------------------------------------------------")
            else:
                print("Product not found.")

        elif option == "5":
            product_id = input("Enter Product ID to remove: ")
            if inventory.remove_product(product_id):
                print("Product removed from inventory.")
            else:
                print("Product not found.")

        elif option == "6":
            if len(suppliers) == 0:
                print("No suppliers yet.")
            for supplier in suppliers.values():
                supplier.display_information()
                print("------------------------------------------------")

        elif option == "7":
            order = create_order(inventory)
            if order is not None:
                orders.append(order)
                order.display_order()

        elif option == "8":
            if len(orders) == 0:
                print("No orders created this session.")
            for order in orders:
                order.display_order()

        elif option == "9":
            save_inventory(inventory)

        elif option == "10":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()