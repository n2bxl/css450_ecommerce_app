# services/menu_service.py

from models.menu_item import MenuItem
from repositories.menu_repository import MenuRepository


class MenuService:
    def __init__(self, repository: MenuRepository):
        self.repository = repository

    def get_available_menu(self) -> list[MenuItem]:
        return [
            item
            for item in self.repository.get_all()
            if item.available
        ]