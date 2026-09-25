# models/order.py

from dataclasses import dataclass
from decimal import Decimal

from models.cart_item import CartItem


@dataclass
class Order:
    order_number: str
    items: list[CartItem]
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    status: str = "Received"