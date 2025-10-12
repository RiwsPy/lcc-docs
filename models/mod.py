from datetime import datetime
import enum
import re
from typing import Annotated, Literal

from pydantic import ConfigDict, StringConstraints, field_validator
from pydantic.dataclasses import dataclass

from i18n import _g, current_language
from models.url import Url
from settings import (
    CategoryEnum,
    GameEnum,
    TranslationStateEnum,
    attrs_icon_data,
    language_flags,
)

link_regex = re.compile(r"\[\[[^].]+\]\]")
external_link_regex = re.compile(r"\[(?P<name>[^\]]+)\]\((?P<url>[^)]+)\)")
quote_regex = re.compile(r"`[^`]+`")
YearMonthFormat = Annotated[str, StringConstraints(pattern=r"^(\d{4}-\d{2})?$")]


class ModStatus(enum.StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    EMBED = "embed"
    MISSING = "missing"
    OBSOLETE = "obsolete"
    WIP = "wip"
    HIDDEN = "hidden"


class MetaStatusEnum(enum.StrEnum):
    DONE = "done"
    NEEDS_REVIEW = "needs_review"
    TODO = "todo"


@dataclass(slots=True, kw_only=True)
class Icon:
    icon: str
    label: str


@dataclass(kw_only=True, eq=False, frozen=True, config=ConfigDict(extra="forbid"))
class Mod:
    id: int
    name: str
    categories: list[CategoryEnum]
    urls: list[str]
    notes: list[str]
    description: str
    team: list[str]
    games: list[GameEnum]
    safe: Literal[0, 1, 2]
    translation_state: TranslationStateEnum
    languages: list[str]
    authors: list[str]
    status: ModStatus
    last_update: YearMonthFormat
    tp2: str
    description_meta: dict = None
    notes_meta: dict = None
    urls_extra: list[str] = None
    notes_extra: list[str] = None

    @field_validator("last_update")
    def check_last_update(cls, v):
        if not v:
            return v
        current_month = datetime.now().strftime("%Y-%m")
        if "1999-01" <= v <= current_month:
            return v
        raise ValueError(
            f"Date impossible, doit être comprise entre 1999-01 et {current_month}"
        )

    @property
    def translation_state_auto(self) -> str:
        if self.translation_state == "auto":
            if not self.languages:
                return "todo"
            return "yes" if current_language() in self.languages else "no"
        return self.translation_state

    @property
    def is_weidu(self) -> bool:
        return self.tp2 != "non-weidu"

    def get_urls(self) -> list[Url]:
        # Pour éviter d'afficher des liens morts tout en les conservant
        if self.status == ModStatus.MISSING:
            return list()
        urls = self.urls.copy()
        # troncate url to remove zip and rar files
        for i, url in enumerate(urls):
            if self.url_is_direct_archive(url):
                urls[i] = url.rsplit("/", 1)[0] + "/"
        return [Url(url) for url in urls]

    @property
    def icons(self) -> list[Icon]:
        icons = list()
        for attr, data_icons in attrs_icon_data.items():
            value = getattr(self, attr)
            for k, v in data_icons.items():
                if value in k:
                    data_icon = v
                    break
            else:
                raise ValueError(f"icon not found for {self.name}")
            icons.append(Icon(**data_icon))

        return icons

    def convert_txt(self, txt: str, mod_id_to_name: dict | None = None) -> str:
        return self._convert_quote(
            self._convert_pipe(self._convert_link(txt, mod_id_to_name=mod_id_to_name))
        )

    def _convert_quote(self, txt: str) -> str:
        quoted_txt = txt
        for quote in quote_regex.findall(quoted_txt):
            quoted_txt = quoted_txt.replace(
                quote, f'<span class="quote">{quote.strip("`")}</span>'
            )

        return quoted_txt

    def _convert_link(self, txt: str, mod_id_to_name: dict | None = None) -> str:
        linked_txt = txt
        for link in link_regex.findall(txt):
            mod_id = link.strip("[] ")
            if mod_id_to_name is None:
                mod_name = mod_id
            else:
                mod_name = mod_id_to_name.get(mod_id, mod_id)
            linked_txt = linked_txt.replace(link, f'<a href="#m{mod_id}">{mod_name}</a>')
        for link in external_link_regex.findall(linked_txt):
            name, url = link
            linked_txt = linked_txt.replace(
                f"[{name}]({url})", f'<a href="{url}" target="_blank">{name}</a>'
            )

        return linked_txt

    def _convert_pipe(self, txt: str) -> str:
        return txt.replace("|", "<br/>")

    def get_description(self, mod_id_to_name: dict | None = None) -> str:
        return self.convert_txt(self.description, mod_id_to_name=mod_id_to_name)

    @property
    def safe_note(self) -> int:
        note = 2
        if self.is_outdated:
            note -= 1
        if not self.is_weidu:
            note -= 1
        if "temnix" in self.authors:  # déso
            note -= 1
        if self.status == ModStatus.ARCHIVED:
            note -= 1
        elif self.status in (ModStatus.EMBED, ModStatus.OBSOLETE):
            note = 0
        elif self.status in (ModStatus.WIP, ModStatus.MISSING):
            note = min(1, note)
        return max(0, note)

    @property
    def is_EE(self) -> bool:
        return bool(set(self.games) & set(GameEnum.EE()))

    @property
    def is_outdated(self) -> bool:
        # EE 2.0 sortie en avril 2016, on considère que tous les mods EE faits avant cette date sont incompatibles
        # EE 2.6 sortie en avril 2021 : sont outdated les mods d'interface et de modification d'exe (pas de catégorie associée)
        return bool(
            self.last_update
            and self.is_EE
            and (
                self.last_update < "2016-04"
                or (self.last_update < "2021-04" and CategoryEnum.INTERFACE in self.categories)
            )
        )

    def get_auto_notes(self) -> list[str]:
        auto_notes = list()

        # Don't download files directly
        for url in self.urls:
            if self.url_is_direct_archive(url):
                filename = url.rsplit("/", 1)[-1]
                auto_notes.append(_g("Fichier `{filename}`.").format(filename=filename))

        if self.is_outdated and self.safe <= 1:
            year, _ = self.last_update.split("-", 1)
            if self.is_EE:
                auto_notes.append(
                    _g(
                        "⚠️ EE : La dernière mise à jour date de {year}. Ce mod pourrait ne pas fonctionner avec la dernière version du jeu."
                    ).format(year=year)
                )

        if not self.is_weidu:
            auto_notes.append(
                _g(
                    "⚠️ WeiDU : Ce mod écrase les fichiers et ne peut être désinstallé. Installez-le à vos risques et périls."
                )
            )
        if self.status == ModStatus.ARCHIVED:
            auto_notes.append(
                _g(
                    "Ce mod a été archivé par son auteur/mainteneur qui ne semble pas vouloir lui donner suite."
                )
            )
        elif self.status == ModStatus.WIP:
            auto_notes.append(_g("Ce mod est toujours en cours de réalisation."))
        elif self.status == ModStatus.MISSING:
            if self.urls:
                url = self.urls[0]
                note = _g(
                    "Ce mod a disparu de <a href='{url}' target='_blank'>{url}</a>."
                ).format(url=url)
            else:
                note = _g("Ce mod a disparu.")
            auto_notes.append(note)

        # check language
        if (
            self.languages
            and self.translation_state_auto != "n/a"
            and current_language() not in self.languages
        ):
            country_flags = ""
            for language in sorted(self.languages):
                country_flags += f" {language_flags.get(language, '??')}"
            auto_notes.append(_g("Disponible en {language}.").format(language=country_flags))

        return auto_notes

    @staticmethod
    def url_is_direct_archive(url: str) -> bool:
        url = url.lower()
        return (url.endswith((".rar", ".zip", ".7z", ".exe"))) and not url.startswith(
            ("https://www.mediafire.com/", "https://sorcerers.net/")
        )

    def get_notes(self, mod_id_to_name: dict | None = None) -> list[str]:
        return [
            self.convert_txt(note, mod_id_to_name=mod_id_to_name)
            for note in self.notes + self.get_auto_notes()
        ]

    @property
    def is_bws_compatible(self) -> bool:
        return (
            GameEnum.EET in self.games
            and self.translation_state_auto
            in (TranslationStateEnum.YES, TranslationStateEnum.NA, TranslationStateEnum.TODO)
            and self.tp2 not in ("non-weidu", "n/a")
            and self.status in (ModStatus.ACTIVE, ModStatus.EMBED, ModStatus.HIDDEN)
        )

    @property
    def games_ordered(self) -> list[str]:
        return [game for game in GameEnum if game in self.games]
