import logging
import os
from os import sep as os_sep
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

from i18n import LANGUAGE_CONFIG, LANGUAGE_DEFAULT
from scripts.utils import ModManager
from settings import (
    DB_PATH,
    CategoryEnum,
    GameEnum,
    attrs_icon_data,
    language_flags,
    resize_image_from_width,
)

# TODO:Réorienter automatiquement vers la page de sa langue

logger = logging.getLogger(__name__)


def main(**kwargs):
    def build_html_page(static: str) -> str:
        return env.get_template("base.html").render(
            games=GameEnum,
            categories=categories_mod,
            static=static,
            attrs_icon_data=attrs_icon_data,
            mod_length=len(mods),
            language=language,
        )

    env = Environment(
        loader=PackageLoader("docs", "templates"),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,  # Supprime les retours à la ligne après un bloc Jinja
        lstrip_blocks=True,  # Supprime les espaces avant un bloc Jinja
    )

    resize_image_from_width(24)

    # auto-discover languages
    with os.scandir(DB_PATH) as it:
        languages = {
            f.name.removeprefix("mods_").removesuffix(".json")
            for f in it
            if f.is_file() and f.name.endswith(".json") and f.name.startswith("mods_")
        }

    for language in languages & language_flags.keys():
        with LANGUAGE_CONFIG.switch_language(language):
            mods = ModManager.get_mod_list()

            mods.sort(key=lambda x: x.name.lower())

            categories_mod = {cat: list() for cat in CategoryEnum}
            for mod in mods:
                for category in mod.categories:
                    categories_mod[category].append(mod)

            page_html = build_html_page(static=f"..{os_sep}static{os_sep}")
            create_page_language(page_html, language)

            # on crée aussi la page par defaut (home), qui est celle du language par défaut
            if language == LANGUAGE_DEFAULT:
                page_html = build_html_page(static=f"static{os_sep}")
                create_page_language(page_html, "")


def create_page_language(page_html: str, language: str) -> None:
    dir_path = Path.cwd() / "docs"
    if language:
        dir_path /= language
    dir_path.mkdir(parents=True, exist_ok=True)

    logger.info("Generating index page for %s", language)
    with open(dir_path / "index.html", "w", encoding="utf-8") as f:
        f.write(page_html)
