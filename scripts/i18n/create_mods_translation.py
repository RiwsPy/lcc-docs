import logging

from i18n import LANGUAGE_DEFAULT, set_language
from models.mod import MetaStatusEnum
from scripts.utils import ModManager
from settings import DB_PATH

logger = logging.getLogger(__name__)


def main(**kwargs):
    language = kwargs.get("language") or LANGUAGE_DEFAULT

    filename = DB_PATH / ModManager.get_language_filename(language=language)
    if filename.exists():
        logger.warning(f"{filename} already exists")
        return

    set_language(language)
    mods = ModManager.get_mod_list(language="")
    mods.sort(key=lambda x: x.id)
    mods_lang = [
        {
            "id": mod.id,
            "description": "",
            "description_meta": {
                "status": MetaStatusEnum.TODO if mod.description else MetaStatusEnum.DONE,
                "source": mod.description,
            },
            "notes": list(),
            "notes_meta": {
                "status": MetaStatusEnum.TODO if mod.notes else MetaStatusEnum.DONE,
                "source": mod.notes,
            },
        }
        for mod in mods
    ]
    ModManager.export(mods_lang, language=language)
