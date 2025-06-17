#!/usr/bin/env python3
import json
from pathlib import Path

from scripts.utils import ModManager
from settings import LANGUAGE_DEFAULT


def extract_mods_text(language):
    root = Path.cwd()
    filename = ModManager.db_path() / ModManager.get_language_filename(language=language)

    # use root in paths
    with open(filename, "r", encoding="utf-8") as f:
        mods = json.load(f)

    with (
        open(root / "db" / f"tra_input_{language}.txt", "w", encoding="utf-8") as out,
        open(root / "db" / f"tra_input_map_{language}.txt", "w", encoding="utf-8") as map_out,
    ):
        line_number = 1

        for mod in mods:
            mod_id = mod["id"]

            if mod["description_meta"]["status"] == "todo":
                # get description_meta.source
                source = mod["description_meta"]["source"]
                out.write(source + "\n")
                map_out.write(f"{line_number}: mod {mod_id} description\n")
                line_number += 1

            # Write each note on a new line, check if note list is not empty and note is not empty string
            if mod["notes_meta"]["status"] == "todo":
                for note_idx, note in enumerate(mod["notes_meta"]["source"]):
                    out.write(note + "\n")
                    map_out.write(f"{line_number}: mod {mod_id} note {note_idx}\n")
                    line_number += 1


def main(**kwargs):
    language = kwargs.get("language") or LANGUAGE_DEFAULT
    extract_mods_text(language)
