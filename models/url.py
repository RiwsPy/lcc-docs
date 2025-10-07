from dataclasses import dataclass
from os import path as os_path
import re

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


class Url:
    domain_regex = re.compile(r"https?://(www\.)?(?P<domain>[^/]*).*")
    country_image_suffix = "-flag-32.png"

    def __init__(self, url):
        self.url = url
        self.img = None

        img = self.get_image_name()
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
            self.img = Image(src=img_dir, **img_data)

    def get_image_special(self) -> str:
        domain = self.get_domain()
        img = domain_to_image.get(domain, "")

        # check sous-domaine
        if not img and domain.count(".") >= 2:
            domain = domain.partition(".")[-1]
            img = domain_to_image.get(domain, "")

        return img

    def get_tld(self) -> str:
        return self.get_domain().rpartition(".")[-1]

    def get_image_country(self) -> str:
        country_img = f"{self.get_tld()}{self.country_image_suffix}"
        img = ""
        # auto-select
        if (IMG_ROOT / FLAG_DIR / country_img).exists():
            img = country_img

        return img

    def get_image_name(self) -> str:
        return self.get_image_special() or self.get_image_country()

    def get_domain(self) -> str:
        domain = ""
        domain_match = self.domain_regex.search(self.url)
        if domain_match:
            domain = domain_match.group("domain")
        return domain or "localhost"

    @property
    def is_external(self) -> bool:
        return self.url.startswith("http")
