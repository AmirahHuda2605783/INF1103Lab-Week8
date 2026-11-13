"""Lab 8 test script: association, aggregation, composition, LSP, polymorphism.

Write your 'Predict first' answers BEFORE running each section.
"""
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


print("=== 2. ASSOCIATION: Supplier and Product ===")
supplier = Supplier("S001", "TechSource Ltd", "sales@techsource.com")
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 10, supplier, 2.5)
ebook = DigitalProduct("D001", "Python eBook", 25.00, 100, supplier, 15.0)

# PREDICT FIRST: after del supplier, can products still show supplier info?
del supplier
print("Variable 'supplier' deleted. Products still hold their own reference:")
laptop.get_supplier().display_information()
ebook.get_supplier().display_information()
print("Same Supplier object shared:", laptop.get_supplier() is ebook.get_supplier())

print("\n=== 3. AGGREGATION: Inventory and Product ===")
inventory_a = Inventory()
inventory_b = Inventory()
inventory_a.add_product(laptop)
inventory_a.add_product(ebook)

# PREDICT FIRST: does the product still work after removal from Inventory A?
removed = inventory_a.remove_product("P001")
print("Removed P001 from Inventory A:", removed)
print("Found in A after removal:", inventory_a.find_product("P001"))
print("Laptop still usable:", laptop.get_name(), laptop.get_stock())

inventory_b.add_product(laptop)
print("Same object now in Inventory B:",
      inventory_b.find_product("P001") is laptop)

print("\n=== 4. COMPOSITION: Order and OrderLine ===")
order1 = Order("O001")
order1.add_order_line(laptop, 2)
order1.add_order_line(ebook, 3)
order1.display_order()

# PREDICT FIRST: same Product in two orders -> how many OrderLines / Products?
order2 = Order("O002")
order2.add_order_line(laptop, 1)

line1 = order1.get_order_lines()[0]
line2 = order2.get_order_lines()[0]
print("OrderLine objects are different:", line1 is not line2)
print("Product objects are the same:", line1.get_product() is line2.get_product())

order1.remove_order_line("D001")
print("After removing D001 line, order1 total: "
      f"${order1.calculate_total():.2f}")
print("ebook Product still exists:", ebook.get_name())

print("\n=== 6. LSP: show_product_details works for any Product ===")
show_product_details(laptop)
print()
show_product_details(ebook)

print("\n=== 7. POLYMORPHISM: one collection, no isinstance ===")
inventory_c = Inventory()
inventory_c.add_product(laptop)
inventory_c.add_product(ebook)

# PREDICT FIRST: what will get_fulfilment_info() print for each product?
inventory_c.display_all()