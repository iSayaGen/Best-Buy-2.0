from abc import ABC, abstractmethod


class Promotion(ABC):
    """Represent an abstract product promotion."""

    def __init__(self, name):
        """Create a promotion with a name."""
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity):
        """Return the price after applying the promotion."""
        pass


class PercentDiscount(Promotion):
    """Represent a percentage discount promotion."""

    def __init__(self, name, percent):
        """Create a percentage discount promotion."""
        super().__init__(name)

        if percent < 0 or percent > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")

        self.percent = percent

    def apply_promotion(self, product, quantity):
        """Return the price after applying the percentage discount."""
        discount = self.percent / 100
        return product.price * quantity * (1 - discount)


class SecondHalfPrice(Promotion):
    """Represent a promotion where every second item is half price."""

    def apply_promotion(self, product, quantity):
        """Return the price where every second item is half price."""
        full_price_items = (quantity + 1) // 2
        half_price_items = quantity // 2

        return (
            full_price_items * product.price
            + half_price_items * product.price / 2
        )


class ThirdOneFree(Promotion):
    """Represent a buy-two-get-one-free promotion."""

    def apply_promotion(self, product, quantity):
        """Return the price where every third item is free."""
        paid_quantity = quantity - quantity // 3
        return paid_quantity * product.price
