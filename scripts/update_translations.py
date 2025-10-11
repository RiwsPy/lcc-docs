import logging

from i18n import LANGUAGE_DEFAULT
from models.mod import MetaStatusEnum
from scripts.utils import ModManager, get_languages

logger = logging.getLogger(__name__)


def main(**kwargs):
    """
    Met à jour les données sources des différents fichiers de traduction
    Rajoute les mod manquants
    """
    mods_main = ModManager.load("")
    mods_id_to_data = {mod["id"]: mod for mod in mods_main}

    for language in get_languages():
        translated_mods = ModManager.load(language=language)

        translated_mods_ids = {mod["id"] for mod in translated_mods}

        # Ajout des nouveaux mods
        for mod_id in mods_id_to_data.keys() - translated_mods_ids:
            if language == LANGUAGE_DEFAULT:
                mod_data = {"id": mod_id}
            else:
                mod_data = {
                    "id": mod_id,
                    "description": "",
                    "description_meta": {
                        "status": MetaStatusEnum.DONE,
                        "source": "",
                    },
                    "notes": list(),
                    "notes_meta": {
                        "status": MetaStatusEnum.DONE,
                        "source": list(),
                    },
                }
            translated_mods.append(mod_data)
            logger.info(f"{language}, Mod {mod_id} added")

        # Mise à jour des données source des traductions
        for translated_mod in translated_mods:
            mod_main_data = mods_id_to_data.get(translated_mod["id"])
            if mod_main_data is None:
                logger.warning(
                    f"{language}, Mod {translated_mod['id']} not found in main database"
                )
                continue

            for attr in ("description", "notes"):
                meta_attr = f"{attr}_meta"
                if (
                    meta_attr in translated_mod
                    and translated_mod[meta_attr]["source"] != mod_main_data[attr]
                ):
                    if translated_mod[meta_attr]["status"] == MetaStatusEnum.DONE:
                        if translated_mod[attr]:
                            next_status = MetaStatusEnum.NEEDS_REVIEW
                        else:
                            next_status = MetaStatusEnum.TODO
                        translated_mod[meta_attr]["status"] = next_status

                    translated_mod[meta_attr]["source"] = mod_main_data[attr]
                    logger.info(
                        f"{language}, Mod {translated_mod['id']}, attr {attr} have been updated"
                    )

        ModManager.export(translated_mods, language=language)
        logger.info(f"{language} check done")

    logger.info("Done")
