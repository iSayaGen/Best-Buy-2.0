import pytest

from products import LimitedProduct
from products import Product
from store import Store


def test_store_total_quantity():
    products = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    ]

    store = Store(products)

    assert store.get_total_quantity() == 600


def test_store_returns_only_active_products():
    available_product = Product(
        "MacBook Air M2",
        price=1450,
        quantity=100
    )
    sold_out_product = Product(
        "Google Pixel 7",
        price=500,
        quantity=0
    )

    store = Store([available_product, sold_out_product])

    assert store.get_all_products() == [available_product]


def test_store_order_updates_stock_and_returns_total():
    product = Product("MacBook Air M2", price=1450, quantity=100)
    store = Store([product])

    total_price = store.order([(product, 2)])

    assert total_price == 2900
    assert product.get_quantity() == 98


def test_store_rejects_order_above_available_stock():
    product = Product("MacBook Air M2", price=1450, quantity=10)
    store = Store([product])

    with pytest.raises(ValueError):
        store.order([(product, 11)])

    assert product.get_quantity() == 10


def test_failed_order_does_not_change_any_product_stock():
    laptop = Product("MacBook Air M2", price=1450, quantity=100)
    shipping = LimitedProduct(
        "Shipping",
        price=10,
        quantity=250,
        maximum=1
    )

    store = Store([laptop, shipping])

    shopping_list = [
        (laptop, 5),
        (shipping, 2),
    ]

    with pytest.raises(ValueError):
        store.order(shopping_list)

    assert laptop.get_quantity() == 100
    assert shipping.get_quantity() == 250