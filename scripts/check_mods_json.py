from collections import Counter
import re
from typing import Pattern

from iteration_utilities import duplicates
from pydantic import HttpUrl

from scripts.utils import ModManager, get_languages
from settings import language_flags

mod_link: Pattern = re.compile(r"\[\[([0-9]+)\]\]")


def main(**kwargs):
    # check id unicity
    mod_list = ModManager.load("")
    duplicate_ids = list(duplicates(str(mod["id"]) for mod in mod_list))
    assert not duplicate_ids, f"🔴 ID duplicates : {' ; '.join(duplicate_ids)}"

    for language in get_languages():
        check_json(language)

    # check tp2 unicity
    duplicate_tp2s = set(duplicates(str(mod["tp2"]) for mod in mod_list))
    duplicate_tp2s -= {"", "n/a", "non-weidu"}
    if duplicate_tp2s:
        print(
            f"🟡 Global TP2 duplicates ({len(duplicate_tp2s)}) → {' ; '.join(duplicate_tp2s)}"
        )

    print("✅ Tests")


def check_json(language) -> None:
    mods = ModManager.get_mod_list(language=language)

    mod_ids = set(str(mod.id) for mod in mods)
    nb_warnings = 0
    mod_urls: list[HttpUrl] = list()

    for mod in mods:
        mod_urls.extend(mod.urls)

        # check links
        text = ";".join([mod.description] + mod.notes)
        id_links = mod_link.findall(text)
        notfound_ids = set(id_links) - mod_ids
        assert not notfound_ids, (
            f"🔴 {language} {mod.id} : Internal link to a non-existent mod → {notfound_ids}"
        )

        # check languages
        for lang in set(mod.languages) - language_flags.keys():
            print(f"🟡 {language} Unknown lang →", lang)
            nb_warnings += 1

    # check urls
    duplicate_urls_counter = Counter(duplicates(mod_urls))
    for url, nb_occurence in duplicate_urls_counter.items():
        print(f"🟡 {language} Url duplicates: {url} → ({nb_occurence + 1})")
        nb_warnings += nb_occurence

    if nb_warnings > 0:
        print(f"🟡 {language} {nb_warnings} warnings found")
