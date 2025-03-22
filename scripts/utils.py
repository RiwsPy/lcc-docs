import json
from pathlib import Path


class ModManager:
    mod_filename: str = "mods.json"
    root = Path.cwd()

    @classmethod
    def load(cls) -> dict:
        with open(cls.root / cls.mod_filename, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def export(cls, mods: dict) -> None:
        assert mods, "Mods not loaded"

        with open(cls.root / cls.mod_filename, "w", encoding="utf-8") as f:
            json.dump(mods, f, indent=4, ensure_ascii=False)
