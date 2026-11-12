from enum import StrEnum
from functools import cached_property
import re
import unicodedata
from urllib.parse import parse_qs, unquote, urlparse

from scripts.cleaner import ReadmeCleaner
from scripts.manager.utils import ManagerMixin


class ShieldType(StrEnum):
    LANGUAGE = "languages"
    GAME = "games"

    @property
    def labels(self) -> set[str]:
        match self.value:
            case self.__class__.LANGUAGE.value:
                return {"language", "langues"}
            case self.__class__.GAME.value:
                return {"supported games", "jeux supportes"}
        return set()

    @property
    def badge_prefix(self) -> str:
        match self.value:
            case self.__class__.LANGUAGE.value:
                return "language"
            case self.__class__.GAME.value:
                return "games"
        return ""


class ReadmeManager(ManagerMixin):
    clean_class = ReadmeCleaner

    mod_name_md_regex = re.compile(r"^\#\s+(.+)")
    mod_name_html_regex = re.compile(r"<h1>(.+?)</h1>", flags=re.DOTALL)
    shields_pattern = re.compile(r"!\[.*?\]\((https:\/\/img\.shields\.io\/.*?)\)")

    author_md_regex = re.compile(
        r"^(?:\*{2})?(?:Auth?ors?|Original Auth?ors?)(?:\*{2})?\s*:\s*(.*)"
    )
    author_html_regex = re.compile(
        r"<strong>(?:Auth?ors?|Original Auth?ors?)\s*:\s*(.*)</strong>"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_html = self.content.startswith("<!DOCTYPE")

    def get_name(self) -> str:
        # NOTE: on peut avoir des balises html dans un fichier md, donc on check toujours la regex html
        regexs = [self.mod_name_html_regex]
        if not self.is_html:
            regexs.insert(0, self.mod_name_md_regex)

        for regex in regexs:
            search = regex.search(self.content)
            if search:
                return search.group(1)
        return super().get_name()

    def get_authors(self) -> list[str]:
        regexs = [self.author_html_regex]
        if not self.is_html:
            regexs.insert(0, self.author_md_regex)

        for regex in regexs:
            search = regex.search(self.content)
            if search:
                return [search.group(1).strip("*")]
        return super().get_authors()

    def read_shields(self, shield_type: ShieldType) -> list[str]:
        for shield in self.shields:
            shield_content = parse_qs(urlparse(shield).query)

            if "label" in shield_content and "message" in shield_content:
                label = shield_content["label"][0]
                if label.lower() in shield_type.labels:
                    message = shield_content["message"][0]
                    return self.clean_shield_message(message)

            elif shield.startswith("https://img.shields.io/badge/") and shield.count("-") >= 2:
                prefix, message, *_ = shield.split("-", 2)
                if prefix.endswith(shield_type.badge_prefix):
                    return self.clean_shield_message(message)

        return list()

    def get_languages(self) -> list[str]:
        return self.read_shields(ShieldType.LANGUAGE)

    def get_games(self) -> list[str]:
        return self.read_shields(ShieldType.GAME)

    @cached_property
    def shields(self) -> list[str]:
        shields = self.shields_pattern.findall(self.content)
        return [
            unicodedata.normalize("NFKD", unquote(shield))
            .encode("ascii", "ignore")
            .decode("ascii")
            for shield in shields
        ]

    @staticmethod
    def clean_shield_message(message: str) -> list[str]:
        message = message.replace("  ", "|").replace(":", "")
        return message.split("|")
