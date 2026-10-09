from functools import cached_property
from typing import Any

from scripts.cleaner.utils import CleanModMixin


class ManagerMixin:
    clean_class: type[CleanModMixin] | None = None

    def __init__(self, content: str):
        self.content = content

    def get_name(self) -> str:
        return ""

    def get_games(self) -> list[str]:
        return list()

    def get_languages(self) -> list[str]:
        return list()

    def get_authors(self) -> list[str]:
        return list()

    def get_categories(self) -> list[str]:
        return list()

    def get_urls(self) -> list[str]:
        return list()

    def get_tp2(self) -> str:
        return ""

    @cached_property
    def clean_json(self) -> dict[str, Any]:
        lcc_json = {
            "name": self.get_name(),
            "games": self.get_games(),
            "languages": self.get_languages(),
            "authors": self.get_authors(),
            "categories": self.get_categories(),
            "urls": self.get_urls(),
            "tp2": self.get_tp2(),
        }
        if self.clean_class is None:
            return lcc_json

        cleaner = self.clean_class(lcc_json)
        cleaner.clean_all()
        return cleaner.cleaned_data
