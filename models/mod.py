from dataclasses import dataclass
import enum
import re

from models.url import Url
from models.utils import slugify
from settings import CategoryEnum, Games, attrs_icon_data, language_translate

link_regex = re.compile(r"\[\[[^].]+\]\]")
quote_regex = re.compile(r"`[^`]+`")


class ModStatus(enum.StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    EMBED = "embed"
    MISSING = "missing"
    OBSOLETE = "obsolete"
    WIP = "wip"


@dataclass(slots=True, kw_only=True)
class Icon:
    icon: str
    label: str


@dataclass(kw_only=True, eq=False, frozen=True)
class Mod:
    name: str
    categories: list
    urls: list
    notes: list
    description: str
    team: list
    games: list
    safe: int
    translation_state: str
    languages: list
    authors: list
    status: str
    last_update: str
    tp2: str

    @property
    def id(self) -> str:
        return slugify(self.name)

    def get_status(self):
        return ModStatus(self.status)

    @property
    def is_weidu(self) -> bool:
        return self.tp2 != "non-weidu"

    def get_urls(self) -> list[Url]:
        # Pour éviter d'afficher des liens morts tout en les conservant
        if self.get_status() == ModStatus.MISSING:
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

    def convert_txt(self, txt: str) -> str:
        return self._convert_quote(self._convert_pipe(self._convert_link(txt)))

    def _convert_quote(self, txt: str) -> str:
        quoted_txt = txt
        for quote in quote_regex.findall(quoted_txt):
            quoted_txt = quoted_txt.replace(
                quote, f'<span class="quote">{quote.strip("`")}</span>'
            )

        return quoted_txt

    def _convert_link(self, txt: str) -> str:
        linked_txt = txt
        for link in link_regex.findall(txt):
            mod_name = link.strip("[] ")
            linked_txt = linked_txt.replace(
                link, f'<a href="#{slugify(mod_name)}">{mod_name}</a>'
            )

        return linked_txt

    def _convert_pipe(self, txt: str) -> str:
        return txt.replace("|", "<br/>")

    def get_description(self) -> str:
        return self.convert_txt(self.description)

    def get_categories(self) -> list[CategoryEnum]:
        return [CategoryEnum(cat) for cat in self.categories]

    @property
    def safe_note(self) -> int:
        note = 2
        if self.is_outdated:
            note -= 1
        if not self.is_weidu:
            note -= 1
        if "temnix" in self.authors:  # déso
            note -= 1
        if self.get_status() == ModStatus.ARCHIVED:
            note -= 1
        elif self.get_status() in (ModStatus.EMBED, ModStatus.OBSOLETE):
            note = 0
        elif self.get_status() in (ModStatus.WIP, ModStatus.MISSING):
            note = min(1, note)
        return max(0, note)

    @property
    def is_EE(self) -> bool:
        return bool(set(self.games) & set(Games.EE()))

    @property
    def is_outdated(self) -> bool:
        # EE 2.0 sortie en avril 2016, on considère que tous les mods EE faits avant cette date sont incompatibles
        # EE 2.6 sortie en avril 2021 : sont outdated les mods d'interface et de modification d'exe (pas de catégorie associée)
        return bool(
            self.last_update
            and self.is_EE
            and (
                self.last_update < "2016-04"
                or (self.last_update < "2021-04" and "Interface" in self.categories)
            )
        )

    def get_auto_notes(self) -> list:
        auto_notes = list()

        # Don't download files directly
        for url in self.urls:
            if self.url_is_direct_archive(url):
                filename = url.rsplit("/", 1)[-1]
                auto_notes.append(f"Fichier `{filename}`.")

        # check language
        if len(self.languages) == 1 and self.languages[0] not in ("fr", "en"):
            language = language_translate["fr"].get(self.languages[0], "langue inconnue")
            auto_notes.append(f"Ce mod n'est disponible qu'en {language}.")

        if self.is_outdated and self.safe <= 1:
            year, _ = self.last_update.split("-")
            if self.is_EE:
                auto_notes.append(
                    f"⚠️ EE : La dernière mise à jour date de {year}. Ce mod pourrait ne pas fonctionner avec la dernière version du jeu."
                )

        if not self.is_weidu:
            auto_notes.append(
                "⚠️ WeiDU : Ce mod écrase les fichiers et ne peut être désinstallé. Installez-le à vos risques et périls."
            )
        if self.get_status() == ModStatus.ARCHIVED:
            auto_notes.append(
                "Ce mod a été archivé par son auteur/mainteneur qui ne semble pas vouloir lui donner suite."
            )
        elif self.get_status() == ModStatus.WIP:
            auto_notes.append("Ce mod est toujours en cours de réalisation.")
        elif self.get_status() == ModStatus.MISSING:
            if self.urls:
                url = self.urls[0]
                note = f"Ce mod a disparu de <a href='{url}' target='_blank'>{url}</a>."
            else:
                note = "Ce mod a disparu."
            auto_notes.append(note)
        # if self.team:
        #     auto_notes.append(
        #         f"Traducteur{'s' * (len(self.team) > 1)} 🇲🇫 : {self.get_team_str()}"
        #     )

        return auto_notes

    @staticmethod
    def url_is_direct_archive(url: str) -> bool:
        url = url.lower()
        return (url.endswith((".rar", ".zip", ".7z", ".exe"))) and not url.startswith(
            ("https://www.mediafire.com/", "https://sorcerers.net/")
        )

    def get_team_str(self) -> str:
        team_html = [f"<span class='translator'>{member}</span>" for member in self.team]
        if not team_html:
            return ""
        elif len(team_html) == 1:
            return team_html[0]
        else:
            *without_last, last = team_html
            return ", ".join(without_last) + f" et {last}"

    def get_notes(self) -> list:
        return [self.convert_txt(note) for note in self.notes + self.get_auto_notes()]

    def get_games(self) -> list:
        return [game for game in Games if game in self.games]
