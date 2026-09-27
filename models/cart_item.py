# models/cart_item.py

from dataclasses import dataclass, field
from decimal import Decimal
from uuid import uuid4

@dataclass
class CartItem:
    item_id: int
    name: str
    size: str
    milk: str | None
    unit_price: Decimal
    quantity: int = 1
    line_id: str = field(
        default_factory=lambda: uuid4().hex
    )