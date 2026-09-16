# models/menu_item.py

from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class MenuItem:
    item_id: int
    name: str
    category: str
    description: str
    base_price: Decimal
    available: bool
    allows_milk: bool