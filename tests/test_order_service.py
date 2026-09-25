# tests/test_order_service.py

from decimal import Decimal

import pytest

from models.cart_item import CartItem
from services.cart_service import CartService
from services.order_service import OrderService


def make_cart():
    return [
        CartItem(
            item_id=1,
            name="Caffe Latte",
            size="Large",
            milk="Oatmilk",
            unit_price=Decimal("5.25"),
            quantity=2,
        )
    ]


def test_submit_order():
    service = OrderService(CartService())
    cart = make_cart()

    order = service.submit_order(
        cart,
        Decimal("0.10"),
    )

    assert order.items == cart
    assert order.subtotal == Decimal("10.50")
    assert order.tax == Decimal("1.05")
    assert order.total == Decimal("11.55")
    assert order.status == "Received"
    assert order.order_number.startswith("PC-")


def test_submit_order_preserves_customizations():
    service = OrderService(CartService())
    cart = make_cart()

    order = service.submit_order(
        cart,
        Decimal("0.10"),
    )

    item = order.items[0]

    assert item.name == "Caffe Latte"
    assert item.size == "Large"
    assert item.milk == "Oatmilk"
    assert item.quantity == 2


def test_submit_order_rejects_empty_cart():
    service = OrderService(CartService())

    with pytest.raises(ValueError):
        service.submit_order(
            [],
            Decimal("0.10"),
        )