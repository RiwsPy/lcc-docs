#!/usr/bin/env python3
import json
from pathlib import Path

from settings import LANGUAGE_DEFAULT


def build_translated_mods(language):
    root = Path.cwd()

    # Read the translated text
    with open(root / "db" / f"tra_output_{language}.txt", "r", encoding="utf-8") as f:
        translated_lines = f.readlines()

    # Read the mapping file
    with open(root / "db" / f"tra_input_map_{language}.txt", "r", encoding="utf-8") as f:
        mapping_lines = f.readlines()

    # Read the original mods_{language} file
    with open(root / "db" / f"mods_{language}.json", "r", encoding="utf-8") as f:
        mods = json.load(f)

    # Create a mapping of line numbers to translations
    translations = {}
    for i, line in enumerate(translated_lines, 1):
        translations[i] = line.strip()

    # Process the mapping and update mods
    for mapping in mapping_lines:
        line_num, mod_info = mapping.strip().split(": ", 1)
        line_num = int(line_num)

        # Parse the mod info
        parts = mod_info.split()
        mod_id = int(parts[1])
        field_type = parts[2]  # 'description' or 'note'

        # Find the corresponding mod
        mod = next((m for m in mods if m["id"] == mod_id), None)
        if not mod:
            continue

        # Update the appropriate field
        if field_type == "description":
            mod["description"] = translations[line_num]
            mod["description_meta"]["status"] = "outdated"
        elif field_type == "note":
            note_idx = int(parts[3])
            # Ensure notes list exists and is long enough
            if "notes" not in mod:
                mod["notes"] = []
            while len(mod["notes"]) <= note_idx:
                mod["notes"].append("")
            mod["notes"][note_idx] = translations[line_num]
            mod["notes_meta"]["status"] = "outdated"

    # Write the translated mods to a new file
    with open(root / "db" / f"mods_{language}.json", "w", encoding="utf-8") as f:
        json.dump(mods, f, ensure_ascii=False, indent=4)


def main(**kwargs):
    language = kwargs.get("language") or LANGUAGE_DEFAULT
    build_translated_mods(language)
