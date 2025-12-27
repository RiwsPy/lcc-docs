# Lignes de bonne conduite du contributeur (WIP)


## Le JSON c'est quoi ?

Documentation sur le JSON : https://developer.mozilla.org/fr/docs/Learn/JavaScript/Objects/JSON

Outil en ligne pour valider le format de votre json : https://jsonformatter.curiousconcept.com \
Pour les utilisateurs de Notepad++ : https://github.com/molsonkiko/JsonToolsNppPlugin


## Les fichiers de traduction

Chaque language possède son propre fichier de traduction :
- `mods.json` est la version référence
- `mods_xx.json` est la version utilisée par la langue de code `xx`

### Le contenu source

Chaque champ non rempli dans `mods_xx.json` sera remplacé par le contenu du fichier `mods_en.json`.\
Après cette étape, si certains champs demeurent non renseignés, ils seront remplacés par le contenu du fichier `mods.json`.\
Ce contenu est appelé contenu `source`.

### Les champs meta

Les fichiers de traduction possèdent des champs supplémentaires suffixés par `_meta`.\
Comme `description_meta`. Qui est associé au champ `description`.\
Il contient des informations supplémentaires utiles à la traduction pour le champ associé.\
Son contenu est généré **automatiquement** et sera donc écrasé si nécessaire.

#### Statuts

Le champ `status` des champs `_meta` peut contenir trois valeurs :
- `"done"` : la traduction a été relue ou aucune traduction n'est nécessaire
- `"needs_review"` : la traduction a été réalisée mais nécessite une relecture
- `"todo"` : la traduction n'a pas été réalisée

#### Source

Le champ `source` des champs `_meta` contient la dernière version connue de la source.\
Si le contenu de la source venait à être modifié, alors une différence entre les deux champs sera détectée.\
Une traduction réalisée de statut `"done"`, et dont la source change passera au statut `"needs_review"`.\
Une traduction vide de statut `"done"`, et dont la source change passera au statut `"todo"`.


### urls_extra

Si ce champ est renseigné, son contenu est ajouté au champ `urls` du mod pour la langue concernée.\
Cela permet d'ajouter des liens non officiels, comme une traduction pas encore acceptée par l'auteur par exemple.\
Cela, sans surcharger les urls de toutes les langues.


### notes_extra

Dans la même veine que `urls_extra`, une note spécifique à la langue est ajoutée aux notes du mod.


## Le fichier .ini

Parfois, les mods possèdent un fichier `.ini`. Plus d'informations [ici](https://www.gibberlings3.net/forums/topic/32516-tutorial-what-is-label-why-you-should-create-it-and-how-to-do-it-properly/).\
Les données contenues dans ce fichier sont considérées comme les plus fiables, on y trouve entre autre :
- `Name` : le nom du mod
- `Author` : le nom de l'auteur
- `Description` : la description (succinte) du mod
- `HomePage` : url de présentation du mod

En tant que contributeur, il est conseillé de l'utiliser autant que possible.\
En tant que moddeur, il est encouragé de le remplir.


## name

Le nom du mod.\
Cette donnée n'est pas aussi simple qu'elle n'y paraît : le nom est variable selon la source.\
Souvent le nom du post diffère de celui du repo.\
En cas de fichier `.ini`, on prend celui qui est renseigné dedans.\
Sinon, on peut se baser sur le nom du sujet de présentation du mod ou du titre dans le readme du mod.\
On préviligiera les noms courts. En évitant les rallonges qui indiquent les compatibilités du mod (le champ `games` permet déjà de renseigner cette information).\
Deux mods ne peuvent avoir le même nom. Cependant, il peut exister deux versions d'un même mod pour deux jeux. Dans ce cas, on peut préciser le nom du jeu entre parenthèse pour les différencier.\
Exemple : `Dragonspear UI++` et `Dragonspear UI++ (IWDEE)`.


## description

La description du mod.\
C'est un "teaser", la description ne doit pas être complète mais donner envie au lecteur de cliquer sur le lien pour en savoir plus.\
Conseils :
- Les informations doivent être stables, on évite : 
    - les commentaires personnels : `cet auteur est génial`
    - les dates fixes : `ce mod existe depuis 3 ans`
    - toute information périssable : `ce mod activement maintenu`
- Si des informations sont à la fois à éviter et pertinentes, elles peuvent être renseignées dans le champ `notes`.
- Les balises html sont fonctionnelles dans la description, cela n'est pas cependant pas conseillé.


### Aides pour se simplifier la vie
- `|` : le pipe, il permet de revenir à la ligne (le saut de ligne n'étant pas autorisé dans le json)
- \`\` : le backtick (l'accent grave), il permet de mettre en `surbrillance un bout de phrase`
- `[[ ]]` : le lien interne, il n'est pas rare qu'un mod parle d'un autre mod, on rajoute un lien : [[id du mod]]
- `[]()` : le lien externe, comme avec les fichiers .md, `[description du lien](url)`

## notes

Les notes du mod écrites par les contributeurs pour compléter la description du mod.\
- On y met :
    - Des conseils sur l'installation
    - Les incompatibilités éventuelles
    - Les points d'attention variés
- On évite :
    - Les jugements de valeur : `le travail de cet auteur laisse à désirer`
- On remplacera :
    - `ce mod existe depuis 3 ans` → `ce mod existe depuis 2017`
    - `Attention le troisième composant n'est pas compatible avec YY` → `Attention le composant XX n'est pas compatible avec YY`


⚠️ Certaines notes sont automatiques.\
On trouvera le code dans `Mod.get_auto_notes` dans `models/mods.py`.\
En voici un résumé des notes automatiques qui ne sont donc **PAS** à ajouter :
- Noms des traducteurs
- `Ce mod n'est disponible qu'en {langue}.`
- Mods EE qui datent d'avant la version 2.0 : `⚠️ EE : La dernière mise à jour date de {year}. Ce mod pourrait ne pas fonctionner avec la dernière version du jeu.`
- Mod non WeiDU (tp2="non-weidu") : `⚠️ WeiDU : Ce mod écrase les fichiers et ne peut être désinstallé. Installez-le à vos risques et périls.`
- Mod archivé (status="archived") : `Ce mod a été archivé par son auteur/mainteneur qui ne semble pas vouloir lui donner suite.`
- Mod disparu (status="missing") : `Ce mod a disparu.`

Les `aides` du champ `description` sont fonctionnelles dans les notes.


## safe

Ce champ renseigne sur la qualité du mod en général. Les valeurs possibles vont de 0 à 2.
    
    2 : 🟢 Mod de qualité
    1 : ⚠️ Mod pouvant poser des problèmes
    0 : 🟥 Mod à éviter ou obsolète

À titre informatif, voici quelques règles utilisées :
* Ce qui met automatiquement la note à **0**
  * Le mod est intégré dans un autre mod plus à jour : `status="embed"`
  * Le mod est considéré comme obsolète : `status="obsolete"`
* Ce qui diminue la note de **1** point :
  * Le mod est compatible EE mais pas mis à jour depuis la version 2.0 (Avril 2016)
  * Le mod est compatible EE, de la catégorie `Interface` mais pas mis à jour depuis Avril 2021
  * Le mod n'est pas weidu : `tp2="non-weidu"`
  * Le mod est archivé (et donc plus maintenu) : `status="archived"`
* Ce qui **limite** la note à 1 point (c'est-à-dire qu'ils valent 0 ou 1)
  * Le mod est en cours de création : `status="wip"`
  * Le mod a disparu : `status="missing"`


Les effets sont cumulatifs.\
Un mod dont le lien a disparu et qui n'est pas WeiDU vaut 0.

## urls
Les urls permettent de renvoyer le lecteur vers un complément d'information mais aussi vers le mod.\
Idéalement, deux liens sont présents :
1. Le premier vers la description officielle du mod faite par l'auteur, souvent il s'agit d'une discussion de forum où l'on peut également trouver les retours des utilisateurs, des bugs éventuels… tout un tas d'informations utiles.
2. Le second pointe vers le mod a proprement parlé, on privilégiera ici les liens vers des repo git


### Fiabilité de la donnée

Si le mod contient un fichier .ini, on préviligie la `HomePage` comme lien n°1.

### Sécurité

La totalité des liens sont des liens **externes**, cela implique que l'on ne sait **pas** ce qu'il y a derrière.\
Ainsi, la facilité ne doit **PAS** primer sur la sécurité.

#### https

Dans la mesure du possible, le **https** doit être proposé.\
Si un lien est en **http**, essayez d'accéder à la page en **https**. Si cela fonctionne, renseignez le lien https.\
Certains sites n'acceptent pas ce protocole, dans ce cas c'est toléré.


#### Pas de téléchargement direct

Comme on ne peut pas assurer du contenu de l'objet téléchargé, le mieux c'est encore de ne rien télécharger. On redirige le lecteur vers la page qui permet le téléchargement, mais la charge lui revient de cliquer (ou pas) sur le lien au sein de la page.


#### Viser un message spécifique dans une discussion

Parfois, un mod se situe au beau milieu d'une discussion. Dans la mesure du possible, ciblez le message en question dans l'url.

#### Viser la page d'accueil plutôt que le blob/plop/release/

Cela concerne notamment les liens github.\
La description du mod ne sera jamais suffisante et ne sera peut-être pas à jour. Il faut autant que possible, rediriger vers la page d'accueil avec le README, le code et la visualisation sur les releases etc… Cela donne un contexte bien plus pertinent que la page avec juste un lien de téléchargement.

Cas particulier pour le forum **beamdog** : on retirera la fin de l'url qui n'est pas maintenable et complique les comparaisons, par exemple :\
https://forums.beamdog.com/discussion/63741/ \
plutôt que\
https://forums.beamdog.com/discussion/63741/plip-plop-plup/




## categories

Les catégories d'appartenance du mod.\
Plusieurs catégories peuvent être choisies.


`PNJ One Day` est une catégorie qui répond à des spécifités particulières. Les One Day n'ont plus la côte. Le choix a été fait de lever ces restrictions. Dans cette catégorie, on trouvera les "vrais" One Day mais aussi les personnages avec peu de contenu, notamment en terme de banters.



Certaines catégories s'entrecroisent, on évitera de toutes les renseigner.\
Quelques exemples :
- Un mod d'`Interface` est souvent également `Cosmétique`. `Cosmétique` étant plus générique, on ne précisera que `Interface`.
- Un mod peut ajouter un `PNJ recrutable` et rendre le `Kit` du personnage disponible pour le PJ. On garde `PNJ recutable` car c'est l'objectif du mod. De plus, on ne veut pas de description d'un personnage dans la catégorie `Kit`.
- Un pack de `Sort et objet` peut être vendu chez des `Forgeron et marchand`. Pas de solution miracle. La description présente-t-elle les objets ou le marchand ? Si la réponse n'est pas évidente, il n'est pas interdit de mettre les deux catégories.


## update_date
Cette date au format `YYYY-MM` contient la date de la dernière mise à jour du mod.\
La date doit être comprise entre le 1er Janvier 1999 et la date d'aujourd'hui.
