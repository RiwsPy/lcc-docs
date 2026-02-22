from dataclasses import dataclass
from pathlib import Path

from pydantic import HttpUrl as PydHttpUrl

from settings import FLAG_DIR, SITE_DIR, DomainImageEnum, image_data


@dataclass(slots=True, kw_only=True)
class Image:
    src: Path
    title: str = ""
    alt: str = ""
    width: int = 32
    height: int = 32


class HttpUrl(PydHttpUrl):
    domain_to_image: dict[str, DomainImageEnum] = {
        "artisans-corner.com": DomainImageEnum.ARTISAN,
        "baldursgateworld.fr": DomainImageEnum.CC,
        "anomaly-studios.fr": DomainImageEnum.CC,
        "downloads.chosenofmystra.net": DomainImageEnum.TEAMBG,
        "beamdog.com": DomainImageEnum.BEAMDOG,
        "blackwyrmlair.net": DomainImageEnum.BWL,
        "gibberlings3.net": DomainImageEnum.GIBBER,
        "github.com": DomainImageEnum.GH,
        "github.io": DomainImageEnum.GH,
        # "havredest.eklablog.fr": DomainImageEnum.HAVREDEST,
        "pocketplane.net": DomainImageEnum.PPG,
        "mediafire.com": DomainImageEnum.MEDIAFIRE,
        "nexusmods.com": DomainImageEnum.NEXUS,
        "reddit.com": DomainImageEnum.REDDIT,
        "sentrizeal.com": DomainImageEnum.SENTRIZEAL,
        "shsforums.net": DomainImageEnum.SHS,
        "spellholdstudios.net": DomainImageEnum.SHS,
        "bgforge.net": DomainImageEnum.BGFORGE,
        "sorcerers.net": DomainImageEnum.SORCERER,
        "sourceforge.net": DomainImageEnum.SF,
        "weaselmods.net": DomainImageEnum.WEASEL,
        "weidu.org": DomainImageEnum.WEIDU,
        "trow.cc": DomainImageEnum.TROW,
    }

    @property
    def url(self) -> str:
        return str(self)

    @property
    def is_direct_archive(self) -> bool:
        return bool(
            self.path
            and self.host
            and self.path.lower().endswith((".rar", ".zip", ".7z", ".exe"))
            and not self.host.startswith(("www.mediafire.com", "sorcerers.net"))
        )

    @property
    def tld(self) -> str:
        return self.host.rpartition(".")[-1] if self.host else ""

    @property
    def is_external(self) -> bool:
        return True

    @property
    def image(self) -> Image | None:
        img = self._image_domain() or self._image_country()
        if not img:
            return None

        # cas spécial pour les drapeaux
        country_flag = DomainImageEnum.COUNTRY_FLAG
        if img.endswith(country_flag):
            flag_img_data = image_data[country_flag].copy()
            flag_img_data["title"] = str(flag_img_data["title"]) % img.removesuffix(
                country_flag
            )
            img_dir = FLAG_DIR
        else:
            flag_img_data = image_data.get(img, dict())
            img_dir = SITE_DIR

        return Image(src=img_dir / img, **flag_img_data)

    def _image_country(self) -> str:
        country_img = f"{self.tld}{DomainImageEnum.COUNTRY_FLAG}"
        img = ""
        # auto-select
        if (FLAG_DIR / country_img).exists():
            img = country_img

        return img

    def _image_domain(self) -> str:
        domain = self.host.removeprefix("www.") if self.host else ""
        img = self.domain_to_image.get(domain, "")

        # check sous-domaine
        if not img and domain.count(".") >= 2:
            domain = domain.partition(".")[-1]
            img = self.domain_to_image.get(domain, "")

        return img
