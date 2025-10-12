from dataclasses import fields
import json
from json import JSONDecodeError
import logging
import os

from i18n import LANGUAGE_DEFAULT, current_language
from models.mod import Mod
from settings import DB_PATH

logger = logging.getLogger(__name__)


class ModManager:
    mod_filename: str = "mods.json"
    mod_filename_lang: str = "mods_{lang}.json"

    @classmethod
    def get_language_filename(cls, language: str | None = None) -> str:
        if language is None:
            language = current_language()
        if language:
            return cls.mod_filename_lang.format(lang=language)
        return cls.mod_filename

    @classmethod
    def load(cls, language: str | None = None) -> list[dict]:
        filename = cls.get_language_filename(language=language)

        try:
            with open(DB_PATH / filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"File not found {DB_PATH / filename}")
        except JSONDecodeError:
            logging.error(f"Error decoding {DB_PATH / filename}")
        return list()

    @classmethod
    def export(cls, mods: dict | list, language: str | None = None) -> None:
        assert mods, "Mods not loaded"

        filename = cls.get_language_filename(language=language)
        with open(DB_PATH / filename, "w", encoding="utf-8") as f:
            json.dump(mods, f, indent=4, ensure_ascii=False)

    @classmethod
    def get_mod_list(cls, language: str | None = None) -> list[Mod]:
        default_list = cls.load(language="")

        if not language:
            source_list = default_list
        elif language in (LANGUAGE_DEFAULT, "en"):
            source_list = cls.get_combine_language(
                default_list, language, merge_urls_extra=True, merge_notes_extra=True
            )
        else:
            source_list = cls.get_combine_language(
                default_list, "en", exclude_fields=["team", "translation_state"]
            )
            source_list = cls.get_combine_language(
                source_list, language, merge_urls_extra=True, merge_notes_extra=True
            )

        return [Mod(**mod) for mod in source_list]

    @classmethod
    def get_combine_language(
        cls,
        source_list: list[dict],
        language_target: str,
        *,
        exclude_fields: None | list[str] = None,
        merge_urls_extra: bool = False,
        merge_notes_extra: bool = False,
    ) -> list[dict]:
        target_list = cls.load(language_target)
        source_list_pks = {mod["id"]: mod for mod in source_list}
        target_list_pks = {mod["id"]: mod for mod in target_list}
        for pk, data in target_list_pks.items():
            source_list_pks[pk] |= {
                k: v
                for k, v in data.items()
                if v and (exclude_fields is None or k not in exclude_fields)
            }
            if merge_urls_extra and "urls_extra" in source_list_pks[pk]:
                source_list_pks[pk]["urls"] += source_list_pks[pk]["urls_extra"]
            if merge_notes_extra and "notes_extra" in source_list_pks[pk]:
                source_list_pks[pk]["notes"] += source_list_pks[pk]["notes_extra"]
        return list(source_list_pks.values())


class CleanModMixin:
    def __init__(self, data: dict):
        self.data = data
        self.cleaned_data = dict()

    def clean_all(self) -> None:
        for field in fields(Mod):
            attr = field.name
            try:
                cleaned_value = getattr(self, f"clean_{attr}")()
            except AttributeError:
                pass
            else:
                if cleaned_value is not None:
                    self.cleaned_data[attr] = cleaned_value


def simplify_url(url: str) -> str:
    if url.startswith(
        ("https://github.com/", "https://forums.beamdog.com/discussion/")
    ) and not url.startswith("https://forums.beamdog.com/discussion/comment/"):
        url = "/".join(url.split("/")[:5])
    return url.removesuffix("/")


with open(DB_PATH / "author_pseudos.json", "r", encoding="utf-8") as f:
    author_pseudos = json.load(f)

AUTHOR_PSEUDOS: dict[str, tuple[str]] = {
    pseudo: k for k, pseudos in author_pseudos.items() for pseudo in pseudos
}


def get_languages() -> set[str]:
    # auto-discover languages
    with os.scandir(DB_PATH) as it:
        return {
            f.name.removeprefix("mods_").removesuffix(".json")
            for f in it
            if f.is_file() and f.name.endswith(".json") and f.name.startswith("mods_")
        }
