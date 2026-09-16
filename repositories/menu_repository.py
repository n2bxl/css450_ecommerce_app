# repositories/menu_repository.py

import csv
from decimal import Decimal
from pathlib import Path

from model.menu_item import MenuItem

class MenuRepository:
    def __init__(self, file_path: Path | None = None):
        if file_path is None:
            file_path = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "menu_items.csv"
            )

        self.file_path = file_path

    def get_all(self) -> list[MenuItem]:
        items = []

        with self.file_path.open(
            mode="r",
            encoding="utf-8",
            newline=""
        ) as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                items.append(
                    MenuItem(
                        item_id=int(row["item_id"]),
                        name=row["name"],
                        category=row["category"],
                        description=row["description"],
                        base_price=Decimal(row["base_price"]),
                        available=self._to_bool(row["available"]),
                        allows_milk=self._to_bool(row["allows-milk"]),
                    )
                )

        return items


@staticmethod
def _to_bool(value: str) -> bool:
    return value.strip().lower() == "true"