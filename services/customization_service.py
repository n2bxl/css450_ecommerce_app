# services/customization_service.py

from decimal import Decimal

from models.menu_item import MenuItem


class CustomizationService:
    SIZE_ADJUSTMENTS = {
        "Small": Decimal("0.00"),
        "Medium": Decimal("0.50"),
        "Large": Decimal("1.00"),
    }

    def calculate_price(
        self,
        item: MenuItem,
        size: str,
    ) -> Decimal:
        return item.base_price + self.SIZE_ADJUSTMENTS[size]