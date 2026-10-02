from decimal import Decimal
from pathlib import Path

from streamlit.testing.v1 import AppTest

from models.cart_item import CartItem


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def make_cart_app():
    latte = CartItem(
        item_id=1,
        name="Caffe Latte",
        size="Medium",
        milk="Oatmilk",
        unit_price=Decimal("4.75"),
        quantity=1,
    )
    americano = CartItem(
        item_id=2,
        name="Caffe Americano",
        size="Small",
        milk=None,
        unit_price=Decimal("3.25"),
        quantity=1,
    )

    app = AppTest.from_file(APP_PATH)
    app.session_state["cart"] = [latte, americano]
    app.session_state["current_view"] = "cart"
    app.run()
    assert not app.exception
    return app, latte, americano


def test_quantity_changes_keep_displayed_line_amounts_and_totals_consistent():
    app, latte, americano = make_cart_app()

    # Independent expected amounts for increases and decreases on both lines.
    expected_states = [
        (2, 1, "9.50", "3.25", "12.75", "1.28", "14.03"),
        (5, 2, "23.75", "6.50", "30.25", "3.03", "33.28"),
        (1, 3, "4.75", "9.75", "14.50", "1.45", "15.95"),
        (4, 1, "19.00", "3.25", "22.25", "2.23", "24.48"),
    ]

    for (
        latte_qty,
        americano_qty,
        latte_amount,
        americano_amount,
        subtotal,
        tax,
        total,
    ) in expected_states:
        app.number_input(key=f"quantity_{latte.line_id}").set_value(latte_qty)
        app.number_input(key=f"quantity_{americano.line_id}").set_value(americano_qty)
        app.run()

        assert not app.exception
        displayed = [element.value for element in app.markdown]
        assert f"\\$4.75 each • **\\${latte_amount}**" in displayed, displayed
        assert f"\\$3.25 each • **\\${americano_amount}**" in displayed, displayed
        assert f"Subtotal: **\\${subtotal}**" in displayed
        assert f"Tax: **\\${tax}**" in displayed
        assert f"### Total: \\${total}" in displayed

    place_order = next(button for button in app.button if button.label == "Place order")
    place_order.click().run()
    assert not app.exception

    order = app.session_state["submitted_order"]
    assert [(item.quantity, item.size, item.milk) for item in order.items] == [
        (4, "Medium", "Oatmilk"),
        (1, "Small", None),
    ]
    assert order.subtotal == Decimal("22.25")
    assert order.tax == Decimal("2.23")
    assert order.total == Decimal("24.48")
    assert "### Total: \\$24.48" in [element.value for element in app.markdown]


def test_removing_all_items_shows_required_instruction_and_blocks_submission():
    app, latte, americano = make_cart_app()

    app.button(key=f"remove_{americano.line_id}").click().run()
    assert not app.exception
    displayed = [element.value for element in app.markdown]
    assert "Subtotal: **\\$4.75**" in displayed
    assert "Tax: **\\$0.48**" in displayed
    assert "### Total: \\$5.23" in displayed

    app.button(key=f"remove_{latte.line_id}").click().run()
    assert not app.exception
    assert app.session_state["cart"] == []
    assert app.session_state["submitted_order"] is None
    assert app.info[0].value == (
        "Your order is empty. Add at least one item before placing an order."
    )
    assert all(button.label != "Place order" for button in app.button)
