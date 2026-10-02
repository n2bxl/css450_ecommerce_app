# app.py

from decimal import Decimal

import streamlit as st

from models.cart_item import CartItem

from repositories.menu_repository import MenuRepository

from services.cart_service import CartService
from services.customization_service import CustomizationService
from services.menu_service import MenuService
from services.order_service import OrderService


st.set_page_config(
    page_title="Phoenix Coffee Co.",
    page_icon="☕️",
)


if "cart" not in st.session_state:
    st.session_state.cart = []

if "current_view" not in st.session_state:
    st.session_state.current_view = "menu"

ORDER_TAX_RATE = Decimal("0.10")


if "selected_item_id" not in st.session_state:
    st.session_state.selected_item_id = None

if "selected_size" not in st.session_state:
    st.session_state.selected_size = None

if "selected_milk" not in st.session_state:
    st.session_state.selected_milk = None

if "configured_item" not in st.session_state:
    st.session_state.configured_item = None

if "submitted_order" not in st.session_state:
    st.session_state.submitted_order = None


def reset_customization():
    st.session_state.selected_item_id = None
    st.session_state.selected_size = None
    st.session_state.selected_milk = None
    st.session_state.configured_item = None


def add_configured_item_to_cart():
    configured = st.session_state.configured_item

    if configured is None:
        return

    cart_item = CartItem(
        item_id=configured["item_id"],
        name=configured["name"],
        size=configured["size"],
        milk=configured["milk"],
        unit_price=configured["price"],
        quantity=1,
    )

    cart_service.add_item(
        st.session_state.cart,
        cart_item,
    )

    reset_customization()
    st.session_state.current_view = "cart"


def return_to_menu():
    reset_customization()
    st.session_state.current_view = "menu"


def clear_configured_item():
    st.session_state.configured_item = None


def submit_current_order():
    if not st.session_state.cart:
        return

    order = order_service.submit_order(
        st.session_state.cart,
        ORDER_TAX_RATE,
    )

    st.session_state.submitted_order = order
    st.session_state.cart = []
    st.session_state.current_view = "confirmation"


def start_new_order():
    st.session_state.submitted_order = None
    st.session_state.cart = []
    reset_customization()
    st.session_state.current_view = "menu"


def render_menu_item(item, key_prefix: str):
    if st.button(
        f"{item.name} • Starting at ${item.base_price:.2f}",
        key=f"{key_prefix}_{item.item_id}",
    ):
        st.session_state.selected_item_id = item.item_id
        st.rerun()

    st.write(item.description)


def render_cart():
    st.subheader("Your Order")

    cart = st.session_state.cart

    if not cart:
        st.info("Your order is empty. Add at least one item before placing an order.")

        st.button(
            "← Continue shopping",
            on_click=return_to_menu,
        )

        return

    for index, item in enumerate(cart):
        st.markdown(f"### {item.name}")
        st.write(f"Size: {item.size}")
        if item.milk is not None:
            st.write(f"Milk: {item.milk}")

        # Keep the price above the input, but fill it after updating quantity.
        price_line = st.empty()
        quantity = st.number_input(
            "Quantity",
            min_value=1,
            step=1,
            value=item.quantity,
            key=f"quantity_{item.line_id}",
        )

        if quantity != item.quantity:
            item.quantity = quantity

        item_total = cart_service.calculate_item_total(item)
        price_line.write(
            f"\\${item.unit_price:.2f} each • "
            f"**\\${item_total:.2f}**"
        )

        if st.button(
            "Remove",
            key=f"remove_{item.line_id}",
        ):
            cart_service.remove_item(cart, item)
            st.rerun()

        st.divider()

    subtotal = cart_service.calculate_subtotal(cart)
    tax = cart_service.calculate_tax(
        cart,
        ORDER_TAX_RATE,
    )
    total = cart_service.calculate_total(
        cart,
        ORDER_TAX_RATE,
    )

    st.write(f"Subtotal: **\\${subtotal:.2f}**")
    st.write(f"Tax: **\\${tax:.2f}**")
    st.write(f"### Total: \\${total:.2f}")

    st.button(
        "Place order",
        type="primary",
        on_click=submit_current_order,
    )

    st.button(
        "← Continue shopping",
        on_click=return_to_menu,
    )


def render_confirmation():
    order = st.session_state.submitted_order

    if order is None:
        st.info("No submitted order is available.")
        return

    st.subheader("Order received.")

    st.success(
        f"Thank you! Your order number is {order.order_number}."
    )

    for item in order.items:
        st.markdown(f"### {item.name}")
        st.write(f"Size: {item.size}")

        if item.milk is not None:
            st.write(f"Milk: {item.milk}")

        st.write(f"Qty: {item.quantity}")
        st.write(
            f"\\${item.unit_price:.2f} each"
        )

    st.divider()

    st.write(f"Subtotal: **\\${order.subtotal:.2f}**")
    st.write(f"Tax: **\\${order.tax:.2f}**")
    st.write(f"### Total: \\${order.total:.2f}")
    st.write(f"Status: **{order.status}**")

    st.button(
        "Start a new order",
        on_click=start_new_order,
    )


cart_service = CartService()
customization_service = CustomizationService()
order_service = OrderService(cart_service)
repository = MenuRepository()
menu_service = MenuService(repository)


st.title("Phoenix Coffee Co.")


if st.session_state.current_view == "cart":
    render_cart()
    st.stop()

if st.session_state.current_view == "confirmation":
    render_confirmation()
    st.stop()


menu_items = menu_service.get_available_menu()


if st.session_state.selected_item_id is not None:
    selected_item = next(
        (
            item
            for item in menu_items
            if item.item_id == st.session_state.selected_item_id
        ),
        None,
    )

    if selected_item is not None:
        st.subheader(f"Customize {selected_item.name}")
        st.write(selected_item.description)
        st.write(f"Starting at **${selected_item.base_price:.2f}**")

        size_options = list(
            customization_service.SIZE_ADJUSTMENTS.keys()
        )

        size = st.radio(
            "Choose a size*",
            size_options,
            index=None,
            key="selected_size",
            on_change=clear_configured_item,
        )

        if selected_item.allows_milk:
            st.selectbox(
                "Add or change dairy or nondairy",
                [
                    "Whole milk",
                    "2% milk",
                    "Nonfat milk",
                    "Breve",
                    "Oatmilk",
                    "Almond milk",
                ],
                index=None,
                key="selected_milk",
                placeholder="Select dairy/nondairy milk",
                on_change=clear_configured_item,
            )
        else:
            st.session_state.selected_milk = None

        if st.session_state.selected_size is not None:
            customized_price = customization_service.calculate_price(
                selected_item,
                st.session_state.selected_size,
            )

            st.write(f"**Current price: ${customized_price:.2f}**")

        if st.button("Continue"):
            if st.session_state.selected_size is None:
                st.warning("Please choose a size before continuing.")
            else:
                customized_price = customization_service.calculate_price(
                    selected_item,
                    st.session_state.selected_size,
                )

                st.session_state.configured_item = {
                    "item_id": selected_item.item_id,
                    "name": selected_item.name,
                    "size": st.session_state.selected_size,
                    "milk": st.session_state.selected_milk,
                    "price": customized_price
                }

                st.success(
                    f"{selected_item.name} customized successfully."
                )

        if st.session_state.configured_item is not None:
            configured = st.session_state.configured_item

            st.write("### Your selection")
            st.write(f"**{configured['name']}**")
            st.write(f"Size: {configured['size']}")

            if configured["milk"] is not None:
                st.write(f"Milk: {configured['milk']}")

            st.write(f"Price: **${configured['price']:.2f}**")

            st.button(
                "Add to order",
                type="primary",
                on_click=add_configured_item_to_cart,
            )

        st.button(
            "← Back to menu",
            on_click=reset_customization,
        )

        st.stop()


st.subheader("What can we get started for you?")
st.write("Browse the menu by category or choose from one of our popular drinks.")


st.markdown("### Browse by category")


coffee_tab, espresso_tab, tea_tab = st.tabs(
    ["Coffee", "Espresso", "Tea"]
)

with coffee_tab:
    for item in menu_items:
        if item.category == "Coffee":
            render_menu_item(item, "coffee")

with espresso_tab:
    for item in menu_items:
        if item.category == "Espresso":
            render_menu_item(item, "espresso")

with tea_tab:
    for item in menu_items:
        if item.category == "Tea":
            render_menu_item(item, "tea")


st.divider()


st.subheader("Popular Drinks")
st.write("Pick from a few customer favorites.")


for item in menu_items:
    render_menu_item(item, "popular")
    st.divider()
