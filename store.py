class Store:
    """Represent a store containing products."""

    def __init__(self, product_list):
        """Create a store containing the provided products."""
        self.products = product_list[:]

    def add_product(self, product):
        """Add a product to the store."""
        self.products.append(product)

    def remove_product(self, product):
        """Remove a product from the store."""
        self.products.remove(product)

    def get_total_quantity(self):
        """Return the total quantity of all products in the store."""
        return sum(product.get_quantity() for product in self.products)

    def get_all_products(self):
        """Return all active products in the store."""
        return [product for product in self.products if product.is_active()]

    def order(self, shopping_list):
        """Process an order and return its total price."""
        quantities = {}

        # Validate the complete order before changing any stock.
        for product, quantity in shopping_list:
            if not product.is_active():
                raise ValueError(f"{product.name} is sold out.")

            if quantity <= 0:
                raise ValueError("Purchase quantity must be positive.")

            quantities[product] = quantities.get(product, 0) + quantity

        for product, quantity in quantities.items():
            if quantity > product.get_quantity():
                raise ValueError(f"Not enough {product.name} in stock.")

        # All products have enough stock, so the order can be processed.
        total = 0

        for product, quantity in shopping_list:
            total += product.buy(quantity)

        return total
