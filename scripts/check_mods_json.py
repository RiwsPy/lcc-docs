import re

from scripts.utils import ModManager
from settings import language_flags


def main(**kwargs):
    mod_link = re.compile(r"\[\[([^\].]+)\]\]")

    mods = ModManager.get_mod_list()

    mod_names_founded = set()
    mod_ids_founded = set()
    mod_names = set(mod.name for mod in mods)
    tp2s = set()
    urls_to_mod = dict()
    nb_warnings = 0

    for mod in mods:
        # check links
        for text in [mod.description] + mod.notes:
            links = mod_link.findall(text)
            for link in links:
                assert link in mod_names, (
                    f"🔴 {mod.name} : Lien interne vers un mod inexistant → {link}"
                )

        # check id unicity
        assert mod.id not in mod_ids_founded, f"🔴 {mod.id} : ID déjà existant"
        mod_ids_founded.add(mod.id)

        # check name unicity
        assert mod.name not in mod_names_founded, f"🔴 {mod.name} : Nom déjà existant"
        mod_names_founded.add(mod.name)

        # check urls, warning
        for url in mod.urls:
            if url in urls_to_mod:
                print("🟡 Url doublon", f"({url})", "→", mod.name, "/", urls_to_mod[url])
                nb_warnings += 1
            else:
                urls_to_mod[url] = mod.name

        # check tp2
        if mod.tp2 not in ("", "n/a", "non-weidu"):
            tp2_lower = mod.tp2.lower()
            if tp2_lower in tp2s:
                print("🟡 TP2 doublon →", mod.tp2)
                nb_warnings += 1
            else:
                tp2s.add(tp2_lower)

        # check languages
        for lang in set(mod.languages) - language_flags.keys():
            print("🟡 Langue inconnue →", lang)
            nb_warnings += 1

    if nb_warnings > 0:
        print(f"🟡 {nb_warnings} warnings found")
    print("✅ Tests")


if __name__ == "__main__":
    main()
