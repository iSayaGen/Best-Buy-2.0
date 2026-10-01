import pytest

from products import LimitedProduct
from products import NonStockedProduct
from products import Product


def test_create_product():
    product = Product("MacBook Air M2", price=1450, quantity=100)

    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    assert product.is_active()


def test_create_product_with_invalid_details():
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)

    with pytest.raises(ValueError):
        Product("   ", price=1450, quantity=100)

    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)

    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=1450, quantity=-1)


def test_product_becomes_inactive_when_quantity_reaches_zero():
    product = Product("MacBook Air M2", price=1450, quantity=1)

    product.buy(1)

    assert product.quantity == 0
    assert not product.is_active()


def test_product_purchase_modifies_quantity_and_returns_total_price():
    product = Product("MacBook Air M2", price=1450, quantity=100)

    total_price = product.buy(2)

    assert product.quantity == 98
    assert total_price == 2900


def test_buying_more_than_available_quantity_raises_exception():
    product = Product("MacBook Air M2", price=1450, quantity=10)

    with pytest.raises(ValueError):
        product.buy(11)


def test_buying_zero_or_negative_quantity_raises_exception():
    product = Product("MacBook Air M2", price=1450, quantity=10)

    with pytest.raises(ValueError):
        product.buy(0)

    with pytest.raises(ValueError):
        product.buy(-1)


def test_non_stocked_product_is_active_without_stock():
    product = NonStockedProduct("Windows License", price=125)

    assert product.is_active()
    assert not product.is_stocked()
    assert product.get_quantity() == 0


def test_non_stocked_product_can_be_purchased_without_changing_quantity():
    product = NonStockedProduct("Windows License", price=125)

    total_price = product.buy(3)

    assert total_price == 375
    assert product.get_quantity() == 0
    assert product.is_active()


def test_limited_product_rejects_quantity_above_maximum():
    product = LimitedProduct(
        "Shipping",
        price=10,
        quantity=250,
        maximum=1
    )

    with pytest.raises(ValueError):
        product.buy(2)

    assert product.get_quantity() == 250


def test_limited_product_allows_quantity_up_to_maximum():
    product = LimitedProduct(
        "Shipping",
        price=10,
        quantity=250,
        maximum=1
    )

    total_price = product.buy(1)

    assert total_price == 10
    assert product.get_quantity() == 249


def test_limited_product_rejects_invalid_maximum():
    with pytest.raises(ValueError):
        LimitedProduct(
            "Shipping",
            price=10,
            quantity=250,
            maximum=0
        )