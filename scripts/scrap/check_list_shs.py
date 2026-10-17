import logging

from bs4 import BeautifulSoup as bs
import curl_cffi

from scripts.cleaner.utils import CleanModMixin
from scripts.utils import ModManager, github_url_prefix, minify_url

LOGGER = logging.getLogger(__name__)


def main(**kwargs):
    lcc_mods = ModManager.get_mod_list("")

    shs_mod_list_url = "https://mods.shsforums.net/"
    req = curl_cffi.get(shs_mod_list_url, impersonate="firefox")
    if req.status_code != 200:
        print(f"Error {req.status_code} for {shs_mod_list_url}")
        return None

    lcc_mod_gh_links = {
        minify_url(url.url): mod
        for mod in lcc_mods
        for url in mod.urls
        if url.url.startswith(github_url_prefix)
    }

    lcc_mod_names = {mod.name: mod for mod in lcc_mods}

    html_page = bs(req.content, "html.parser")
    mod_categories = html_page.find_all("ul", class_="mod-list")

    exclude_names = {
        "Sirene",  # external mod with specific link
        "BiG World Project - English",  # not a mod
        "BiG World Install Pack",
        "Lol's Kit Guide",
        "aTweaks",  # https://github.com/TotoR115/aTweaks is up-to-date
        "PaintBG for BG:EE",
        "AI Scripting Tutorial",
        "BAM Resizer",
        "BAM Workshop",
        "Infinity Engine Game Launcher",
        "Palette Generator",
        "PS BAM",
        "Saga Baldur's Gate Conversion",
        "tile2ee",
        "tileconv",
        "tis2ovl",
        "Traify Tool",
        "WeiDU Syntax Highlighters for Notepad++",
        "K'aeloree's Unfinished Varia",
        "SHS Readme #1",
        "SHS Readme #2",
    }

    print("\n##### Missing & Compatibility #####\n")
    # Shs mods
    for mod_category in mod_categories:
        for mod in mod_category.find_all("li"):
            shs_mod = get_mod_data(mod)
            for url in shs_mod["urls"]:
                lcc_mod = lcc_mod_gh_links.get(url)
                if not lcc_mod:
                    if shs_mod["name"] not in exclude_names:
                        print(f"{shs_mod['name']} github link not found in lcc list")
                else:
                    diff_games = set(shs_mod["games"]) - set(lcc_mod.games)
                    if diff_games:
                        print(f"{shs_mod['name']} had more compatibility {diff_games}")

    print("\n##### Miscellaneous #####\n")
    not_found_mod_nb = 0
    not_found_link_nb = 0
    miscs = html_page.find_all("ul", class_="template-list")
    if not miscs:
        print("Miscellaneous category not found.")
        return

    exclude_categories = {"Tools", "Resources"}

    for misc in miscs:
        category = misc.find_previous_sibling("h4")
        if category and category.next_element in exclude_categories:
            continue
        for mod in misc.find_all("li"):
            link = mod.find("a").get("href", "").strip("/")
            name, _, author = mod.text.partition(" by ")

            if link not in lcc_mod_gh_links and name not in exclude_names:
                print(f"{name} ({link}) link not found in lcc list")
                not_found_link_nb += 1
                if name not in lcc_mod_names:
                    print(f"{name} ({link}) mod not found in lcc list")
                    not_found_mod_nb += 1

    print(f"{not_found_link_nb} misc liens non trouvés")
    print(f"{not_found_mod_nb} misc mods non trouvés")


def get_mod_data(mod) -> dict:
    game_data = {
        "name": mod.find("div", class_="mod-name").text,
        "urls": list(),
    }

    tags = mod.find("span", class_="mod-tag")
    if tags.text:
        game_data["games"] = tags.text

    mod_links = mod.find("span", class_="mod-links")
    if mod_links:
        for link in mod_links.find_all("a"):
            if link.text.lower() == "github":
                game_data["urls"].append(link.get("href"))
                break

    clean_mod = ShsCleanMod(game_data)
    clean_mod.clean_all()
    return clean_mod.cleaned_data


class ShsCleanMod(CleanModMixin):
    def clean_games(self) -> set[str]:
        games_str = (
            self.data["games"].replace("BG1", "BG").replace("IWD1", "IWD").replace(":", "")
        )
        return set(games_str.split(" ")) - {"external", "IWD2EE"}

    def clean_urls(self) -> list[str]:
        return [minify_url(url) for url in self.data["urls"]]
