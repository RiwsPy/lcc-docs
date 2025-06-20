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
