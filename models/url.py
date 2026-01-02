from dataclasses import dataclass
from functools import cached_property
from os import path as os_path

from pydantic import HttpUrl as PydHttpUrl

from settings import (
    FLAG_DIR,
    IMG_ROOT,
    SITE_DIR,
    domain_to_image,
    image_data,
)


@dataclass(slots=True, kw_only=True)
class Image:
    src: str
    title: str = ""
    alt: str = ""
    width: int = 32
    height: int = 32


class HttpUrl(PydHttpUrl):
    country_image_suffix = "-flag-32.png"

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

    @cached_property
    def img(self) -> Image | None:
        def image_country(self) -> str:
            country_img = f"{self.tld}{self.country_image_suffix}"
            img = ""
            # auto-select
            if (IMG_ROOT / FLAG_DIR / country_img).exists():
                img = country_img

            return img

        def image_special(self) -> str:
            domain = self.host.removeprefix("www.") if self.host else ""
            img = domain_to_image.get(domain, "")

            # check sous-domaine
            if not img and domain.count(".") >= 2:
                domain = domain.partition(".")[-1]
                img = domain_to_image.get(domain, "")

            return img

        def image_name(self) -> str:
            return image_special(self) or image_country(self)

        img = image_name(self)
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

            img_dir = os_path.join("img", dir, img)
            return Image(src=img_dir, **img_data)
        return None
