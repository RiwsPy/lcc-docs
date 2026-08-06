import logging
from os import sep as os_sep
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape
import minify_html

from i18n import LANGUAGE_CONFIG, TEMPLATE_TRANSLATIONS, _g
from models.mod import ModStatus
from scripts.utils import ModManager, get_languages
from settings import (
    CategoryEnum,
    GameEnum,
    attrs_icon_data,
    language_flags,
    resize_image_from_width,
)

logger = logging.getLogger(__name__)

home_page = "https://riwspy.github.io/lcc-docs/"


def main(**kwargs):
    def build_html_page(**kwargs) -> str:
        html_page = env.get_template("base.html").render(
            games=GameEnum,
            attrs_icon_data=attrs_icon_data,
            language_flags=used_language_flags,
            trans=TEMPLATE_TRANSLATIONS,
            home_page=home_page,
            **kwargs,
        )
        return minify_html.minify(html_page, minify_js=True, minify_css=True)

    env = Environment(
        loader=PackageLoader("docs", "templates"),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,  # Supprime les retours à la ligne après un bloc Jinja
        lstrip_blocks=True,  # Supprime les espaces avant un bloc Jinja
        extensions=["jinja2.ext.i18n"],
    )
    env.install_gettext_callables(
        gettext=_g,
        ngettext=_g,
        newstyle=True,
    )

    resize_image_from_width(24)

    languages = get_languages() & language_flags.keys()
    used_language_flags = {k: v for k, v in language_flags.items() if k in languages}
    authors = set()
    team = set()

    for language in languages:
        with LANGUAGE_CONFIG.switch_language(language):
            mods = ModManager.get_mod_list(language)

            mods.sort(key=lambda x: x.name.lower())

            mod_id_to_name = {mod.id: mod.name for mod in mods}

            categories_mod = {cat: list() for cat in CategoryEnum}
            for mod in mods:
                if ModStatus.HIDDEN not in mod.status:
                    for category in mod.categories:
                        categories_mod[category].append(mod)
                    authors |= set(mod.authors)
                    team |= set(mod.team)

            page_html = build_html_page(
                static=f"..{os_sep}static{os_sep}",
                categories=categories_mod,
                mod_length=len(mods),
                language=language,
                mod_id_to_name=mod_id_to_name,
                is_home_page=False,
            )
            create_page_language(page_html, language)

    # on crée la page par defaut (home)
    tp2_nb = 0
    translation_count = 0
    mod_per_game = {game.value: 0 for game in GameEnum}
    urls = set()

    with LANGUAGE_CONFIG.switch_language("en"):
        mods = ModManager.get_mod_list("en")
        mod_id_to_name = {mod.id: mod.name for mod in mods}

        for mod in mods:
            authors |= set(mod.authors)
            team |= set(mod.team)
            if mod.tp2 not in ("n/a", "non-weidu", ""):
                tp2_nb += 1
            if mod.translation_state != "n/a":
                translation_count += int(len(mod.languages) - 1)
            for game in mod.games:
                mod_per_game[game] += 1
            urls |= set(mod.urls)

        last_added_mods = ModManager.get_last_added_mods(mods, nb=20)
        last_updated_mods = ModManager.get_last_updated_mods(mods, nb=30)
        without_author_mods = ModManager.get_without_author_mods(mods)
        without_tp2_mods = ModManager.get_without_tp2_mods(mods)
        missing_mods = ModManager.get_missing_mods(mods)

        page_html = build_html_page(
            static=f"static{os_sep}",
            is_home_page=True,
            mod_length=len(mods),
            authors_nb=len(authors),
            team_nb=len(team),
            mod_id_to_name=mod_id_to_name,
            tp2_nb=tp2_nb,
            translation_count=translation_count,
            url_count=len(urls),
            mod_per_game=mod_per_game,
            categories={
                HomeCategory(id=1, value="Last Added Mods"): last_added_mods,
                HomeCategory(id=2, value="Last Updated Mods"): last_updated_mods,
                HomeCategory(id=3, value="Unknown Author Mods"): sorted(
                    without_author_mods, key=lambda x: x.name
                ),
                HomeCategory(id=4, value="Unknown Tp2 Mods"): sorted(
                    without_tp2_mods, key=lambda x: x.name
                ),
                HomeCategory(id=5, value="Missing Mods"): sorted(
                    missing_mods, key=lambda x: x.name
                ),
            },
        )
        create_page_language(page_html, "")


class HomeCategory:
    def __init__(self, id, value) -> None:
        self.id = id
        self.value = value


def create_page_language(page_html: str, language: str) -> None:
    dir_path = Path.cwd() / "docs"
    if language:
        dir_path /= language
    dir_path.mkdir(parents=True, exist_ok=True)

    index_page = dir_path / "index.html"
    logger.info(
        f"Generating index page for {language or 'home'}: \x1b]8;;{index_page}\x1b\\{index_page}\x1b]8;;\x1b\\",
    )
    with open(index_page, "w", encoding="utf-8") as f:
        f.write(page_html)
