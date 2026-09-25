# services/order_service.py

from decimal import Decimal
from uuid import uuid4

from models.cart_item import CartItem
from models.order import Order
from services.cart_service import CartService


class OrderService:
    def __init__(self, cart_service: CartService):
        self.cart_service = cart_service

    def submit_order(
            self,
            cart: list[CartItem],
            tax_rate: Decimal,
    ) -> Order:
        if not cart:
            raise ValueError("Cannot submit an empty order.")

        subtotal = self.cart_service.calculate_subtotal(cart)
        tax = self.cart_service.calculate_tax(cart, tax_rate)
        total = self.cart_service.calculate_total(cart, tax_rate)

        return Order(
            order_number=f"PC-{uuid4().hex[:8].upper()}",
            items=list(cart),
            subtotal=subtotal,
            tax=tax,
            total=total,
        )