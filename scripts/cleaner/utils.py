from dataclasses import fields
import json
import re

from models import Mod
from settings import GameEnum


class CleanModMixin:
    def __init__(self, data: dict):
        self.data = data
        self.cleaned_data: dict = dict()

    def clean_all(self) -> None:
        for field in fields(Mod):
            attr = field.name

            if hasattr(self, f"clean_{attr}"):
                cleaned_value = getattr(self, f"clean_{attr}")()
            else:
                cleaned_value = self.data.get(attr)

            if cleaned_value is not None:
                self.cleaned_data[attr] = cleaned_value


# https://fr.wikipedia.org/wiki/ISO_3166-1

lang_pseudos = {
    "br": ("pt_br", "br", "pt"),
    "bq": ("nl_bq", "bq", "nederlands", "nl"),
    "cn": ("zh_cn", "ch", "cn", "si", "sc", "简体", "繁體", "¼ò", "tc", "zh"),
    "cz": ("cs_cz", "ce", "če", "cz", "cs"),
    "de": ("de_de", "ge", "al", "de"),
    "en": ("en_us", "en", "us", "am", "an", "en"),
    "es": ("es_es", "es", "ca", "sp"),
    "fr": ("fr_fr", "fr"),
    "hr": ("hr_ba", "croatian", "ba", "hr"),
    "hu": ("hu_hu", "ma", "hu"),
    "it": ("it_it", "it"),
    "jp": ("ja_jp", "jp", "日本", "ja"),
    "kr": ("ko_kp", "kp", "한국", "ko", "茄惫", "kr"),
    "pl": ("pl_pl", "po", "polish", "pl"),
    "pt": ("pt_pt", "portuguese", "pt"),
    "ru": ("ru_ru", "d¢", "ru"),
    "se": ("sv_se", "sw", "se", "sv"),
    "tr": ("tr_tr", "tu"),
}

lang_mapping = {
    pseudo.lower(): lang.lower() for lang, pseudos in lang_pseudos.items() for pseudo in pseudos
}


with open("db/author_pseudos.json", "r", encoding="utf-8") as f:
    author_pseudos = json.load(f)

author_map = {pseudo: k for k, pseudos in author_pseudos.items() for pseudo in pseudos}


class ModCleaner(CleanModMixin):
    # clean name : vX.Y
    # name authors : case insensitive

    # author (email)
    bracket_author_regex = re.compile(r"\s+\(.*?\)")
    tp2_clean_regex = re.compile(r"(setup-)?(?P<name>.+)\.tp2", flags=re.IGNORECASE)
    bracket_regex = re.compile(r"\[.+?\]|\(.+?\)")

    def clean_all(self) -> None:
        for field in fields(Mod):
            attr = field.name
            # Note: needed for data_from_url
            if attr not in self.data:
                continue

            if hasattr(self, f"clean_{attr}"):
                cleaned_value = getattr(self, f"clean_{attr}")()
            else:
                cleaned_value = self.data.get(attr)

            if cleaned_value is not None:
                self.cleaned_data[attr] = cleaned_value

    def clean_name(self) -> str:
        next_name = self.data.get("name", "")
        # TODO: Aller chercher la strref si besoin
        if next_name.startswith("@"):
            next_name = ""
        else:
            next_name = next_name.removesuffix("<br/>").replace("&amp;", "&").replace("’", "'")
            next_name = self.bracket_regex.sub("", next_name)

        return next_name.strip().strip('"')

    def clean_games(self) -> list[str]:
        if not self.data.get("games"):
            return list()

        def clean_game(game: str) -> str:
            if not game:
                return ""

            game = game.strip()
            game = (
                game.lower()
                .replace("tutu_totsc", "tutu")
                .replace("bg1", "bg")
                .replace("totsc", "bg")
                .replace("iwd1", "iwd")
                .replace("tob", "bg2")
                .strip()
            )

            try:
                return getattr(GameEnum, game.upper()).value
            except AttributeError:
                # print(f"{game} not found in `GameEnum`")
                return ""

        # TODO: sorted
        return list(
            set(
                cleaned_game
                for game in set(self.data["games"])
                if (cleaned_game := clean_game(game))
            )
        )

    def clean_authors(self) -> list[str]:
        def clean_author(author: str) -> str:
            cleaned_author = self.bracket_author_regex.sub("", author)
            if "@" in cleaned_author:
                cleaned_author = cleaned_author.partition("@")[0]

            cleaned_author = (
                cleaned_author.replace("\r", "").replace("\xa0", " ").removesuffix(",").strip()
            )

            return author_map.get(cleaned_author, cleaned_author)

        authors = list()
        for author in self.data.get("authors", list()):
            author = (
                author.replace(" and ", "&")
                .replace(", ", "&")
                .replace(" et ", "&")
                .replace('"', "")
            )
            if "&" in author:
                authors += author.split("&")
            else:
                authors.append(author)

        return [
            author_cleaned
            for author in authors
            if (author_cleaned := clean_author(author))
            # Utilisé pour indiquer une adresse email ou une url, non pertinent
            # and not author_cleaned.startswith("at ")
            and not author_cleaned.startswith("http")
            and not author_cleaned.startswith("at ")
            and author_cleaned != "others"
        ]

    def clean_languages(self) -> list[str]:
        if not self.data.get("languages"):
            return list()

        def clean_lang(lang: str) -> str:
            lang = self.bracket_author_regex.sub("", lang)
            lang = lang.lower().strip().strip("/")
            lang = lang.rsplit("/", 1)[-1].strip()
            cleaned_lang = lang_mapping.get(lang) or lang_mapping.get(lang[:2]) or ""
            if lang not in ("", "tra") and not cleaned_lang:
                print(f"{self.clean_name()}: Lang {lang} not found")
                # cleaned_lang = lang[:2]
            return cleaned_lang

        return sorted(
            set(
                cleaned_lang
                for lang in set(self.data["languages"])
                if (cleaned_lang := clean_lang(lang))
            )
        )

    def clean_last_update(self) -> str:
        try:
            last_update = self.data["last_update"].strftime(Mod.last_update_date_format)
        except Exception:
            last_update = ""

        return last_update

    def clean_tp2(self) -> str:
        tp2_name = self.data.get("tp2", "")
        re_match = self.tp2_clean_regex.fullmatch(tp2_name)
        if re_match:
            tp2_name = re_match.group("name")

        return tp2_name

    def clean_categories(self) -> list[str]:
        return list(set(self.data.get("categories", list())))
