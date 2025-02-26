import enum
import os

STATIC_ROOT = os.path.join("docs", "static")
IMG_ROOT = os.path.join(STATIC_ROOT, "img")

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
            "label": "Mod de qualité",
        },
        (1, "1"): {
            "icon": "⚠️",
            "label": "Mod pouvant poser des problèmes",
        },
        (0, "0"): {
            "icon": "🟥",
            "label": "Mod à éviter ou obsolète",
        },
    },
    "translation_state": {
        ("yes", "n/a"): {
            "icon": "✅",
            "label": "Mod traduit",
        },
        ("todo",): {
            "icon": "❎",
            "label": "Mod partiellement traduit",
        },
        ("no", "wip"): {
            "icon": "❌",
            "label": "Mod non traduit",
        },
    },
    "is_weidu": {
        (True,): {
            "icon": "😀",
            "label": "Mod Weidu",
        },
        (False,): {
            "icon": "😡",
            "label": "Mod override, non désinstalable",
        },
    },
}


# TODO: ordre à définir
class Games(enum.StrEnum):
    BG = "BG"
    BG2 = "BG2"
    TUTU = "Tutu"
    BGT = "BGT"
    BGEE = "BGEE"
    BG2EE = "BG2EE"
    SOD = "SoD"
    EET = "EET"
    IWD = "IWD"
    IWD2 = "IWD2"
    IWDEE = "IWDEE"
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


categorie_names = [
    "Patch non officiel",
    "Utilitaire",
    "Conversion",
    "Interface",
    "Cosmétique",
    "Portrait et son",
    "Quête",
    "PNJ recrutable",
    "PNJ One Day",
    "PNJ (autre)",
    "Forgeron et marchand",
    "Sort et objet",
    "Kit",
    "Gameplay",
    "Script et tactique",
    "Personnalisation du groupe",
]

FLAG_DIR = "flags"
SITE_DIR = "sites"

# TODO: réduire/convertir les static/img
domain_to_image = {
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

image_data = {
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
