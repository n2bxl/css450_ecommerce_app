# app.py

import streamlit as st

from repositories.menu_repository import MenuRepository
from services.customization_service import CustomizationService
from services.menu_service import MenuService


if "selected_item_id" not in st.session_state:
    st.session_state.selected_item_id = None

if "selected_size" not in st.session_state:
    st.session_state.selected_size = None

if "selected_milk" not in st.session_state:
    st.session_state.selected_milk = None

if "configured_item" not in st.session_state:
    st.session_state.configured_item = None

def reset_customization():
    st.session_state.selected_item_id = None
    st.session_state.selected_size = None
    st.session_state.selected_milk = None
    st.session_state.configured_item = None

def clear_configured_item():
    st.session_state.configured_item = None

customization_service = CustomizationService()

st.set_page_config(
    page_title="Phoenix Coffee Co.",
    page_icon="☕️",
)

repository = MenuRepository()
menu_service = MenuService(repository)

st.title("Phoenix Coffee Co.")

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

        size = st.radio(
            "Choose a size*",
            ["Small", "Medium", "Large"],
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
            "← Back to menu",
            on_click=reset_customization,
        )

        st.stop()

st.subheader("What can we get started for you?")
st.write("Browse the menu by category or choose from one of our popular drinks.")

def render_menu_item(item, key_prefix: str):
    if st.button(
        f"{item.name} • Starting at ${item.base_price:.2f}",
        key=f"{key_prefix}_{item.item_id}",
    ):
        st.session_state.selected_item_id = item.item_id
        st.rerun()

    st.write(item.description)

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