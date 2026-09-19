#!/usr/bin/env python3
from i18n import LANGUAGE_DEFAULT
from models.mod import MetaStatusEnum
from scripts.utils import ModManager
from settings import DB_PATH

DATA_SEP = ";"


def build_line(line_number: int, mod_id: int, field_type: str, idx: int) -> str:
    return DATA_SEP.join([str(line_number), str(mod_id), field_type, str(idx)])


def extract_mods_text(language):
    """
    Extract the text of the mods to translate from the database.

    Outputs:
        - tra_input_{language}.txt: the text of the description and notes to translate
        - tra_input_map_{language}.txt: the map of the text to the mod id, text type and index
    """
    mods = ModManager.load(language=language)

    with (
        open(DB_PATH / f"tra_input_{language}.txt", "w", encoding="utf-8") as out,
        open(DB_PATH / f"tra_input_map_{language}.txt", "w", encoding="utf-8") as map_out,
    ):
        line_number = 1

        for mod in mods:
            mod_id = mod["id"]

            if mod["description_meta"]["status"] == MetaStatusEnum.TODO:
                source = mod["description_meta"]["source"]
                out.write(source + "\n")
                map_line = build_line(line_number, mod_id, "description", 0)
                map_out.write(map_line + "\n")
                line_number += 1

            if mod["notes_meta"]["status"] == MetaStatusEnum.TODO:
                for note_idx, note in enumerate(mod["notes_meta"]["source"]):
                    out.write(note + "\n")
                    map_line = build_line(line_number, mod_id, "note", note_idx)
                    map_out.write(map_line + "\n")
                    line_number += 1


def main(**kwargs):
    language = kwargs.get("language") or LANGUAGE_DEFAULT
    extract_mods_text(language)
