from dataclasses import dataclass
from pathlib import Path

from pydantic import HttpUrl as PydHttpUrl

from settings import FLAG_DIR, SITE_DIR, image_data


@dataclass(slots=True, kw_only=True)
class Image:
    src: Path
    title: str = ""
    alt: str = ""
    width: int = 32
    height: int = 32


class HttpUrl(PydHttpUrl):
    country_image_suffix: str = "-flag-32.png"

    domain_to_image: dict[str, str] = {
        "artisans-corner.com": "artisans-32.avif",
        "baldursgateworld.fr": "logocc.png",
        "anomaly-studios.fr": "logocc.png",
        # "baldursgatemods.com": "teambg.png",
        "downloads.chosenofmystra.net": "teambg.png",
        "beamdog.com": "beamdog.png",
        "blackwyrmlair.net": "bwl.gif",
        "gibberlings3.net": "g3icon-32.avif",
        "github.com": "github-32.png",
        "github.io": "github-32.png",
        # "havredest.eklablog.fr": "luren.avif",
        "pocketplane.net": "ppg-32.jpg",
        "mediafire.com": "mediafire.png",
        "nexusmods.com": "nexus-32.png",
        "reddit.com": "reddit_76.png",
        "sasha-altherin.webs.com": "ab-logo-32.jpg",
        "sentrizeal.com": "sentrizeal.ico",
        "shsforums.net": "shs_reskit-32.avif",
        "spellholdstudios.net": "shs_reskit-32.avif",
        "bgforge.net": "bgforge.svg",
        "sorcerers.net": "sorcerer-32.avif",
        "sourceforge.net": "sf.png",
        "weaselmods.net": "weasel-32.png",
        "weidu.org": "weidu.ico",
        "clandlan.net": "sp-flag-32.png",
        "trow.cc": "trow-32.png",
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
        if img:
            # cas spécial pour les drapeaux
            if img.endswith(self.country_image_suffix):
                img_data = image_data[self.country_image_suffix].copy()
                img_data["title"] = str(img_data["title"]) % img.removesuffix(
                    self.country_image_suffix
                )
                dir = FLAG_DIR
            else:
                img_data = image_data.get(img, dict())
                dir = SITE_DIR

            return Image(src=dir / img, **img_data)
        return None

    def _image_country(self) -> str:
        country_img = f"{self.tld}{self.country_image_suffix}"
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
