import enum
import os
from pathlib import Path

from i18n import _g
from models.utils import slugify

STATIC_ROOT: Path = Path(os.path.join("docs", "static"))
IMG_ROOT: Path = STATIC_ROOT / "img"
DB_PATH: Path = Path.cwd() / "db"


class TranslationStateEnum(enum.StrEnum):
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


class GameEnum(enum.StrEnum):
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
    def pst(cls) -> list:
        return [cls.PST, cls.PSTEE]

    @classmethod
    def iwd(cls) -> list:
        return [cls.IWD, cls.IWD2, cls.IWDEE]

    @classmethod
    def bg2(cls) -> list:
        return [cls.BG2, cls.BGT, cls.BG2EE, cls.EET]

    @classmethod
    def bg1(cls) -> list:
        return [cls.BG, cls.TUTU, cls.BGT, cls.BGEE, cls.SOD, cls.EET]

    @classmethod
    def BG_EE(cls) -> tuple:
        return (cls.BGEE, cls.BG2EE, cls.EET, cls.SOD)

    @classmethod
    def IWD_EE(cls) -> tuple:
        return (cls.IWDEE,)

    @classmethod
    def EE(cls) -> tuple:
        return cls.BG_EE() + cls.IWD_EE() + (cls.PSTEE,)


class CategoryEnum(enum.StrEnum):
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

    @property
    def id(self) -> str:
        return slugify(self.name)

    @classmethod
    def values(cls) -> list[str]:
        return [cat.value for cat in cls]


FLAG_DIR = "flags"
SITE_DIR = "sites"

# TODO: réduire/convertir les static/img
domain_to_image: dict[str, str] = {
    "artisans-corner.com": "artisans-32.avif",
    "baldursgateworld.fr": "logocc.png",
    "anomaly-studios.fr": "logocc.png",
    # "baldursgatemods.com": "teambg.png",
    "downloads.chosenofmystra.net": "teambg.png",
    "beamdog.com": "beamdog.png",
    "blackwyrmlair.net": "bwl.gif",
    "gibberlings3.net": "g3icon-32.avif",
    "github.com": "github-32.png",
    "github.io": "github-32.png",
    # "havredest.eklablog.fr": "luren.avif",
    "pocketplane.net": "ppg-32.jpg",
    "mediafire.com": "mediafire.png",
    "nexusmods.com": "nexus-32.png",
    "reddit.com": "reddit_76.png",
    "sasha-altherin.webs.com": "ab-logo-32.jpg",
    "sentrizeal.com": "sentrizeal.ico",
    "shsforums.net": "shs_reskit-32.avif",
    "spellholdstudios.net": "shs_reskit-32.avif",
    "bgforge.net": "bgforge.svg",
    "sorcerers.net": "sorcerer-32.avif",
    "sourceforge.net": "sf.png",
    "weaselmods.net": "weasel-32.png",
    "weidu.org": "weidu.ico",
    # les cas particuliers récupérés de la version de freddy
    "clandlan.net": "sp-flag-32.png",
    "trow.cc": "cn-flag-32.png",
}

image_data: dict[str, dict[str, str | int]] = {
    "artisans-32.avif": {"title": "The Artisan Corner", "width": 32, "height": 32},
    "logocc.png": {"title": "La Courrone de Cuivre", "width": 32, "height": 32},
    "teambg.png": {"title": "TeamBG", "width": 32, "height": 13},
    "beamdog.png": {"title": "Beamdog", "width": 32, "height": 32},
    "bwl.gif": {"title": "The Black Wyrm's Lair", "width": 32, "height": 29},
    "g3icon-32.avif": {"title": "Gibberlings3", "width": 32, "height": 32},
    "github-32.png": {"title": "GitHub", "width": 32, "height": 32},
    # TODO: raccourcir cet icône
    # "luren.avif": {"title": "Retour à Havredest", "width": 78},
    "ppg-32.jpg": {"title": "Pocket Plane Group", "width": 32, "height": 32},
    "mediafire.png": {"title": "Mediafire", "width": 32, "height": 32},
    "nexus-32.png": {"title": "Nexus Mods", "width": 32, "height": 32},
    "reddit_76.png": {"title": "Reddit", "width": 32, "height": 32},
    "ab-logo-32.jpg": {"title": "AB aka Sasha al'Therin", "width": 32, "height": 24},
    "sentrizeal.ico": {"title": "Sentrizeal", "width": 16, "height": 16},
    "shs_reskit-32.avif": {"title": "Spellhold Studios", "width": 32, "height": 32},
    "sorcerer-32.avif": {"title": "Sorcerer's Place", "width": 32, "height": 32},
    "sf.png": {"title": "SourceForge", "width": 32, "height": 32},
    "weasel-32.png": {"title": "Weasel Mods", "width": 32, "height": 32},
    "weidu.ico": {"title": "WeiDU", "width": 16, "height": 16},
    "bgforge.svg": {"title": "BG Forge", "width": 32, "height": 32},
    "-flag-32.png": {"title": "Mod %s", "width": 32, "height": 21},
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
