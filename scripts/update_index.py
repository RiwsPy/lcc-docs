from json import load as json_load
from os import sep as os_sep
from pathlib import Path

# import yaml
from jinja2 import Environment, PackageLoader, select_autoescape

from models import Mod
from settings import CategoryEnum, GameEnum, attrs_icon_data, resize_image_from_width


def main():
    env = Environment(
        loader=PackageLoader("docs", "templates"),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,  # Supprime les retours à la ligne après un bloc Jinja
        lstrip_blocks=True,  # Supprime les espaces avant un bloc Jinja
    )

    root = Path.cwd()
    with open(root / "db" / "mods.json", "r", encoding="utf-8") as f:
        mods = json_load(f)
    # with open("mods.yaml", "r") as f:
    #     mods = yaml.safe_load(f)

    mods.sort(key=lambda x: x["name"].lower())

    resize_image_from_width(24)

    categories_mod = {cat: list() for cat in CategoryEnum}
    for mod_json in mods:
        mod = Mod(**mod_json)

        for category in mod.categories:
            categories_mod[category].append(mod)

    page_html = env.get_template("base.html").render(
        games=GameEnum,
        categories=categories_mod,
        static=f"static{os_sep}",
        attrs_icon_data=attrs_icon_data,
        mod_length=len(mods),
    )

    with open(root / "docs" / "index.html", "w", encoding="utf-8") as f:
        f.write(page_html)
