# Liste des mods de l'Infinity Engine

Version maintenue de la [liste des mods](https://lacouronnedecuivre.github.io/lcc-docs/) BG de FreddyGwendo \
Reprise de la liste des mods de JohnBob

## Infos

Le fichier `db/mods.json` contient les informations nécessaires à la génération de la page. Pour ajouter, corriger, supprimer un mod c'est lui et seulement lui qu'il faut éditer.

## Installation

### Le minimum vital

[Python](https://www.python.org/downloads/)3.11+\
[uv](https://docs.astral.sh/uv/getting-started/installation/), le gestionnaire de paquet

### Créez l'environnement virtuel
```
    cd lcc-docs/
    uv sync
```

### Testez l'intégrité du fichier mods.json
```
    uv run main.py scripts/check_mods_json.py
```

### Créez la page statique du site
```
    uv run main.py scripts/update_index.py
```
Cela génère le fichier `index.html` dans `docs/` ainsi que les pages traduites (chacune présente dans son dossier associé, ex : `db/fr/index.html` pour la version française).

## Améliorations par rapport à la v1

Cette version propose plusieurs améliorations techniques notables :
* Bien meilleure maintenabilité
* Merge des 8 jeux de données en un seul
* Merge des 8 templates : exit le fix typo à appliquer 8 fois
* Pas de connaissance nécessaire en html/css pour faire des modifications
* Suppression de la plage d'identifiant unique pour les mods
* Une seule feuille de style (avec utilisation de variable…)
* Retrait des styles inlines css
* Script de génération de la page `index.html`
* Les mods peuvent être dans plusieurs catégories
* Du responsive (un tableau ça a des limites)
* Une facilité de lecture accrue (taille de police, des images etc)
* Modification aisée de la structure de la donnée (et des mods qui vont avec)
* Filtre par nom
* Filtre par qualité de mod
* CI qui check automatiquement la conformité du contenu de `mods.json`
* Traduction possible de l'interface et du contenu
* …

## Limites
* Modifier un Json est moins sexy que de passer par un formulaire fait pour ça
* Le Json est moins sexy d'une base de données relationnelle pour gérer les relations
* …


## TODO
* Remplacer le Json par du Yaml paraît être une bonne idée mais la multiplication des `'\"\'` en tout genre ne m'y a pas encouragé (peut-être une config permet de contourner le problème ou une autre solution est envisageable ?)
* Formulaire d'ajout d'un mod qui renvoit son équivalent en Json (plus qu'à l'ajouter à la db)
* Rédaction de GuideLine pour les contributeurs (wip)


## Doc

Comme tout se fait dans le fichier `db/mods.json`, il est important de savoir ce qui est possible de faire ou non.

### Le JSON c'est quoi ?
Documentation sur le JSON : https://developer.mozilla.org/fr/docs/Learn/JavaScript/Objects/JSON\
Outil en ligne pour valider le format de votre json : https://jsonformatter.curiousconcept.com


### Informations par défaut des mods :
```json
    {
        "id": 0,
        "name": "",
        "description": "",
        "urls": [],
        "categories": [],
        "games": [],
        "authors": [],
        "team": [],
        "notes": [],
        "translation_state": "no",
        "safe": 2,
        "languages": [],
        "status": "active",
        "last_update": "",
        "tp2": ""
    }
```


### Détails
`id`: identifiant unique du mod\
`name` : nom du mod\
`description` : description du mod\
`urls` : liste de lien, généralement lien de téléchargement ou/et lien du forum le présentant\
`categories`: liste des catégories dans lesquelles le mod est placé. Valeurs possibles :
 - Patch non officiel
 - Utilitaire
 - Conversion
 - Interface
 - Cosmétique
 - Portrait et son
 - Quête
 - PNJ recrutable
 - PNJ One Day
 - PNJ (autre)
 - Forgeron et marchand
 - Sort et objet
 - Kit
 - Gameplay
 - Script et tactique
 - Personnalisation du groupe

`games` : liste des jeux sur lesquels le mod est fonctionnel. Valeurs possibles :
 - BG
 - BG2
 - BGT
 - Tutu
 - BGEE
 - SoD
 - BG2EE
 - EET
 - IWD
 - IWD2
 - IWDEE
 - PST
 - PSTEE

`authors`: liste des personnes ayant participé à la création/maintenance du mod\
`team` : liste des personnes ayant participé à la traduction du mod\
`notes` : liste de messages indiquant des points d'attention\
`translation_state` : le mod est traduit ou pas, ou s'il ne nécessite pas de traduction. Valeurs possibles :
 - `"yes"` : ✅ Mod traduit
 - `"no"` : ❌ Mod non traduit
 - `"n/a"` : ✅ Mod ne nécessitant pas de traduction
 - `"todo"` : ❎ Mod partiellement traduit
 - `"wip"` : ❌ Mod en cours de traduction
 - `"auto"` : ? Si le Mod possède la langue courante dans `languages`, alors `yes` sinon `no`

`safe` : si le mod est considéré comme fiable (installable via weidu, maintenu, ne génère pas d'incompatibilités). Valeurs possibles :
 - `2` : 🟢 Mod de qualité
 - `1` : ⚠️ Mod pouvant poser des problèmes
 - `0` : 🟥 Mod à éviter ou obsolète

`languages` : langues dans lesquelles le mod existe, actuellement non affiché, format [ISO-3166-1](https://fr.wikipedia.org/wiki/ISO_3166-1)

`status` : la raison peut être indiquée dans les `notes`
 - `"active"` : mod actif
 - `"archived"` : mod est archivé et donc non maintenu
 - `"obsolete"` : incompatible avec les dernières versions des jeux originaux ou/et EE (exemple d'un mod fait sous EE 1.3 mais jamais upgrade depuis)
 - `"embed"` : intégré en tant que composant (et maintenu) dans un autre mod ou pack
 - `"missing"` : lien de téléchargement disparu
 - `"wip"` : le mod est phase de développement
 - `"hidden"` : le mod ne s'affiche pas dans la liste

`last_update` : date connue de la dernière mise à jour du mod, champ automatique, format `YYYY-MM`

`tp2` : nom du fichier tp2 du mod. Valeurs possibles :
 - `"nom du tp2"` : le vrai nom du tp2 (sans le setup-)
 - `"n/a"` : non concerné (notamment pour les utilitaires)
 - `"non-weidu"` : pas de fichier tp2 car non-WeiDU
