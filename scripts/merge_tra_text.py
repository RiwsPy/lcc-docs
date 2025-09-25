#!/usr/bin/env python3
import logging

from i18n import LANGUAGE_DEFAULT
from models.mod import MetaStatusEnum
from scripts.extract_tra_text import DATA_SEP
from scripts.utils import ModManager
from settings import DB_PATH

logger = logging.getLogger(__name__)


def parse_line(line: str) -> tuple[int, int, str, int]:
    line_number, mod_id, field_type, idx = line.split(DATA_SEP)
    return int(line_number), int(mod_id), field_type, int(idx)


def merge_translated_text(language):
    """Merge the translated text into the mods_{language}.json, set its status to 'needs_review'."""
    # Load the mods database
    mods = ModManager.load(language=language)

    # Read the translated text
    with open(DB_PATH / f"tra_output_{language}.txt", "r", encoding="utf-8") as f:
        translated_lines = f.readlines()

    # Read the mapping file
    with open(DB_PATH / f"tra_input_map_{language}.txt", "r", encoding="utf-8") as f:
        mapping_lines = f.readlines()

    # Create a mapping of line numbers to translations
    translations = {}
    for i, line in enumerate(translated_lines, 1):
        translations[i] = line.strip()

    # Create a mapping of mod ids to mods
    mapping_id_mod = {mod["id"]: mod for mod in mods}

    # Process the mapping and update mods
    for mapping in mapping_lines:
        line_num, mod_id, field_type, idx = parse_line(mapping)

        # Find the corresponding mod
        mod = mapping_id_mod.get(mod_id)
        if not mod:
            logger.warning(f"Mod {mod_id} not found in {language} database")
            continue

        # Update the appropriate field
        if field_type == "description":
            mod["description"] = translations[line_num]
            mod["description_meta"]["status"] = MetaStatusEnum.NEEDS_REVIEW
        elif field_type == "note":
            # Ensure notes list exists and is long enough
            if "notes" not in mod:
                mod["notes"] = []
            while len(mod["notes"]) <= idx:
                mod["notes"].append("")
            mod["notes"][idx] = translations[line_num]
            mod["notes_meta"]["status"] = MetaStatusEnum.NEEDS_REVIEW

    ModManager.export(mods, language=language)


def main(**kwargs):
    language = kwargs.get("language") or LANGUAGE_DEFAULT
    merge_translated_text(language)
