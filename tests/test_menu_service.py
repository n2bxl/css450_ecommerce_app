# tests/test_menu_service.py

from decimal import Decimal

from models.menu_item import MenuItem
from services.menu_service import MenuService


class FakeMenuRepository:
    def get_all(self):
        return [
            MenuItem(
                item_id=1,
                name="Latte",
                category="Espresso",
                description="Test latte",
                base_price=Decimal("4.25"),
                available=True,
                allows_milk=True,
            ),
            MenuItem(
                item_id=2,
                name="Hidden Drink",
                category="Test",
                description="Unavailable item",
                base_price=Decimal("3.00"),
                available=False,
                allows_milk=False,
            ),
        ]


def test_get_available_menu_excludes_unavailable_items():
    service = MenuService(FakeMenuRepository())

    menu = service.get_available_menu()

    assert len(menu) == 1
    assert menu[0].name == "Latte"