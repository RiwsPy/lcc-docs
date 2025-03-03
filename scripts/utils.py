import json
from pathlib import Path


class ModManager:
    mod_filename: str = "mods.json"
    root = Path.cwd()

    @staticmethod
    def load() -> dict:
        with open(__class__.root / __class__.mod_filename, "r") as f:
            return json.load(f)

    @staticmethod
    def export(mods: dict) -> None:
        assert mods, "Mods not loaded"

        with open(__class__.root / __class__.mod_filename, "w") as f:
            json.dump(mods, f, indent=4, ensure_ascii=False)
