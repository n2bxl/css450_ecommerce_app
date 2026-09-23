# services/cart_service.py

from decimal import Decimal, ROUND_HALF_UP

from models.cart_items import CartItem

class CartService:
    def calculate_item_total(
            self,
            item: CartItem,
    ) -> Decimal:
        return item.unit_price * item.quantity

    def calculate_subtotal(
            self,
            cart: list[CartItem],
    ) -> Decimal:
        return sum(
            (
                self.calculate_item_total(item)
                for item in cart
            ),
            start=Decimal("0.00")
        )

    def calculate_tax(
            self,
            cart: list[CartItem],
            tax_rate: Decimal
    ) -> Decimal:
        if tax_rate < Decimal("0") or tax_rate > Decimal("1"):
            raise ValueError("Tax rate must be between 0 and 1.")

        subtotal = self.calculate_subtotal(cart)

        return (subtotal * tax_rate).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    def calculate_total(
            self,
            cart: list[CartItem],
            tax_rate: Decimal,
    ) -> Decimal:
        subtotal = self.calculate_subtotal(cart)
        tax = self.calculate_tax(cart, tax_rate)

        return subtotal + tax

    def increase_quantity(
            self,
            item: CartItem,
    ) -> None:
        item.quantity += 1

    def decrease_quantity(
            self,
            item: CartItem,
    ) -> None:
        if item.quantity > 1:
            item.quantity -= 1

    def remove_item(
            self,
            cart: list[CartItem],
            item: CartItem,
    ) -> None:
        cart.remove(item)