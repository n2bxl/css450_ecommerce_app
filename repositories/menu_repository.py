# repositories/menu_repository.py

import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

from models.menu_item import MenuItem


class MenuRepository:
    REQUIRED_COLUMNS = {
        "item_id",
        "name",
        "category",
        "description",
        "base_price",
        "available",
        "allows_milk",
    }

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
        seen_item_ids = set()

        with self.file_path.open(
            mode="r",
            encoding="utf-8",
            newline=""
        ) as csv_file:
            reader = csv.DictReader(csv_file)

            fieldnames = set(reader.fieldnames or [])
            missing_columns = self.REQUIRED_COLUMNS - fieldnames

            if missing_columns:
                raise ValueError(
                    "Missing required column(s): "
                    + ", ".join(sorted(missing_columns))
                )

            for row in reader:
                item_id = self._to_item_id(row["item_id"])

                if item_id in seen_item_ids:
                    raise ValueError(
                        f"Duplicate item ID: {item_id}"
                    )

                seen_item_ids.add(item_id)

                items.append(
                    MenuItem(
                        item_id=item_id,
                        name=self._require_text(row["name"], "name"),
                        category=self._require_text(row["category"], "category"),
                        description=self._require_text(row["description"], "description"),
                        base_price=self._to_price(row["base_price"]),
                        available=self._to_bool(row["available"]),
                        allows_milk=self._to_bool(row["allows_milk"]),
                    )
                )

        return items

    @staticmethod
    def _to_bool(value: str) -> bool:
        normalized_value = value.strip().lower()

        if normalized_value == "true":
            return True

        if normalized_value == "false":
            return False

        raise ValueError(
            f"Invalid boolena value: {value!r}. "
            "Expected 'true' or 'false'."
        )

    @staticmethod
    def _to_price(value: str) -> Decimal:
        try:
            price = Decimal(value.strip())
        except InvalidOperation as exc:
            raise ValueError(
                f"Invalid price value: {value!r}. "
                "Expected a numeric value."
            ) from exc

        if price < 0:
            raise ValueError(
                f"Invalid price value: {value!r}. "
                "Price cannot be negative."
            )

        return price

    @staticmethod
    def _require_text(value:str, field_name: str) -> str:
        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError(
                f"Required field '{field_name}' cannot be blank."
            )

        return normalized_value

    @staticmethod
    def _to_item_id(value: str) -> int:
        try:
            item_id = int(value.strip())
        except (AttributeError, TypeError, ValueError) as exc:
            raise ValueError(
                f"Invalid item ID: {value!r}. "
                "Expected a positive integer."
            ) from exc

        if item_id <= 0:
            raise ValueError(
                f"Invalid item ID: {value!r}. "
                "Item ID must be greater than zero."
            )

        return item_id