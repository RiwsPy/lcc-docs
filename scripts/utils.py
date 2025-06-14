from dataclasses import fields
import json
from pathlib import Path

from models.mod import Mod


class ModManager:
    mod_filename: str = "mods.json"
    root = Path.cwd()

    @classmethod
    def db_path(cls) -> Path:
        return cls.root / "db"

    @classmethod
    def load(cls) -> dict:
        with open(cls.db_path() / cls.mod_filename, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def export(cls, mods: dict) -> None:
        assert mods, "Mods not loaded"

        with open(cls.db_path() / cls.mod_filename, "w", encoding="utf-8") as f:
            json.dump(mods, f, indent=4, ensure_ascii=False)

    @classmethod
    def get_mod_list(cls) -> list[Mod]:
        return [Mod(**mod) for mod in cls.load()]


class CleanModMixin:
    def __init__(self, data: dict):
        self.data = data
        self.cleaned_data = dict()

    def clean_all(self) -> None:
        for field in fields(Mod):
            attr = field.name
            if attr not in self.data:
                continue
            try:
                cleaned_value = getattr(self, f"clean_{attr}")()
            except AttributeError:
                pass
            else:
                if cleaned_value is not None:
                    self.cleaned_data[attr] = cleaned_value


def simplify_url(url: str) -> str:
    if url.startswith(
        ("https://github.com/", "https://forums.beamdog.com/discussion/")
    ) and not url.endswith("https://forums.beamdog.com/discussion/comment/"):
        url = "/".join(url.split("/")[:5])
    return url.removesuffix("/")


with open(ModManager.db_path() / "author_pseudos.json", "r", encoding="utf-8") as f:
    author_pseudos = json.load(f)

AUTHOR_PSEUDOS: dict[str, tuple[str]] = {
    pseudo: k for k, pseudos in author_pseudos.items() for pseudo in pseudos
}
