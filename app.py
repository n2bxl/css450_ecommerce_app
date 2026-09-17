# app.py

import streamlit as st

from repositories.menu_repository import MenuRepository
from services.menu_service import MenuService


st.set_page_config(
    page_title="Phoenix Coffee Co.",
    page_icon="☕️",
)

repository = MenuRepository()
menu_service = MenuService(repository)

st.title("Phoenix Coffee Co.")

st.subheader("What can we get started for you?")
st.write("Browse the menu by category or choose from one of our popular drinks.")

menu_items = menu_service.get_available_menu()

st.markdown("### Browse by category")

coffee_tab, espresso_tab, tea_tab = st.tabs(
    ["Coffee", "Espresso", "Tea"]
)

with coffee_tab:
    for item in menu_items:
        if item.category == "Coffee":
            st.markdown(f"**{item.name}**")
            st.write(item.description)
            st.write(f"Starting at **${item.base_price:.2f}**")

with espresso_tab:
    for item in menu_items:
        if item.category == "Espresso":
            st.markdown(f"**{item.name}**")
            st.write(item.description)
            st.write(f"Starting at **${item.base_price:.2f}**")

with tea_tab:
    for item in menu_items:
        if item.category == "Tea":
            st.markdown(f"**{item.name}**")
            st.write(item.description)
            st.write(f"Starting at **${item.base_price:.2f}**")

st.divider()

st.subheader("Popular Drinks")
st.write("Pick from a few customer favorites.")

for item in menu_items:
    st.markdown(f"#### {item.name}")
    st.write(item.description)
    st.write(f"Starting at **${item.base_price:.2f}**")
    st.divider()