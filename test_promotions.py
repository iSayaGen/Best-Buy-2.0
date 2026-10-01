import pytest

from products import NonStockedProduct
from products import Product
from promotions import PercentDiscount
from promotions import Promotion
from promotions import SecondHalfPrice
from promotions import ThirdOneFree


def test_promotion_is_abstract():
    with pytest.raises(TypeError):
        Promotion("Test Promotion")


def test_percent_discount():
    product = Product("MacBook Air M2", price=1450, quantity=100)
    promotion = PercentDiscount("30% off!", percent=30)

    total_price = promotion.apply_promotion(product, 2)

    assert total_price == pytest.approx(2030)


def test_percent_discount_rejects_invalid_percentage():
    with pytest.raises(ValueError):
        PercentDiscount("Invalid", percent=-1)

    with pytest.raises(ValueError):
        PercentDiscount("Invalid", percent=101)


def test_second_half_price():
    product = Product("MacBook Air M2", price=1450, quantity=100)
    promotion = SecondHalfPrice("Second Half price!")

    assert promotion.apply_promotion(product, 1) == 1450
    assert promotion.apply_promotion(product, 2) == 2175
    assert promotion.apply_promotion(product, 3) == 3625
    assert promotion.apply_promotion(product, 4) == 4350


def test_third_one_free():
    product = Product(
        "Bose QuietComfort Earbuds",
        price=250,
        quantity=500
    )
    promotion = ThirdOneFree("Third One Free!")

    assert promotion.apply_promotion(product, 1) == 250
    assert promotion.apply_promotion(product, 2) == 500
    assert promotion.apply_promotion(product, 3) == 500
    assert promotion.apply_promotion(product, 4) == 750
    assert promotion.apply_promotion(product, 6) == 1000


def test_product_can_have_a_promotion():
    product = Product("MacBook Air M2", price=1450, quantity=100)
    promotion = SecondHalfPrice("Second Half price!")

    product.set_promotion(promotion)

    assert product.get_promotion() is promotion


def test_product_buy_uses_promotion():
    product = Product("MacBook Air M2", price=1450, quantity=100)
    promotion = SecondHalfPrice("Second Half price!")

    product.set_promotion(promotion)

    total_price = product.buy(2)

    assert total_price == 2175
    assert product.get_quantity() == 98


def test_non_stocked_product_buy_uses_promotion():
    product = NonStockedProduct("Windows License", price=125)
    promotion = PercentDiscount("30% off!", percent=30)

    product.set_promotion(promotion)

    total_price = product.buy(2)

    assert total_price == 175
    assert product.get_quantity() == 0