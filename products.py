class Product:
    """Represent products that can be sold by the store."""

    def __init__(self, name, price, quantity):
        """Create a product with a name, price, and stock quantity."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty.")

        if price < 0:
            raise ValueError("Product price cannot be negative")

        if quantity < 0:
            raise ValueError("Product quantity cannot be negative")

        self.name = name.strip()
        self.price = price
        self.quantity = quantity
        self.active = quantity > 0

    def get_quantity(self):
        """Return the current quantity in stock."""
        return self.quantity

    def set_quantity(self, quantity):
        """Set the product quantity and deactivate it if sold out."""
        if quantity < 0:
            raise ValueError("Product quantity cannot be negative.")

        self.quantity = quantity

        if self.quantity == 0:
            self.deactivate()

    def is_active(self):
        """Return True if the product is available for purchase."""
        return self.active

    def activate(self):
        """Activate the product."""
        self.active = True

    def deactivate(self):
        """Deactivate the product."""
        self.active = False

    def show(self):
        """Print the product's information."""
        print(f"{self.name}, Price: {self.price}, Quantity: {self.quantity}")

    def buy(self, quantity):
        """Purchase a quantity of the product and return the total price."""
        if not self.active:
            raise ValueError("Product is sold out")

        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive.")

        if quantity > self.quantity:
            raise ValueError("Not enough items in stock")

        total_price = self.price * quantity
        self.set_quantity(self.quantity - quantity)

        return total_price


class NonStockedProduct(Product):
    """Represent a product that does not have physical stock."""

    def __init__(self, name, price):
        """Create a non-stocked product."""
        super().__init__(name, price, quantity=0)
        self.active = True

    def set_quantity(self, quantity):
        """Keep the quantity of a non-stocked product at zero."""
        self.quantity = 0

    def buy(self, quantity):
        """Purchase a non-stocked product without changing its quantity."""
        if not self.active:
            raise ValueError("Product is not available.")

        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive.")

        return self.price * quantity

    def show(self):
        """Print the non-stocked product's information."""
        print(
            f"{self.name}, Price: {self.price}")


class LimitedProduct(Product):
    """Represent a product with a maximum purchase quantity per order."""

    def __init__(self, name, price, quantity, maximum):
        """Create a limited product."""
        if maximum <= 0:
            raise ValueError("Maximum purchase quantity must be positive.")

        super().__init__(name, price, quantity)
        self.maximum = maximum

    def buy(self, quantity):
        """Purchase a limited quantity of the product."""
        if quantity > self.maximum:
            raise ValueError(
                f"Cannot purchase more than {self.maximum} of this product."
            )

        return super().buy(quantity)

    def show(self):
        """Print the limited product's information."""
        print(
            f"{self.name}, "
            f"Price: {self.price}, "
            f"Quantity: {self.quantity}, "
            f"Maximum: {self.maximum}"
        )