# tests/test_menu_repository.py

from decimal import Decimal

import pytest

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


def test_get_all_rejects_invalid_boolean_value(tmp_path):
    menu_file = tmp_path / "menu_items.csv"

    menu_file.write_text(
        "item_id,name,category,description,base_price,available,allows_milk\n"
        "1,Caffe Latte,Espresso,Espresso with steamed milk,4.25,maybe,true\n",
        encoding="utf-8",
    )

    repository = MenuRepository(menu_file)

    with pytest.raises(ValueError):
        repository.get_all()


def test_get_all_rejects_invalid_base_price(tmp_path):
    menu_file = tmp_path / "menu_items.csv"

    menu_file.write_text(
        "item_id,name,category,description,base_price,available,allows_milk\n"
        "1,Caffe Latte,Espresso,Espresso with steamed milk,not-a-price,true,true\n",
        encoding="utf-8",
    )

    repository = MenuRepository(menu_file)

    with pytest.raises(ValueError):
        repository.get_all()


def test_get_all_rejects_negative_base_price(tmp_path):
    menu_file = tmp_path / "menu_items.csv"

    menu_file.write_text(
        "item_id,name,category,description,base_price,available,allows_milk\n"
        "1,Caffe Latte,Espresso,Espresso with steamed milk,-4.25,true,true\n",
        encoding="utf-8",
    )

    repository = MenuRepository(menu_file)

    with pytest.raises(ValueError):
        repository.get_all()


def test_get_all_rejects_blank_required_text_value(tmp_path):
    menu_file = tmp_path / "menu_items.csv"

    menu_file.write_text(
        "item_id,name,category,description,base_price,available,allows_milk\n"
        "1,,Espresso,Espresso with steamed milk,4.25,true,true\n",
        encoding="utf-8",
    )

    repository = MenuRepository(menu_file)

    with pytest.raises(ValueError):
        repository.get_all()


def test_get_all_rejects_non_positive_item_id(tmp_path):
    menu_file = tmp_path / "menu_items.csv"

    menu_file.write_text(
        "item_id,name,category,description,base_price,available,allows_milk\n"
        "-1,Caffe Latte,Espresso,Espresso with steamed milk,4.25,true,true\n",
        encoding="utf-8",
    )

    repository = MenuRepository(menu_file)

    with pytest.raises(ValueError):
        repository.get_all()


def test_get_all_rejects_duplicate_item_ids(tmp_path):
    menu_file = tmp_path / "menu_items.csv"

    menu_file.write_text(
        "item_id,name,category,description,base_price,available,allows_milk\n"
        "1,Caffe Latte,Espresso,Espresso with steamed milk,4.25,true,true\n"
        "1,Caffe Americano,Espresso,Espresso with hot water,3.25,true,false\n",
        encoding="utf-8",
    )

    repository = MenuRepository(menu_file)

    with pytest.raises(ValueError):
        repository.get_all()


def test_get_all_rejects_missing_required_column(tmp_path):
    menu_file = tmp_path / "menu_items.csv"

    menu_file.write_text(
        "item_id,name,category,description,base_price,available\n"
        "1,Caffe Latte,Espresso,Espresso with steamed milk,4.25,true\n",
        encoding="utf-8",
    )

    repository = MenuRepository(menu_file)

    with pytest.raises(ValueError):
        repository.get_all()