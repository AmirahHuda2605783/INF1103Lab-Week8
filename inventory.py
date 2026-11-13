from product import Product


class Inventory:
    """Aggregation: an Inventory groups Product objects but does not
    create them or control their lifecycle. Products can be removed and
    moved to another Inventory without being destroyed.
    """

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self) -> None:
        print("Current Inventory")
        print("------------------------------------------------")

        if len(self.__products) == 0:
            print("Inventory is empty.")

        for product in self.__products:
            product.display_information()
            print(f"Fulfilment: {product.get_fulfilment_info()}")
            print("------------------------------------------------")

    def get_all_products(self) -> list[dict]:
        return [product.to_dict() for product in self.__products]