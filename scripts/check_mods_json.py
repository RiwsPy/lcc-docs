from dataclasses import fields
from datetime import datetime
import re

from models import Mod, ModStatus
from scripts.utils import ModManager
from settings import CategoryEnum, Games, language_flags


def main():
    check_type = {field.name: field.type for field in fields(Mod)}
    mod_link = re.compile(r"\[\[([^\].]+)\]\]")
    date_regex = re.compile(r"\d{4}-\d{2}")

    mods = ModManager.load()

    mod_names_founded = set()
    category_names = set(CategoryEnum.values())
    game_names = set(Games)
    valid_status = [status.value for status in ModStatus]

    mod_names = set(mod["name"] for mod in mods)
    tp2s = set()
    urls_to_mod = dict()
    nb_warnings = 0

    for mod_data in mods:
        mod = Mod(**mod_data)
        mod_name = mod.name

        # check clés
        diff_keys = check_type.keys() - mod_data.keys()
        assert not diff_keys, f"🔴 {mod_name} : Clé manquante {' | '.join(diff_keys)}"

        diff_keys = mod_data.keys() - check_type.keys()
        assert not diff_keys, (
            f"🔴 {mod_name} : Clé inconnue ; choix possibles : {' | '.join(check_type.keys())}"
        )

        # clean fields type
        for key, value in mod_data.items():
            assert key in check_type and type(value) is check_type[key], (
                f"🔴 {mod_name} : {key} de type non conforme ; attendu : {check_type[key]} ; obtenu : {type(value)}"
            )

        # check links
        for text in [mod.description] + mod.notes:
            links = mod_link.findall(text)
            for link in links:
                assert link in mod_names, (
                    f"🔴 {mod_name} : Lien interne vers un mod inexistant → {link}"
                )

        # clean name unicity
        assert mod_name not in mod_names_founded, f"🔴 {mod_name} : Nom déjà existant"
        mod_names_founded.add(mod_name)

        # clean category
        cat_diff = set(mod.categories) - category_names
        assert not cat_diff, (
            f"🔴 {mod_name} : Catégorie non conforme ; choix possibles : {' | '.join(category_names)}"
        )

        # clean game
        game_diff = set(mod.games) - game_names
        assert not game_diff, (
            f"🔴 {mod_name} : Jeu inconnu ; choix possibles : {' | '.join(game_names)}"
        )

        # clean last_update
        last_update_check = mod.last_update == "" or date_regex.fullmatch(mod.last_update)
        assert last_update_check, (
            f"🔴 {mod_name} : Date non conforme : {mod.last_update}; format attendu : YYYY-MM"
        )
        if mod.last_update:
            try:
                mod_update_date = datetime.strptime(mod.last_update, "%Y-%m")
            except ValueError as e:
                raise AssertionError(
                    f"🔴 {mod_name} : Format de date non conforme : {e}"
                ) from e

            assert datetime(1999, 1, 1) <= mod_update_date <= datetime.today(), (
                f"🔴 {mod_name} : Date impossible : {mod_update_date}"
            )

        # check safe
        assert 0 <= mod.safe <= 2, (
            f"🔴 {mod_name} : Safe non conforme {mod.safe} ; Valeur attendue 0 <= safe <= 2"
        )

        # check status
        assert mod.status in valid_status, (
            f"🔴 {mod_name} : Statut non conforme {mod.status} ; Valeur attendue : {' | '.join(valid_status)}"
        )

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
