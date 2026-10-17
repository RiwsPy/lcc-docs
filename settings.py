from enum import StrEnum
from pathlib import Path

from i18n import _g
from models.utils import slugify

DB_PATH: Path = Path.cwd() / "db"
FLAG_DIR: Path = Path("img") / "flags"
SITE_DIR: Path = Path("img") / "sites"


class TranslationStateEnum(StrEnum):
    TODO = "todo"
    NO = "no"
    WIP = "wip"
    YES = "yes"
    NA = "n/a"
    AUTO = "auto"


"""
    safe: les paramètres qui font baisser la note :
    - incompatibilités avec d'autres mods ou avec la dernière version du jeu (notamment pour les EE) ⇒ les mods override sont toujours concernés
    - autre version plus avancée existante (présence dans un mod plus conséquent, plus maintenu ou avec une meilleure compatibilité)
    - installation difficile
    - mod en version bêta ou wip
"""
attrs_icon_data: dict[str, dict[tuple, dict[str, str]]] = {
    "safe": {
        (2, "2"): {
            "icon": "🟢",
            "label": _g("Mod de qualité"),
        },
        (1, "1"): {
            "icon": "⚠️",
            "label": _g("Mod pouvant poser des problèmes"),
        },
        (0, "0"): {
            "icon": "🟥",
            "label": _g("Mod à éviter ou obsolète"),
        },
    },
    "translation_state_auto": {
        (TranslationStateEnum.YES, TranslationStateEnum.NA): {
            "icon": "✅",
            "label": _g("Mod traduit"),
        },
        (TranslationStateEnum.TODO,): {
            "icon": "❎",
            "label": _g("Mod partiellement traduit"),
        },
        (TranslationStateEnum.NO, TranslationStateEnum.WIP): {
            "icon": "❌",
            "label": _g("Mod non traduit"),
        },
    },
    "is_weidu": {
        (True,): {
            "icon": "😀",
            "label": _g("Mod Weidu"),
        },
        (False,): {
            "icon": "😡",
            "label": _g("Mod override, non désinstallable"),
        },
    },
}


class GameEnum(StrEnum):
    BG = "BG"
    TUTU = "Tutu"
    BG2 = "BG2"
    BGT = "BGT"
    BGEE = "BGEE"
    SOD = "SoD"
    BG2EE = "BG2EE"
    EET = "EET"
    IWD = "IWD"
    IWDEE = "IWDEE"
    IWD2 = "IWD2"
    PST = "PST"
    PSTEE = "PSTEE"

    @classmethod
    def pst(cls) -> set:
        return {cls.PST, cls.PSTEE}

    @classmethod
    def iwd(cls) -> set:
        return {cls.IWD, cls.IWD2, cls.IWDEE}

    @classmethod
    def bg2(cls) -> set:
        return {cls.BG2, cls.BGT, cls.BG2EE, cls.EET}

    @classmethod
    def bg1(cls) -> set:
        return {cls.BG, cls.TUTU, cls.BGT, cls.BGEE, cls.SOD, cls.EET}

    @classmethod
    def BG_EE(cls) -> set:
        return {cls.BGEE, cls.BG2EE, cls.EET, cls.SOD}

    @classmethod
    def IWD_EE(cls) -> set:
        return {cls.IWDEE}

    @classmethod
    def EE(cls) -> set:
        return cls.BG_EE() | cls.IWD_EE() | {cls.PSTEE}


class CategoryEnum(StrEnum):
    FIX = _g("Patch non officiel")
    TOOL = _g("Utilitaire")
    CONVERSION = _g("Conversion")
    INTERFACE = _g("Interface")
    COSMETIC = _g("Cosmétique")
    PORTRAIT_SOUND = _g("Portrait et son")
    QUEST = _g("Quête")
    NPC = _g("PNJ recrutable")
    NPC_1DAY = _g("PNJ One Day")
    NPC_OTHER = _g("PNJ (autre)")
    BLACKSMITH_MERCHANT = _g("Forgeron et marchand")
    SPELL_ITEM = _g("Sort et objet")
    KIT = _g("Kit")
    TWEAK = _g("Gameplay")
    SCRIPT = _g("Script et tactique")
    PARTY_PERSONNALISATION = _g("Personnalisation du groupe")
    GEMRB = _g("GemRB")

    @property
    def id(self) -> str:
        return slugify(self.name)

    @classmethod
    def values(cls) -> list[str]:
        return [cat.value for cat in cls]


class DomainImageEnum(StrEnum):
    ARTISAN = "artisans-32.avif"
    BALDURS_GATE = "baldurs-gate-32.png"
    BEAMDOG = "beamdog.png"
    BGFORGE = "bgforge.svg"
    BWL = "bwl.gif"
    CC = "logocc.png"
    GH = "github-32.png"
    GIBBER = "g3icon-32.avif"
    HAVREDEST = "luren.avif"
    MEDIAFIRE = "mediafire.png"
    NEXUS = "nexus-32.png"
    PPG = "ppg-32.jpg"
    REDDIT = "reddit_76.png"
    SENTRIZEAL = "sentrizeal.ico"
    SHS = "shs_reskit-32.avif"
    SORCERER = "sorcerer-32.avif"
    SF = "sf.png"
    TEAMBG = "teambg.png"
    TROW = "trow-32.png"
    WEASEL = "weasel-32.png"
    WEIDU = "weidu.ico"
    COUNTRY_FLAG = "-flag-32.png"


image_data: dict[DomainImageEnum | str, dict[str, str | int]] = {
    DomainImageEnum.ARTISAN: {"title": "The Artisan Corner", "width": 32, "height": 32},
    DomainImageEnum.BALDURS_GATE: {"title": "Baldur's Gate", "width": 32, "height": 32},
    DomainImageEnum.BEAMDOG: {"title": "Beamdog", "width": 32, "height": 32},
    DomainImageEnum.BGFORGE: {"title": "BG Forge", "width": 32, "height": 32},
    DomainImageEnum.BWL: {"title": "The Black Wyrm's Lair", "width": 32, "height": 29},
    DomainImageEnum.CC: {"title": "La Courrone de Cuivre", "width": 32, "height": 32},
    DomainImageEnum.GIBBER: {"title": "Gibberlings3", "width": 32, "height": 32},
    DomainImageEnum.GH: {"title": "GitHub", "width": 32, "height": 32},
    # DomainImageEnum.HAVREDEST: {"title": "Retour à Havredest", "width": 78},
    DomainImageEnum.MEDIAFIRE: {"title": "Mediafire", "width": 32, "height": 32},
    DomainImageEnum.NEXUS: {"title": "Nexus Mods", "width": 32, "height": 32},
    DomainImageEnum.PPG: {"title": "Pocket Plane Group", "width": 32, "height": 32},
    DomainImageEnum.REDDIT: {"title": "Reddit", "width": 32, "height": 32},
    DomainImageEnum.SENTRIZEAL: {"title": "Sentrizeal", "width": 16, "height": 16},
    DomainImageEnum.SHS: {"title": "Spellhold Studios", "width": 32, "height": 32},
    DomainImageEnum.SORCERER: {"title": "Sorcerer's Place", "width": 32, "height": 32},
    DomainImageEnum.SF: {"title": "SourceForge", "width": 32, "height": 32},
    DomainImageEnum.TEAMBG: {"title": "TeamBG", "width": 32, "height": 13},
    DomainImageEnum.TROW: {"title": "The Ring of Wonder", "width": 32, "height": 32},
    DomainImageEnum.WEASEL: {"title": "Weasel Mods", "width": 32, "height": 32},
    DomainImageEnum.WEIDU: {"title": "WeiDU", "width": 16, "height": 16},
    DomainImageEnum.COUNTRY_FLAG: {"title": "Mod %s", "width": 32, "height": 21},
}


def resize_image_from_width(width: int) -> None:
    """
    Recalcule les dimensions des images en conservant le ratio initial en se basant sur le width
    """
    for key, value in image_data.items():
        current_width = int(value["width"])
        if current_width == width:
            continue

        current_height = int(value["height"])
        diff_base1 = 1 - (current_width - width) / current_width
        image_data[key]["width"] = width
        image_data[key]["height"] = int(current_height * diff_base1)


language_flags: dict[str, str] = {
    "br": "🇧🇷",
    "cn": "🇨🇳",
    "cz": "🇨🇿",
    "de": "🇩🇪",
    "en": "🇬🇧",
    "es": "🇪🇸",
    "fo": "🇫🇴",
    "fr": "🇨🇵",
    "hr": "🇭🇷",
    "hu": "🇭🇺",
    "it": "🇮🇹",
    "jp": "🇯🇵",
    "kr": "🇰🇷",
    "nl": "🇳🇱",
    "no": "🇳🇴",
    "pl": "🇵🇱",
    "pt": "🇵🇹",
    "ru": "🇷🇺",
    "se": "🇸🇪",
    "tr": "🇹🇷",
    "ua": "🇺🇦",
}
