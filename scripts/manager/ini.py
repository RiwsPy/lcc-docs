from functools import cached_property
import re
from typing import Any

from scripts.cleaner.ini import IniCleaner
from scripts.manager.utils import ManagerMixin


class IniManager(ManagerMixin):
    clean_class = IniCleaner

    header_regex = re.compile(r"\[Metadata\]\s+(?P<content>.*)", flags=re.DOTALL)
    comment_line_regex = re.compile(r"\s#.*")
    data_regex = re.compile(r"(?P<key>\w+)\s*=\s*(?P<value>.*)")

    def __init__(self, content: str):
        super().__init__(content)
        search = self.header_regex.search(content)

        if search:
            content_clean = search.group("content")
        else:
            content_clean = content

        self.content_clean = self.clean_comments(content_clean)

    @classmethod
    def clean_comments(cls, content: str) -> str:
        return cls.comment_line_regex.sub("", content)

    def get_authors(self) -> list[str]:
        author = self.json.get("Author", "")
        if author:
            return [author]
        return super().get_authors()

    def get_urls(self) -> list[str]:
        return [
            url
            for key in ("Homepage", "Forum", "Download")
            if (url := self.json.get(key, "").strip())
        ]

    def get_name(self) -> str:
        name = self.json.get("Name", "").strip()
        if name:
            return name
        return super().get_name()

    def get_categories(self) -> list[str]:
        category = self.json.get("Type", "").strip()
        if category:
            return [category]
        return super().get_categories()

    def get_tp2(self) -> str:
        if "Overwrite" in self.json.get("Type", ""):
            return "non-weidu"
        return super().get_tp2()

    def _get_tp2_position(self, position: str) -> list[str]:
        def clean_tp2(tp2: str) -> str:
            return tp2.replace(" ", "").replace("\r", "").lower()

        return [
            cleaned_tp2
            for tp2 in self.json.get(position, "").split(",")
            if (cleaned_tp2 := clean_tp2(tp2))
        ]

    def get_after(self) -> list[str]:
        return self._get_tp2_position("After")

    def get_before(self) -> list[str]:
        return self._get_tp2_position("Before")

    def get_readme(self) -> str:
        return self.json.get("Readme", "")

    def get_labeltype(self) -> str:
        return self.json.get("LabelType", "")

    @cached_property
    def json(self) -> dict[str, Any]:
        return dict(items for items in self.data_regex.findall(self.content_clean))
