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
        for mod_id in sorted(mods_id_to_data.keys() - translated_mods_ids):
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

        # Suppression des mods en trop dans les traductions
        mod_to_delete = translated_mods_ids - mods_id_to_data.keys()
        if mod_to_delete:
            translated_mods = [mod for mod in translated_mods if mod["id"] not in mod_to_delete]
            logger.info(f"{language}, Mod(s) {mod_to_delete} deleted")

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
                if meta_attr not in translated_mod:
                    continue

                data_source = translated_mod[meta_attr]["source"]
                data_status = translated_mod[meta_attr]["status"]
                have_changed = False
                # la source a changé, on met à jour le statut
                if data_source != mod_main_data[attr]:
                    if data_status == MetaStatusEnum.DONE:
                        if translated_mod[attr]:
                            data_status = MetaStatusEnum.NEEDS_REVIEW
                        else:
                            data_status = MetaStatusEnum.TODO
                    data_source = mod_main_data[attr]
                    have_changed = True

                # la source a été supprimée, on reset la traduction
                if not data_source and (
                    data_status != MetaStatusEnum.DONE or translated_mod[attr]
                ):
                    data_status = MetaStatusEnum.DONE
                    translated_mod[attr] = data_source
                    have_changed = True

                if not have_changed:
                    continue

                translated_mod[meta_attr]["source"] = data_source
                translated_mod[meta_attr]["status"] = data_status
                logger.info(
                    f"{language}, Mod {translated_mod['id']}, attr {attr} have been updated"
                )

        ModManager.export(translated_mods, language=language)
        logger.info(f"{language} check done")

    logger.info("Done")
