import re

from scripts.cleaner import Tp2Cleaner
from scripts.manager.utils import ManagerMixin


class Tp2Manager(ManagerMixin):
    clean_class = Tp2Cleaner

    # // ou /* */
    # FIXME: on peut avoir des cas sans espace comme `REPLACE ~9999995~ @10//[Movie]BioWare and IE Logos``
    comment_line_regex = re.compile(r"^//.*|\s//.*", flags=re.MULTILINE)
    comment_block_regex = re.compile(r"/\*.*?\*/", flags=re.DOTALL)

    # ~ ~ ou " "
    # FIXME: parfois rien : BEGIN @0
    string_value = '[~"](.*?)[~"]'
    string_regex = re.compile(rf"{string_value}")
    author_name_regex = re.compile(rf"\bAUTHOR\s+{string_value}", flags=re.DOTALL)
    mod_name_regex = re.compile(rf"\n\bBEGIN\s+{string_value}", flags=re.DOTALL)
    # On retire les checks s'ils sont suivis par: `? 1 : 0`
    # On retire les checks qui sont précédés par `NOT ` ou par `!`
    game_names_regex = re.compile(
        r"(?<!\bNOT\s)(?<!\!)(?:GAME_IS|ENGINE_IS|GAME_INCLUDES|GAME_SUPPORTS)\s+[~\"](.*?)[~\"](?!.*\? 1 : 0)",
        flags=re.DOTALL,
    )
    # FIXME: saut de ligne non pris en compte pour la traduction FR de `Tsujatha Melalor`
    language_block_regex = re.compile(
        r"\bLANGUAGE\s+((?:[~\"](.*?)[~\"]\s*)+)", flags=re.DOTALL
    )
    # author (email)
    bracket_author_regex = re.compile(r"\s+\(.*?\)")

    version_regex = re.compile(r"\bVERSION\s+[~\"](.+)[~\"]")

    def __init__(self, content: str):
        super().__init__(content)
        self.content_clean = self.clean_comments(self.content)

    @classmethod
    def clean_comments(cls, content: str) -> str:
        content = cls.comment_block_regex.sub("", content)
        content = cls.comment_line_regex.sub("", content)
        return content

    def get_authors(self) -> list[str]:
        return self.author_name_regex.findall(self.content_clean)

    # TODO
    # def get_name(self) -> str:
    #     names = self.mod_name_regex.search(self.content_clean)
    #     if not names:
    #         return ""
    #     return names.group(1)

    def get_translators(self) -> list[str]:
        # TODO
        return [
            value
            for language_block in self.language_block_regex.finditer(self.content_clean)
            for value in self.string_regex.findall(language_block.group(1))[:2]
            if ("(" in value or value.count(" ") >= 2)
        ]

    def get_languages(self) -> list[str]:
        # lang_name, lang_dir_name, lang_tra_files, x
        # TODO: tester les deux premiers est générateur d'erreur en cas de valeurs inhabituelles, voir `BG2 FixPack` ou `BG2 Improved GUI`
        return [
            value
            for language_block in self.language_block_regex.finditer(self.content_clean)
            for value in self.string_regex.findall(language_block.group(1))[:2]
        ]

    def get_games(self) -> list[str]:
        re_game_names = self.game_names_regex.findall(self.content_clean)
        return [re_game for re_games in re_game_names for re_game in re_games.split(" ")]

    def get_version(self) -> str:
        match = self.version_regex.search(self.content_clean)
        if match:
            return match.group(1)
        return ""
