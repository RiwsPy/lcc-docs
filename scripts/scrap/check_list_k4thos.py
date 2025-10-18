from itertools import chain

import bs4
from bs4 import BeautifulSoup as bs
import curl_cffi

from scripts.utils import ModManager, simplify_url
from settings import GameEnum

"""
Search differences between lcc-docs and k4thos list.

Since the names of the mods are different, only the URL is used to match the mods.
The logs could be improved.
"""


def main(**kwargs) -> None:
    data = curl_cffi.get(
        "https://k4thos.github.io/EET-Compatibility-List/EET-Compatibility-List.html",
        impersonate="firefox",
    )
    soup = bs(data.content, "html.parser")

    sections = soup.find_all("div", class_="section")[-2:]
    links = list(chain(*[section.find_all("a") for section in sections]))

    print("# Check K4thos list")
    compatible_links = {
        clean_url(str(link.attrs.get("href", "")))
        for link in links
        if link.parent and link.parent.name == "li" and isinstance(link, bs4.Tag)
    }
    print(len(compatible_links), "mods found on the list")
    found_links = set()
    missing_eet_mods = set()

    for mod in ModManager.get_mod_list():
        for url in mod.urls:
            url = simplify_url(url)
            if url in compatible_links:
                found_links.add(url)
                if GameEnum.EET not in mod.games:
                    missing_eet_mods.add(mod)

    if missing_eet_mods:
        print(f"\n## Missing EET compatibility in lcc-list ({len(missing_eet_mods)}):")
        for mod in missing_eet_mods:
            print(mod.id, mod.name)

    not_found_links = compatible_links - found_links
    if not_found_links:
        print(f"\n## Mods not found in lcc-list ({len(not_found_links)}):")
        print("\n".join(sorted(list(not_found_links))))


def clean_url(url: str) -> str:
    return simplify_url(url).replace("http://www.shsforums.net/", "https://www.shsforums.net/")
