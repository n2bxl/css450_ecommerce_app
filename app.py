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
st.subheader("Menu")

menu_items = menu_service.get_available_menu()
st.write(f"Loaded {len(menu_items)} menu items")

for item in menu_items:
    st.markdown(f"### {item.name}")
    st.write(item.description)
    st.write(f"**${item.base_price:.2f}**")
    st.divider()