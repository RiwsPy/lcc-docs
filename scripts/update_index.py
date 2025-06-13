import os
from os import sep as os_sep
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

from scripts.utils import ModManager
from settings import (
    LANGUAGE_CONFIG,
    CategoryEnum,
    GameEnum,
    attrs_icon_data,
    language_flags,
    resize_image_from_width,
)

# TODO: Script pour générer le fichier en par défaut (avec prise en compte de la langue et retrait de team)
# Réorienter automatiquement vers la page de sa langue


def main():
    env = Environment(
        loader=PackageLoader("docs", "templates"),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,  # Supprime les retours à la ligne après un bloc Jinja
        lstrip_blocks=True,  # Supprime les espaces avant un bloc Jinja
    )

    root = Path.cwd()
    resize_image_from_width(24)

    # auto-discover languages
    with os.scandir(ModManager.db_path()) as it:
        languages = {
            f.name.removeprefix("mods_").removesuffix(".json")
            for f in it
            if f.is_file() and f.name.endswith(".json") and f.name.startswith("mods_")
        }

    for language in languages & language_flags.keys():
        with LANGUAGE_CONFIG.override_language(language):
            mods = ModManager.get_mod_list()

            mods.sort(key=lambda x: x.name.lower())

            categories_mod = {cat: list() for cat in CategoryEnum}
            for mod in mods:
                for category in mod.categories:
                    categories_mod[category].append(mod)
            page_html = env.get_template("base.html").render(
                games=GameEnum,
                categories=categories_mod,
                static=f"..{os_sep}static{os_sep}",
                attrs_icon_data=attrs_icon_data,
                mod_length=len(mods),
            )

            dir_path = root / "docs" / language
            dir_path.mkdir(parents=True, exist_ok=True)
            with open(dir_path / "index.html", "w", encoding="utf-8") as f:
                f.write(page_html)
