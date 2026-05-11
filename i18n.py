from contextlib import contextmanager
import gettext
from pathlib import Path
import threading

LANGUAGE_DEFAULT = "fr"
LOCALE_DIR = "locales"

translation = gettext.translation(
    "messages", Path.cwd() / LOCALE_DIR, languages=[LANGUAGE_DEFAULT]
)
translation.install()

_current_translation = gettext.translation(
    "messages", Path.cwd() / LOCALE_DIR, languages=[LANGUAGE_DEFAULT]
)


def init_i18n(lang: str):
    global _current_translation
    _current_translation = gettext.translation(
        "messages", Path.cwd() / LOCALE_DIR, languages=[lang], fallback=True
    )


def _g(msg: str) -> str:
    return _current_translation.gettext(msg)


class LanguageConfig:
    _instance = None
    _lock = threading.Lock()
    _local = None

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._language = LANGUAGE_DEFAULT
                cls._instance._local = threading.local()
        return cls._instance

    @property
    def LANGUAGE(self) -> str:
        return getattr(self._local, "language", self._language)

    @LANGUAGE.setter
    def LANGUAGE(self, value):
        self._language = value

    @contextmanager
    def switch_language(self, lang: str):
        """Temporarily switch language in a context"""
        old_lang = getattr(self._local, "language", LANGUAGE_DEFAULT)
        assert self._local is not None
        self._local.language = lang
        init_i18n(lang)
        try:
            yield
        finally:
            self._local.language = old_lang
            init_i18n(old_lang)


LANGUAGE_CONFIG = LanguageConfig()


def set_language(lang: str) -> None:
    init_i18n(lang)
    LANGUAGE_CONFIG.LANGUAGE = lang


def current_language() -> str:
    return LANGUAGE_CONFIG.LANGUAGE


TEMPLATE_TRANSLATIONS = {
    "title": _g("Liste des mods pour IE - La Couronne de Cuivre"),
    "mod": _g("Mod"),
    "home": _g("Accueil"),
    "compatibilities": _g("Compatibilités"),
    "authors": _g("Auteurs"),
    "translators": _g("Traducteurs"),
    "team": _g("Équipe"),
    "link": _g("Lien"),
    "all": _g("Tous"),
    "all_f": _g("Toutes"),
    "translation_state": _g("État de la traduction"),
    "mod_quality": _g("Qualité du mod"),
    "category": _g("Catégorie"),
    "search": _g("Recherche :"),
    "advanced_filters": _g("Filtres avancés"),
    "mod_list": _g("Liste des mods"),
    "author": _g("Auteur"),
    "maintainer": _g("Mainteneur"),
    "back": _g("Retourner aux filtres"),
    "website": _g("Site internet"),
    "discussion": _g("Discussion"),
    "introduction": _g("Introduction"),
    "version": _g("Version"),
    "mod_nb": _g("Mods recensés"),
    "go_to_list": _g("Accéder à la liste"),
    "intros": [
        _g("Voici la liste de mods de la saga Baldur's Gate disponibles au téléchargement."),
        _g(
            'Afin qu\'elle soit la plus précise possible, n\'hésitez pas à remonter sur le dépôt <a href="https://github.com/RiwsPy/lcc-docs/issues">tout problème</a>, signaler des <a href="https://github.com/RiwsPy/lcc-docs/discussions/65">mods non repertoriés</a>, ou encore une <a href="https://github.com/RiwsPy/lcc-docs/discussions/66">erreur</a>.'
        ),
        _g(
            'N\'oubliez pas de consulter le <a href="https://github.com/RiwsPy/lcc-docs/blob/main/README.md">readme</a> avant de contribuer ainsi que les <a href="https://github.com/RiwsPy/lcc-docs/blob/main/CONTRIBUTING.md">guidelines</a>.'
        ),
    ],
    "wargning_title": _g("AVERTISSEMENTS"),
    "warnings": [
        _g(
            'Par sécurité, tous les liens qui proposent un téléchargement direct sont coupés en deux. La première partie est dans le lien et la seconde dans la description, sous la dénomination `Fichier xxx.yy`. Pour avoir un lien valide il peut être nécessaire de reconstituer les deux. Par exemple, pour le mod <a href="#m903">Runic Bladesinger Elven Kit</a>, le lien `https://baldur.cob-bg.pl/download/bg2/kits/` est à regrouper avec `Runiczny_v2.0.zip`.'
        )
    ],
    "mod_name": _g("Nom du mod"),
    "legend": _g("Légende :"),
    "weidu_mod": _g("Mod Weidu"),
}
