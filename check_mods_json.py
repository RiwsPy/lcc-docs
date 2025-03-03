from dataclasses import fields
import re

from models import Mod, ModStatus
from scripts.utils import ModManager
from settings import CategoryEnum, Games


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

    for mod in mods:
        mod_name = mod["name"]

        # check clés
        diff_keys = check_type.keys() - mod.keys()
        assert not diff_keys, f"{mod_name} : Clé manquante {' | '.join(diff_keys)}"

        diff_keys = mod.keys() - check_type.keys()
        assert not diff_keys, (
            f"{mod_name} : Clé inconnue ; choix possibles : {' | '.join(check_type.keys())}"
        )

        # clean fields type
        for key, value in mod.items():
            assert key in check_type and type(value) is check_type[key], (
                f"{mod_name} : {key} de type non conforme ; attendu : {check_type[key]} ; obtenu : {type(value)}"
            )

        # check links
        for text in [mod["description"]] + mod["notes"]:
            links = mod_link.findall(text)
            for link in links:
                assert link in mod_names, (
                    f"{mod_name} : Lien interne vers un mod inexistant → {link}"
                )

        # clean name unicity
        assert mod_name not in mod_names_founded, f"{mod_name} : Nom déjà existant"
        mod_names_founded.add(mod_name)

        # clean category
        cat_diff = set(mod["categories"]) - category_names
        assert not cat_diff, (
            f"{mod_name} : Catégorie non conforme ; choix possibles : {' | '.join(category_names)}"
        )

        # clean game
        game_diff = set(mod["games"]) - game_names
        assert not game_diff, (
            f"{mod_name} : Jeu inconnu ; choix possibles : {' | '.join(game_names)}"
        )

        # clean last_update
        last_update_check = mod["last_update"] == "" or date_regex.fullmatch(mod["last_update"])
        assert last_update_check, (
            f"{mod_name} : Date non conforme : {mod['last_update']}; format attendu : YYYY-MM"
        )

        # check safe
        assert 0 <= mod["safe"] <= 2, (
            f"{mod_name} : Safe non conforme {mod['safe']} ; Valeur attendue 0 <= safe <= 2"
        )

        # check status
        assert mod["status"] in valid_status, (
            f"{mod_name} : Statut non conforme {mod['status']} ; Valeur attendue : {' | '.join(valid_status)}"
        )

    print("🟢 Tests 🟢")


if __name__ == "__main__":
    main()
