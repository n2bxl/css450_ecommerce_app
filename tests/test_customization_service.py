# tests/test_customization_service.py

from decimal import Decimal

from models.menu_item import MenuItem
from services.customization_service import CustomizationService


def make_menu_item():
    return MenuItem(
        item_id=1,
        name="Caffe Latte",
        category="Espresso",
        description="Espresso with steamed milk",
        base_price=Decimal("4.25"),
        available=True,
        allows_milk=True,
    )


def test_small_size_uses_base_price():
    service = CustomizationService()
    item = make_menu_item()

    price = service.calculate_price(item, "Small")

    assert price == Decimal("4.25")


def test_medium_size_adds_fifty_cents():
    service = CustomizationService()
    item = make_menu_item()

    price = service.calculate_price(item, "Medium")

    assert price == Decimal("4.75")


def test_large_size_adds_one_dollar():
    service = CustomizationService()
    item = make_menu_item()

    price = service.calculate_price(item, "Large")

    assert price == Decimal("5.25")