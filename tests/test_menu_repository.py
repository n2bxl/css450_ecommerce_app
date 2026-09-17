# tests/test_menu_repository.py

from decimal import Decimal

from repositories.menu_repository import MenuRepository


def test_get_all_converts_csv_rows_to_menu_items(tmp_path):
    menu_file = tmp_path / "menu_items.csv"

    menu_file.write_text(
        "item_id,name,category,description,base_price,available,allows_milk\n"
        "1,Caffe Latte,Espresso,Espresso with steamed milk,4.25,true,true\n"
        "2,Hot Chocolate,Other,Steamed milk with chocolate sauce,3.95,false,true\n",
        encoding="utf-8",
    )

    repository = MenuRepository(menu_file)

    menu = repository.get_all()

    assert len(menu) == 2

    assert menu[0].item_id == 1
    assert menu[0].name == "Caffe Latte"
    assert menu[0].category == "Espresso"
    assert menu[0].description == "Espresso with steamed milk"
    assert menu[0].base_price == Decimal("4.25")
    assert menu[0].available is True
    assert menu[0].allows_milk is True

    assert menu[1].item_id == 2
    assert menu[1].name == "Hot Chocolate"
    assert menu[1].base_price == Decimal("3.95")
    assert menu[1].available is False
    assert menu[1].allows_milk is True