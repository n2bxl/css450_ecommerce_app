# models/cart_item.py

from dataclasses import dataclass
from decimal import Decimal

@dataclass
class CartItem:
    item_id: int
    name: str
    size: str
    milk: str | None
    unit_price: Decimal
    quantity: int = 1