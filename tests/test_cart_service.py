# tests/test_cart_service.py

from decimal import Decimal

import pytest

from models.cart_item import CartItem
from services.cart_service import CartService


def make_cart_item(
    quantity: int = 1,
    unit_price: Decimal = Decimal("5.25"),
) -> CartItem:
    return CartItem(
        item_id=1,
        name="Caffe Latte",
        size="Large",
        milk="Oatmilk",
        unit_price=unit_price,
        quantity=quantity,
    )


def test_calculate_item_total():
    service = CartService()
    item = make_cart_item(quantity=2)

    total = service.calculate_item_total(item)

    assert total == Decimal("10.50")


def test_calculate_subtotal_for_multiple_items():
    service = CartService()
    cart = [
        make_cart_item(
            quantity=2,
            unit_price=Decimal("5.25"),
        ),
        CartItem(
            item_id=2,
            name="Cold Brew",
            size="Medium",
            milk=None,
            unit_price=Decimal("4.50"),
            quantity=1,
        ),
    ]

    subtotal = service.calculate_subtotal(cart)

    assert subtotal == Decimal("15.00")


def test_empty_cart_subtotal_is_zero():
    service = CartService()

    subtotal = service.calculate_subtotal([])

    assert subtotal == Decimal("0.00")


def test_increase_quantity():
    service = CartService()
    item = make_cart_item()

    service.increase_quantity(item)

    assert item.quantity == 2


def test_decrease_quantity():
    service = CartService()
    item = make_cart_item(quantity=2)

    service.decrease_quantity(item)

    assert item.quantity == 1


def test_quantity_does_not_drop_below_one():
    service = CartService()
    item = make_cart_item(quantity=1)

    service.decrease_quantity(item)

    assert item.quantity == 1


def test_remove_item():
    service = CartService()
    item = make_cart_item()
    cart = [item]

    service.remove_item(cart, item)

    assert cart == []


def test_calculate_tax():
    service = CartService()
    cart = [
        make_cart_item(
            quantity=2,
            unit_price=Decimal("5.00"),
        ),
    ]

    tax = service.calculate_tax(
        cart,
        Decimal("0.10"),
    )

    assert tax == Decimal("1.00")


def test_calculate_total_includes_tax():
    service = CartService()
    cart = [
        make_cart_item(
            quantity=2,
            unit_price=Decimal("5.00"),
        ),
    ]

    total = service.calculate_total(
        cart,
        Decimal("0.10"),
    )

    assert total == Decimal("11.00")


def test_zero_tax_rate():
    service = CartService()
    cart = [
        make_cart_item(
            unit_price=Decimal("5.25"),
        ),
    ]

    tax = service.calculate_tax(
        cart,
        Decimal("0.00"),
    )

    assert tax == Decimal("0.00")


def test_rejects_invalid_tax_rate():
    service = CartService()
    cart = [make_cart_item()]

    with pytest.raises(ValueError):
        service.calculate_tax(
            cart,
            Decimal("1.01"),
        )