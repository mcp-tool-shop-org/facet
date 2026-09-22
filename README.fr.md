<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.md">English</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/facet/readme.png" alt="facet" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/facet/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/facet/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="docs/experiments/"><img src="https://img.shields.io/badge/record-spec%20%E2%86%92%20report%20%E2%86%92%20ruling-8a6f3f" alt="The record"></a>
  <a href="https://mcp-tool-shop-org.github.io/facet/"><img src="https://img.shields.io/badge/landing%20page-live-2ea043" alt="Landing page"></a>
</p>

<p align="center">
  <strong>A styled 2D concept goes in. A textured 3D asset comes out.</strong><br>
  Local-first — your own GPU, with a metered cloud step where it will not fit<br>
  No non-commercial licence anywhere in the chain
</p>

---

Le style est appliqué **sur l’élément**, dans l’espace de texture, et non pas peint pour chaque vue, puis assemblé par la suite. Fournissez à la séquence une représentation en argile aux formes exagérées, et elle renverra un maillage texturé dont la couleur provient d’une référence stylisée de *ce* maillage, chaque élément que la référence ne pouvait pas voir étant rempli par un pinceau de retouche masqué et une dilatation tenant compte de la surface.

Nommé d’après les deux aspects du problème : les polygones et la surface qu’ils doivent représenter.

## Installation

La séquence elle-même est un ensemble de scripts locaux que vous exécutez sur des chemins que vous tapez. Clonez le dépôt et lisez [comment démarrer](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Deux serveurs sont fournis dans un seul package** : l’index des enregistrements, afin qu’un assistant puisse interroger la trace des preuves au lieu de la lire, et **à partir de la version 0.4.0, le serveur de mesure**, de sorte que deux éléments mesurés à plusieurs mois d’intervalle passent par un seul chemin de code.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` est le serveur MCP stdio qui traite les enregistrements (six outils, dont la vérification à quatre points qui sert de surface de contrôle) et `facet-index` est l’index lui-même (`build` / `verify` / `q` / `claims`). Exécutez l’un ou l’autre à partir d’un répertoire de travail ; `--db` désigne un index différent.

### Le serveur de mesure : nouveauté dans la version 0.4.0

`facet-measure` répond à la **partie numérique** d’une comparaison et n’indique jamais si la sortie est correcte. Chaque charge utile contient la version du serveur, le hachage du fichier de l’instrument et un hachage de configuration, et `measure_report` **refuse** de comparer des éléments qui ne correspondent pas, ce qui est la propriété pour laquelle l’ensemble a été conçu.

Vérifié en exécutant une **commande** plutôt que `--help` : un maillage de contrôle renvoie 786 432 faces avec une enveloppe d’identité complète sur une machine qui ne contient pas de répertoire de travail.

**Ce que vous obtenez dépend d’une seule chose : votre version de Python :**

| votre Python | `[measure-full]` vous donne |
|---|---|
| **3.11 / 3.12** | **les huit outils** : `open3d` s’installe à partir de PyPI |
| **3.13** | quatre outils : `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 est la dernière *version* et publie des roues cp38–cp312 **sans sdist**, de sorte que sur 3.13, il n’y a rien sur PyPI à installer. L’élément supplémentaire le fournit en arrière-plan via `python_version < "3.13"`, de sorte que l’installation **réussie** et les quatre outils de géométrie renvoient **`4` REFUSÉ**, en indiquant ce dont ils ont besoin, plutôt que l’installation entière échoue.

**Pour obtenir les huit outils sur Python 3.13**, Open3D publie les roues cp313 actuelles sur son canal de développement continu. Une URL directe est acceptable dans une ligne de commande ; elle est simplement interdite dans les métadonnées des packages publiés :

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **Sur Windows et macOS, les roues de développement sont suffixées par `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` au moment de la rédaction), et le nom change lorsque `main` change. Listez les éléments sur [la version `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) et prenez la version actuelle. **Cette version est celle par rapport à laquelle les nombres de cette séquence, qui dépendent d’Open3D, ont été mesurés, et elle constitue une véritable limite de comparabilité : l’enveloppe d’identité enregistre le hachage de l’instrument, et non ses dépendances — [E31](docs/experiments/E31-ruling.md).**

*Jusqu’à la version 0.3.1, la roue contenait deux fichiers `.py` et aucun des instruments de mesure, de sorte qu’un serveur de mesure installé n’avait rien à exécuter. Personne ne l’a remarqué pendant quatre versions, car ce dépôt EST le répertoire de travail : l’outil fonctionnait là où il était construit et n’avait jamais été ailleurs.*

⚠ **`pip install facet-mcp` était défectueux dans toutes les versions publiées jusqu’à la version 0.3.0, et il est corrigé dans la version 0.3.1.** La roue installe `facet_index` en tant que module de premier niveau, de sorte que jusqu’à et y compris la version 0.3.0, elle résolvait l’emplacement de l’enregistrement par rapport à `<venv>/Lib`, qui ne contient ni corpus ni index, et `build`, `claims` et `q` sans `--db` échouaient tous. **Pour la version 0.3.0 ou une version antérieure, utilisez le binaire `npx` ci-dessus.**

À partir de la version 0.3.1, la racine est résolue en **vérifiant l’existence de l’enregistrement** plutôt qu’en supposant qu’il existe : exécutez l’une ou l’autre commande à partir d’un répertoire de travail et elle le trouvera ; exécutez-la depuis n’importe quel autre endroit et elle renverra **`4` REFUSÉ**, en indiquant les deux répertoires qu’elle a essayés et les deux marqueurs qu’elle a recherchés. `$FACET_INDEX_DB` est maintenant lu par les deux commandes, et il sélectionne quel *index*, et non quel *corpus*. Mesuré sur une roue construite à partir de `main` et installée dans un environnement virtuel propre — [E24](docs/experiments/E24-ruling.md).

*Ce bloc a été corrigé deux fois. Il indiquait d’abord `pipx install facet-mcp # ou le package Python directement `, until v0.3.0's read-back ran a **verb** instead of ` --help`.
Il indiquait ensuite que la roue « ne fonctionne que pour `q` et `claims` » — **`claims` ne fonctionnait pas non plus**, ce que E24 a découvert en l’exécutant. Les deux corrections se trouvent dans [known-defects.md](docs/known-defects.md) avec leurs mesures.*

## État actuel

**Quatre éléments acceptés, répartis dans quatre classes de sujets, sans coût.** Chacun a été validé par le directeur à son propre niveau de zoom — sur le fichier GLB ou sur des feuilles de taille réelle — et non par une métrique qui dépasse un seuil.

| sujet | classe | accepté | référence / pinceau / dilatation |
|---|---|---|---|
| **Character (W3)** | humanoïde | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | véhicule, gréement fin | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bête, membranes des ailes | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | accessoire, presque 2D, gris sur gris | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Les parts sont des texels valides, et **elles ne sont pas comparables entre les sujets** : un navire cache la majeure partie de lui depuis le niveau des yeux et un animal en cache la moitié. Évaluez chaque élément par rapport à son propre plafond de portée préenregistré, par rapport auquel ils atteignent **86 à 93 %** : la différence entre les lignes est la géométrie, et non une régression. [Nombres complets, avec leurs dénominateurs](docs/handbook/subjects.md).

**Un cinquième sujet est en cours de traitement, et il s'agit de la première référence construite en premier
(17 août 2026 → 19 août 2026).** A1, « l’archiviste », a été créé à partir d’une référence contenant sa propre recette intégrée, plutôt que d’un concept en argile, et chaque étape ultérieure a été validée en fonction de cela : le canon a été approuvé avec **16/16 surfaces** avant même qu’un maillage n’existe, un maillage a été approuvé par le directeur, un environnement a reproduit la référence **pixel par pixel, trois fois**, un ensemble de huit vues jumelles avec un manifeste sha256 a été accepté, et deux erreurs de contamination nommées ont été mesurées pour chaque mécanisme avant que quoi que ce soit ne soit modifié. La cuisson a été approuvée le [19 août 2026](docs/experiments/E70-baked-look-report.md) — **en fonction de l’identité et de l’ensemble des vêtements, et c’est là toute l’étendue de cette approbation.**

**Ensuite, le pinceau s’est ouvert et il ne dessine que dans les trous.** La première passe a été effectuée avec un angle de lacet de 90 degrés le 19 août 2026 : l’invariance ANDON a affiché **0,014 lv avec la plus grande composante chaude de 0 px** en dehors de la figure, sur les 472 318 px testés, et `commit` a dessiné **3 585 texels**, en remplissant les trous **2 044 423 → 2 040 838**, l’atlas source ayant été revérifié et étant identique, octet par octet. Au niveau du zoom du directeur, le triangle pâle au niveau du col du gilet s’est transformé en prune et la couture apparaît comme un seul vêtement. Il n’a pas inventé un visage, tourné la tête ou peint un deuxième gilet.

**Le résultat méthodologique est plus important que l’actif.** Tout au long de cette période, la force de ControlNet n’a jamais été modifiée : chaque correction a **supprimé une cause** plutôt que d’appliquer une force. Deux des erreurs étaient des défauts de spécification propres au conseiller, détectés par les postes d’exécution et par un canal d’examen externe avant qu’un crédit ne soit dépensé, et les deux sont nommés dans le registre avec la mesure qui les a invalidées.

**Il s’agit d’un pipeline, et non d’un générateur à un seul caractère.** Contredisez la spécification sur huit éléments nommés et l’invite l’emporte **8 fois sur 8** — la valeur médiane ΔE est de 46,3 contre 6,2 sur cinq contrôles maintenus — tandis que la figure reste la même. La structure est maintenue par le maillage et le contrôle ; les attributs nommés sont liés à l’invite.

**La question du projecteur a été close le 16 août 2026** ([E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
Les huit plaques **sont composées** : reconstruites à partir de l’ensemble par vue, en utilisant les poids de bordure × de face × de visibilité, le rendu de l’atlas a franchi pour la première fois la barre d’acceptation du directeur sur cet itinéraire — deux fois, sur deux arcs — à côté d’un atlas publié dont l’itinéraire avait pour effet de détruire la peinture, et les plaques sont d’accord. La chaîne qui a permis cela se trouve dans `tools/`
(`emit_view_aovs`, `s3_composite`, `flow_estimate`, `s3_run`, `s3_sheet`,
`atlas_from_aovs`, `twin_mesh_warp`), et a été largement construite grâce à un canal d’examen externe dont les revendications de calibration nominatives ont été maintenues **vingt fois sur vingt**, chacune étant vérifiée ici en l’exécutant avant que quoi que ce soit ne fasse confiance à la construction.

**Le canon est une donnée, et il contrôle la dépense (17 août 2026).** La spécification d’identité a nommé dix-sept éléments ; le flux de travail qui a généré les jumeaux a nommé seize éléments ; la valeur par défaut du profil, une nouvelle exécution, a nommé six éléments. Rien ne les reliait, de sorte que quatre arcs ont corrigé la composition en aval de la peinture qui était incorrecte à la source. Le canon est maintenant une base de données indexée sur la **surface** — une liste d’éléments ne peut pas vous montrer ce qui manque, et un occupant nullable transforme un trou en une ligne — et `canon_gate` s’exécute **à l’intérieur** des outils qui créent une génération, avant que le répertoire de sortie n’existe. Une génération dont l’invite ne couvre pas le canon approuvé est refusée et rien n’est écrit.

**Il s’agit d’un routeur, et il est configuré pour être sécurisé.** Il résout un sujet dans son fichier canon, couvre une invite dans les **deux** sens et contient une portée. **Un outil qui crée une dépense et qui ne reçoit pas de canon ne procède pas en douceur — il refuse.** La solution pour un sujet qui n’en a réellement pas est basée sur un recensement et ne peut pas être portée par un sujet qui en a : `--no-canon --subject GALLEON` procède et s’annonce ; `--no-canon --subject W3` est
**refusé**, car W3 a des surfaces. Cela ferme la case à cocher par construction plutôt que par convention, et cela est important car la forme précédente — `if args.canon:` — a permis au pilote PowerShell publié de passer la barrière en silence.

**La deuxième direction est celle qui détecte un défaut réel.** Vérifier que l’invite *contient* le canon permet de trouver une invite peu précise. Vérifier que tout dans l’invite *est* du canon permet de trouver une phrase qui nomme quelque chose que le personnage n’a pas — et il y en avait une dans la valeur par défaut en direct : **`gold necklace`**, que ce dépôt avait déjà mesurée comme nommant incorrectement la médaille en or de la ceinture, *"et l’élément survit par accident."* Une invite qui couvre cette phrase et qui y est ajoutée renvoie maintenant `missing: 0` et refuse de toute façon, en nommant la clause.

```
canon_gate 1.0.0  census  (occupancy is not ratification)
subject      named   occupancy   ratified   prof_hit surfaces
W3              19       24/24      24/24       5/19 canon/w3.surfaces.json
GALLEON         13           -          -      11/13 NONE
DRAGON          11           -          -      10/11 NONE
LONGSWORD        5         5/5        5/5        4/5 canon/longsword.surfaces.json
E10-LAYER        1           -          -          - NONE
LOGO             0           -          -          - NONE
A1              10       16/16      16/16      10/10 canon/a1.surfaces.json
```

`prof_hit 5/19` est un **échantillon délibérément laissé cassé** : il s’agit de la valeur par défaut en direct qu’une exécution utiliserait réellement, de sorte que la première `--profile character.json` est censée s’arrêter. La réparation de la chaîne supprimerait la preuve.

**Et il existe une feuille de calcul, car les quatre sujets qui n’ont pas de canon ne vont pas se déplacer tout seuls.** Elle émet chaque surface qu’un sujet *implique* — donc un trou est une ligne avant que quiconque ne l’ait nommé — transforme un fichier IDENTITY.md en un inventaire, transporte les joints par paires pour confirmer et réserve des emplacements de portée par vue. Il est **structurellement incapable de remplir un occupant**, et c’est la propriété pour laquelle il est testé : une phrase toxique qui arrive avec une surface déjà attribuée n’est pas écrite. La génération d’un canon est un humain qui suit une référence ; la feuille de calcul ne fait que rendre cette démarche moins coûteuse et plus complète.

**La limite de la scène est définie, plutôt que laissée à la découverte.** Elle vérifie les phrases du canon validé dans les deux sens, dans une certaine mesure. Elle ne vérifie pas les paraphrases ou les synonymes — une correspondance sémantique placerait un modèle à l’intérieur d’une scène, ce que ce dépôt refuse en principe — ni les éléments par vue tant qu’une portée de vue n’est pas déclarée, ni si un matériau nommé se trouve sur la surface *correcte*. Des emplacements de portée existent et leurs listes de surfaces sont vides : les remplir est une tâche humaine, comme remplir les emplacements. Quatre sujets ont un fichier IDENTITY.md et aucun fichier JSON de surfaces — ce qui a été laissé inachevé plutôt que généré sans parcourir la référence.

**Le nombre d’éléments qu’une requête peut contenir est mesuré, et il n’atteint pas le canon.** La documentation évalue chaque élément de requête ajouté à un coût, en fonction de la présence ou non des éléments, sur une plage bien inférieure à la nôtre, de sorte qu’une requête Opus a demandé si les éléments déjà payés pouvaient suffire. **Ce n’est pas le cas, et la raison est structurelle** : aucun élément du corpus ne conserve sa phrase constante alors que le nombre qui l’entoure varie *et* peut être absent. Ce qu’ils fournissent, c’est une limite unilatérale, à partir de cinq requêtes pour une caméra avec un contrôle, un masque et une graine identiques : sur une échelle d’éléments de **10 → 17**, le nombre d’éléments supprimés est **nul** par rapport à ce qui était présent à 10, tandis qu’un changement d’identité à *zéro* a modifié l’intervalle d’étalonnage complet. **Le canon de W3 exige 19, et le corpus n’y parvient jamais** ([E55](docs/experiments/E55-density-vs-identity-report.md)). Le studio affiche les trois nombres qui sont combinés : 24 surfaces de requête, 25 vérifications requises, 19 éléments uniques — de sorte qu’un nombre de couverture n’est jamais mis en relation avec une mesure du nombre d’éléments.

**Un sixième sujet a été utilisé pour répondre à une question différente et a renvoyé un résultat négatif (2026-09-22).** Un gardien de port pour `ai-rpg-stage` a été reconstitué pour tester ce qui se passe *après* l’application de la peinture — pose et accessoires — et il se reconstruit correctement, puis **échoue à l’auto-rigging**. Quatre causes potentielles ont été éliminées par mesure plutôt que par argument : entrée non texturée, nombre de composants, topologie du maillage et la pose. **Le discriminateur n’est pas identifié**, et [`canon/BASE-FIGURE.md`](canon/BASE-FIGURE.md) contient le tableau de ce qui a été essayé tout en refusant de nommer une cause — parce que la seule cause que ce dépôt a nommée, la séparation du bras et du torse, a été invalidée dans la même heure par une pose A correcte qui a échoué avec une *plus grande* séparation qu’une pose qui a réussi.

**Ce qui en ressort, c’est un contrat de taille et deux scènes.** Chaque reconstruction que ce processus effectue est ramenée à une valeur normalisée de **1,002 sur son axe le plus long** — mesurée sur quatre éléments non liés, avec trois décimales — de sorte qu’un maillage d’accessoire n’a aucune échelle réelle et qu’un bouclier de radiateur chargé tel quel est une porte de 1,8 m. La taille réelle d’un accessoire est désormais déclarée une seule fois en millimètres, stockée à côté du fichier et vérifiée plutôt que supposée (`tools/prop_scale.py`, unité de scène **1,0 = 1,8 m**). Un accessoire qui *touche* une figure à un seul sommet n’est pas conservé, de sorte que la scène de contact signale une distance minimale **et une zone de contact** (`tools/verify/prop_contact.py`) — l’élément qui a déclenché cela a touché à 0,00072 sur 97 points sur 624 510 et n’était manifestement pas en prise. Et le résultat d’un auto-rig est désormais lu plutôt que supposé : `tools/verify/rig_report.py` nomme les articulations, compare le maillage en tant qu’*ensemble* plutôt qu’en tant que nombre, et indique si le skinning est présent.

**Une main à six doigts a atteint une feuille acceptée après avoir traversé quatre scènes qui ne pouvaient pas voir les mains.** Le directeur l’a trouvé en regardant. La clause 7 du canon — cinq doigts par main — existe parce que la clause 2 l’a causée, et les mains sont désormais un élément d’acceptation lors de son zoom, plutôt qu’une chose sur laquelle les métriques étaient silencieuses.

## Le processus

```
  styled 2D concept ╌╌► clay prep ╌╌╮   ← CANDIDATE hop, walked once. Not a route
                                    ╎     stage. Everything below it is the route.
                                    ▼
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

Étape par étape, avec la justification de chaque étape : **[le manuel](docs/handbook/index.md)**.

**Le saut en pointillés est nouveau et est délibérément non solide.** La première boîte du processus a toujours affiché *concept en argile*, et jusqu’à présent, rien ici n’en a créé : chaque argile est arrivée à la main et a été hachée en cours de route. Un outil concept→argile existe désormais et sa première paire a été testée à pleine échelle : la pose, les bracelets de poignet, le médaillon de ceinture et l’ourlet déchiré ont été utilisés ; la masse de la crinière n’a pas été utilisée ; la fuite de couleur a été mesurée sur toute l’image à **C\* p99,9 = 13,15** avec un arrière-plan achromatique uniforme. **Ce que cette paire ne peut pas montrer, c’est si le maillage revient en mieux**, ce qui est la seule question qui le favorise, de sorte qu’il reste un candidat avec ses preuves enregistrées : **[préparation du concept](docs/concept-prep.md)**.

## Ce qui le fait fonctionner

Six conclusions, chacune d’entre elles nécessitant une expérience et chacune d’entre elles s’appliquant au-delà du sujet qui l’a produite. [La version longue, avec les
mesures](docs/findings.md).

- **La forme d’abord, le style ensuite.** Les outils de reconstruction interprètent le bruit de surface comme de la géométrie. Une argile propre, semblable à une sculpture, avec des plans délibérément exagérés, donne un meilleur résultat en termes de topologie qu’un sprite stylisé ; le jumeau stylisé est généré en parallèle et sert de référence de couleur.
- **Définir le visage, obtenir un visage.** Un cadrage en buste ajoute **3,1 à 4,5 fois** plus de polygones à la tête, et la différence est structurelle : paupières séparées, sillon du sourcil, cavités nasales modélisées, et non un flou plus prononcé.
- **Les jumeaux appartiennent à un maillage, et non à un personnage.** Réutilisez un jumeau sur différents maillages, et la couverture diminue de **62 % à 22,7 %**, car les bras se projettent dans l’espace vide à côté du modèle. Générez des jumeaux à partir du maillage que vous allez texturer, à chaque fois.
- **L’identité appartient à l’invite.** Un élément canonique non mentionné dans l’invite apparaît par erreur et disparaîtra de la même manière : cela est mesuré lorsque des plaques de genou dorées se sont avérées n’apparaître dans l’image que par le biais du bruit dans un ControlNet défectueux.
- **Demandez à la géométrie, et non à un seuil.** Le remplacement d’un masque clé par la silhouette exacte du lancer de rayons a déplacé la couverture de référence de **28,4 % à 39,1 %** de texels valides, de manière strictement additive, sans diffusion, sans utilisation du GPU. Le masquage par médiane des coins a maintenant échoué **quatre** fois ici et est abandonné : un dégradé peint, un rendu d’argile en nuances de gris, un arrière-plan de studio éclairé d’un modèle de diffusion et une référence de diffusion dont les propres coins s’étendent sur L\* 48,1 à 81,1. ⚠ La forme est toujours présente dans un seul produit, `tools/verify/gate_mesh.py`, qui échantillonne un seul coin : il est nommé ici plutôt que simplement inclus.
- **Supprimez ce qu’aucune caméra ne peut voir, à partir de l’atlas et jamais du maillage.** 49 % des texels de l’atlas sont invisibles de l’extérieur ; l’exclusion de ces faces réduit l’interpolation de **68 %**. L’exclusion plutôt que la suppression rend l’échec impossible au lieu de simplement détectable.

## Ce qui n’est pas résolu

Nommé et mesuré, sur la page d’accueil plutôt que dans une note de bas de page. [Tous, situés dans le code](docs/known-defects.md).

- **Certaines zones de la surface visible sont mappées sur l'espace de l'atlas, mais aucune n'est jamais écrite lors du processus de « bake »**, et elles sont affichées comme le noir par défaut non modifié de l'image. Le système de « bake » de Blender utilise un échantillonnage au centre des texels, de sorte qu'un triangle qui ne chevauche aucun centre de texel reste vide — ses propres développeurs
[ont nommé ce mécanisme et ont intégré une correction](https://projects.blender.org/blender/blender/pulls/161752)
deux semaines après la version à partir de laquelle toutes les mesures ont été effectuées. Il s'agit d'une propriété de la trajectoire,
et non d'un objet spécifique : mesurée sur un actif, **non mesurée sur les quatre autres**.
- **La bande de texture couvre 0,00 % de la référence de l’étape 1** sur les huit caméras : l’acier sur un fond gris se trouve exactement au seuil de la texture. La combinaison permet de récupérer 55,72 %.
- **Les joints de texture ne sont pas uniformisés.** Une limite de provenance présente une variation de texture **5,5 fois** supérieure à la normale ; la zone nommée par le directeur présente une variation **9,5 fois** supérieure.
- **La diffusion se propage entre les îles de l’atlas non liées** — 74,9 % des texels diffusés tirent leur
couleur d’une autre île, avec une distance médiane de 0,177 sur une figure de 1,0 de hauteur. ⚠ **Cette part se trouve dans les texels de l’atlas et ne constitue pas une affirmation sur ce qu’une caméra voit** : la diffusion représente 26,95 % de l’atlas généré et **4,95 % des pixels de la figure rendus**, soit un rapport de 0,18. La peinture se trouve dans de grandes cartes, les trous se trouvent dans de petites cartes, de sorte qu’un texel diffusé est peu coûteux dans l’espace d’affichage.
- **⚑ Le défaut qui détermine l’acceptation est lié à la PEINTURE, et non à un remplissage** — les zones qui affichent la couleur d’un autre matériau, ce que aucune statistique de texture ne peut détecter. Mesuré de trois manières différentes, lors de trois sessions dans trois espaces : **91,05 % `reference`, avec un enrichissement de 0,99**, ce qui correspond exactement au taux de base ; la même classe dans le vert du tissu **68,46 % `reference`** ; et sur une fine bande, les propres texels peints de la surface **18,77 %** sont contaminés par rapport à son remplissage de diffusion, qui est de **5,55 %**.
Le remplissage provient correctement de son voisin peint le plus proche, et ce voisin est déjà
incorrect. Le mélange lui-même est une division à deux bandes non documentée
(`M + gaussian_blur_σ16(B − M)`) qui mesure **la pire des quatre** alternatives sur les mêmes
points.
- **⚑ Une face peinte présente des bandes, et c’est la découverte de la propriété qui s’applique à un actif accepté.** La face jumelle de A1 est une seule couche continue ; le « bake » est divisé en bandes verticales de différentes nuances de pêche. `project_twins` est **le gagnant remporte tout** — une caméra gagne chaque texel sans partage en fonction du poids de la face, de la propriété plutôt que de la moyenne — et la face est visible par la vue avant et les deux quarts à 45°, ce qui **présente une différence de valeur de la peau de R 13,0 / G 13,9 / B 18,3** sur le cercle accepté. Partout où deux cartes UV sur la face sont la propriété de caméras différentes, la différence se manifeste sous la forme d’une démarcation nette, de sorte que **les bandes sont des limites d’îles, et non de la saleté** — ni de la classe du trou gris. **Le pinceau ne peut pas corriger cela structurellement** : `commit` écrit uniquement dans les texels de trou et les texels stylisés sont figés. Deux solutions sont nommées, mais aucune n’est appliquée : laisser la vue avant posséder toute la bande de la tête, ou un mélange de joints **autorisé à réécrire la peau stylisée**, ce que aucune étape de cette trajectoire ne peut faire actuellement.
La moyenne pondérée est déjà accumulée dans l’outil et l’atlas mélangé existe déjà
sur le disque ; personne ne l’a mis à la disposition du directeur. **Cela était présent sur la feuille à partir de laquelle le « bake » a été approuvé**, et l’approbation couvrait l’identité et l’ensemble des vêtements — un défaut ouvert sur un artefact accepté n’est pas une contradiction, mais le compte rendu ne doit pas indiquer qu’une approbation couvre une propriété qui n’a pas été évaluée.
- **Les vues ne sont jamais indépendantes, ce qui limite toute correction de mélange.** Pour chaque groupe de défauts,
**100 % des faces avec deux caméras ou plus ont toutes ces caméras à l’intérieur d’un angle de 90°**
(médiane de 45°), et 21 % des faces défectueuses sont vues par une seule caméra. Les vues adjacentes sous un contrôle presque identique échouent ensemble, de sorte que les gains multi-vues publiés de la photogrammétrie ne se traduisent pas ici en valeur nominale.
- **Chaque reconstruction sur cette trajectoire est une coquille creuse à double paroi**, les parois mesurant environ deux voxels. Aucune condition volumétrique n’est valide sur l’une d’elles.
- **Les plaques sont en désaccord aux limites de matériaux non nommés, et le canon est la clé**
(16-08-2026). La déformation intérieure vers le maillage mesurée **3,5 à 11,1 px en médiane** sur les huit vues, par rapport aux médianes de silhouette de 1,2 à 3,0 ; chaque région résiduelle que le directeur a encerclée — coupe de manche, main, dessus de la botte — est un joint de matériau que l’invite de génération n’a jamais nommé. ⚠ **CORRIGÉ le 17-08-2026, et la correction affine la découverte.**
Il est écrit que « l’invite enregistrée comporte six éléments » : il a été constaté qu’elle fusionne deux fichiers différents. Le flux de travail qui a généré les jumeaux nomme **16 des 17**, ne manquant que la prise ; le *profil par défaut du pinceau* en nomme six. Les deux sont vrais, et la phrase contenait une seule affirmation fausse. Ce qui est important et qui persiste : la prise, le bracelet, le protège-jambe et la main apparaissent **zéro** fois dans l’invite de 16 phrases — car **aucun élément pour eux n’existe dans le canon**. Une invite complète ne peut toujours pas nommer une main qui n’a jamais été spécifiée.
✅ **FERMÉ le 17-08-2026** — la liste des surfaces est parcourue, remplie et **24/24 ratifiée**, et la porte refuse désormais une invite qui ne la couvre pas.
- **4,65 à 5,57 % des texels valides sont des surfaces qu’aucune caméra à anneau plat ne peut voir** — elles échouent au niveau du seuil de profondeur dans toutes les vues, aucune trajectoire de projection ne peut les peindre, et le pipeline livré les a recouvert du remplissage aveugle de l’île qui a créé les marques sombres. Elles ont besoin d’une politique (matériau neutre, pinceau ou acceptation), et non d’une correction
([rapport E49](docs/experiments/E49-finish-and-cap-report.md)).
- **Polygones colorés plats sur les feuilles de qualité acceptée** — la seule classe ouverte du directeur.
⚠ **L’hypothèse du passage de remplissage est FAUSSE (17-08-2026).** Le remplissage orphelin mesure *en dessous* de son propre taux de base au niveau du défaut (0,27 x), les correctifs se trouvent à 90 à 99 % sur des texels peints normaux, et le même défaut est présent dans un rendu construit à partir d’un atlas qui précède la correction dont il est tenu responsable. Il est plutôt lié à sa source : le jumeau de la vue de rendu est propre à cet endroit, et une **vue différente** possède 97 des 115 pixels défectueux avec un angle de 0,68 par rapport à 0,60. Le correctif angulaire est un **artefact de dispersion** et la couleur est une réelle différence entre les vues sur une surface qui a déjà été nommée — de sorte qu’une régénération du jumeau n’est pas justifiée par le fait que « le défaut se trouve dans les jumeaux ».
⚠ **Et la correction que cette page a proposée est également FAUSSE (17-08-2026).** Il est écrit que « un compositeur préférant la vue cible est la correction à portée de main et ne coûte rien ». Le compositeur existait déjà et était déjà la valeur par défaut ; mesuré par rapport au classificateur plat sur les images fixes d’une exécution enregistrée, la priorité à la cible **augmente** le nombre à la cible nommée (38 → 40) et l’augmente fortement à deux autres (23 → 64, 36 → 110), devenant *plus* connecté ce faisant. Le mécanisme : **la forme est la propriété, la couleur ne l’est pas.** L’olive est la propre peinture de la vue 6 d’une surface que la vue 6 peint correctement, de sorte qu’à la cible 6 — où la priorité à la cible signifie *préférer la vue 6* — la politique maximise exactement la peinture dont le défaut est constitué. **Une politique de propriété ne peut pas corriger une différence de couleur entre les vues sur une surface correctement attribuée**, ce qui met fin à la famille plutôt qu’à un seul de ses membres ([E52](docs/experiments/E52-target-first-flats-ruling.md)). Il ne reste qu’une question de peinture, et cela coûte une génération. *Texte remplacé, conservé conformément à la règle des corrections : « îles orphelines de la taille de simples triangles, remplies à plat à partir d’échantillons de jumeaux adjacents pris avec la silhouette non érodée. »

- **Une reconstruction qui ne procédera pas automatiquement à la création d’un squelette, sans aucun discriminateur connu.** L’un des six sujets est reconstruit correctement et échoue à la création automatique d’un squelette. L’entrée n’est pas texturée, le nombre de composants, la topologie du maillage et la pose sont chacun éliminés par mesure, et la cause que ce dépôt *a* indiquée a été falsifiée dans la même heure, de sorte que le tableau reste sans indication. L’utilisation d’un squelette qui existe déjà présente une limite mesurée plutôt qu’une solution : environ 20 degrés de rotation du bras restent corrects, environ 110 degrés déforment les épaules, et la fixation rigide de la plaque [ne la répare pas](docs/tools.md) — les trois tentatives de réparation ont été mesurées et les trois ont échoué.
- **Aucun accessoire n’a été monté et accepté.** Le contrat de taille et la porte de contact existent et sont testés sur des maillages synthétiques à une distance connue. Rien n’a encore été placé dans une main et évalué lors du zoom du directeur, et tant que cela ne se produit pas, la porte est un instrument sans point d’ancrage sur un actif réel.

## Comment ce dépôt est utilisé

La rigueur est aussi importante que le processus, et elle existe pour une raison : une série précédente a comporté dix sessions, chacune évaluant ses propres résultats et rédigeant des conclusions que la session suivante a considérées comme des faits établis. Rien dans cette boucle n’était vérifiable.

- **Spécifications avant le travail, rapport après, décision finale** — et la session qui conçoit une expérience n’évalue jamais ses propres résultats. Soixante-treize expériences sont disponibles dans [les archives](docs/experiments/).
- **Les corrections sont appliquées en place, à côté de la mesure qui les a invalidées**, et non sous forme de suppressions discrètes. Six affirmations initiales ont été falsifiées lors de la première session, et les six sont toujours lisibles à côté de ce qui les a remplacées.
- **Les échecs restent dans le dépôt avec leur raison.** [`tools/superseded/`](docs/tools.md) n’est pas une archive — n’importe qui peut exécuter ces outils et les voir échouer de la même manière.
- **Un résultat négatif est un succès total**, rapporté et clôturé plutôt que modifié pour atteindre un nombre.
- **Les tests sont liés au commit qui modifie le code** — 1 376 tests réussis sur deux postes, avec une intégration continue basée sur les chemins sur les 1 319 tests hermétiques.
- **Les archives sont consultables.** Un index SQLite + FTS5 sur l’ensemble du parcours, vérifié sur quatre systèmes. Il a trouvé une erreur dans le nombre de décisions que le texte avait mal indiqué à trois endroits, en comptant les archives elles-mêmes.

## Où tout se trouve

| | |
|---|---|
| **[Le manuel](docs/handbook/index.md)** | le guide — le parcours étape par étape, les sujets, le système de profil |
| **[Accessoires et squelettes](docs/handbook/props-and-rigs.md)** | l’étape suivant la peinture : le sujet qui ne procédera pas automatiquement à la création d’un squelette, et les deux contrats qui font d’un accessoire un accessoire |
| **[Préparation du concept](docs/concept-prep.md)** | le prototype de préparation en argile : son parcours de test 0, son placement et l’élément de licence qu’il ouvre |
| **[Les archives](docs/experiments/)** | soixante-treize expériences : spécifications, rapport, décision et chaque prédiction énoncée avant la mesure |
| **[Ce que le parcours a appris](docs/findings.md)** | les conclusions durables et les règles durement acquises, en intégralité |
| **[État de chaque outil](docs/tools.md)** | ce qui fonctionne, ce qui est obsolète et les preuves pour chacun |
| **[Défauts connus](docs/known-defects.md)** | tout ce qui n’a pas été résolu, mesuré et localisé dans le code |
| **[Le parcours, tel qu’il s’est déroulé](docs/arc-history.md)** | l’historique chronologique, avec les corrections intactes |
| **[CLAUDE.md](CLAUDE.md)** | comment travailler ici — les rôles, les règles et ce que chacun coûte |

## Position concernant la licence

Chaque étape s’exécute localement et est conforme aux exigences commerciales : SDXL (OpenRAIL++), MV-Adapter (open), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Exclusions délibérées, avec la raison : **nvdiffrast** (non commercial — appliqué ici par un mécanisme de sécurité structurel, et non par une attestation), **Hunyuan3D-Paint** (licence non valide dans l’UE, au Royaume-Uni et en Corée du Sud), **MVPaint** et **TEXGen** (aucune licence), et **UltraSharp / SUPIR / StableSR** (améliorateurs non commerciaux).

**La limite de la revendication, indiquée plutôt que laissée à la découverte.** Elle décrit le **parcours enregistré** — les étapes du diagramme ci-dessus, à partir de l’image vers la 3D. L’étape actuelle de préparation du prototype en argile en amont utilise une API cloud fermée dont les conditions, ce dépôt **n’a pas vérifiées**, de sorte qu’aucune revendication de licence ici ne couvre un actif créé à partir de l’un de ses argiles. Il s’agit d’un élément ouvert avec un chemin nommé pour le résoudre : le modèle local conforme à la licence est **Qwen-Image-Edit (Apache-2.0)**, et **FLUX.1-Kontext [dev] est exclu pour les mêmes raisons que nvdiffrast** — poids non commerciaux. Les deux sont vérifiés par rapport au catalogue de modèles du studio plutôt que rappelés ; le raisonnement se trouve dans [la préparation du concept](docs/concept-prep.md).

## Modèle de confiance et de menace

facet s’exécute entièrement sur votre propre machine — chaque outil est un script que vous exécutez sur des chemins que vous tapez, de sorte que la question pertinente n’est pas *quelles sont les autorisations demandées par cette application*, mais *que font ces scripts sur votre machine*. La réponse est fournie par la mesure, chaque cycle pouvant être réexécuté ; la politique complète se trouve dans [SECURITY.md](SECURITY.md) :

- **Données concernées :** maillages, textures, images et fichiers JSON sur le disque local, aux chemins que vous spécifiez dans la ligne de commande. De plus, `docs/index/facet.db`, qui est *dérivé* : il ne contient rien qui n’était pas déjà un fichier dans ce dépôt, et `facet_index.py build` le régénère à partir de zéro.
- **Données non concernées :** aucune donnée d’identification, jamais. Rien ici ne lit, ne stocke ni ne transmet de jeton, de clé ou de mot de passe, et rien de tel n’est présent dans l’arborescence : recherche effectuée pour les clés préfixées par le fournisseur, les jetons d’authentification GitHub (PAT), les jetons Slack, les ID de clés AWS, les blocs de clés privées, les jetons d’autorisation et les affectations en ligne `api_key`/`password`, **zéro correspondance**, aucun fichier ressemblant à une donnée d’identification n’est suivi.
- **Aucune télémétrie.** Aucune donnée n’est collectée ni envoyée. Il n’y a pas d’option de désactivation, car il n’y a rien à désactiver.
- **Sortie réseau :** deux outils ouvrent une socket : `restylize_views.py` et `texpass_brush.py`, et les deux appellent une API HTTP ComfyUI à l’adresse `--host`, **par défaut `127.0.0.1:8188`**. Rien d’autre dans `tools/` n’effectue d’appel réseau.
- **Autorisations :** utilisateur ordinaire. Pas d’élévation de privilèges, pas d’installation de service, pas d’écritures dans les paramètres système ou le registre.

Trois aspects importants sont mis en évidence plutôt que niés, car une note de sécurité qui ne contient que des assurances n’est pas un modèle de menace : **les opérations sur les fichiers ne sont pas exécutées dans un environnement isolé** (un outil écrit là où ses arguments l’indiquent) ; **les chemins locaux absolus sont intégrés dans de nombreux outils et documents** : 114 occurrences dans 26 fichiers, ce ne sont pas des secrets, mais une divulgation de la configuration d’une machine, et la raison pour laquelle la plupart des outils ne fonctionneront pas sans modification ailleurs ; et **les échecs inattendus se manifestent sous forme de traces Python dans les scripts de recherche non publiés**, sans passerelle `--debug`. Les arrêts intentionnels sont des messages `ANDON:` qui contiennent la mesure qui les a déclenchés. C’est le contrat de l’instrument de recherche, et [SHIP_GATE.md](SHIP_GATE.md) indique exactement quand il cesse d’être suffisant, ce qui, pour les deux commandes qui l’installent, est le cas à la version 0.2.0 : `facet-index` et `facet-mcp` renvoient `0` (OK) / `1` (erreur utilisateur) / `2` (erreur d’exécution), et, depuis [E22](docs/experiments/E22-ruling.md), **`4` REFUSÉ** pour une passerelle déclenchée ou une branche `verify` défaillante, ce qui signifie que l’outil fonctionne et vous indique de ne pas continuer plutôt qu’il s’agisse d’une erreur d’exécution. Tous les outils refusent avec un message d’erreur structuré qui indique l’étape suivante plutôt qu’une trace ([E21](docs/experiments/E21-cli-contract-report.md)).

**And the gates in those two commands are no longer deletable.** Every ANDON in what
facet installs `raise`s; a bare `assert` is a statement `python -O` removes silently,
and 87 of this repo's gates were removable by an environment variable until E22
converted them. Measured before and after on the same gate, in four interpreter modes.
**And since [E23](docs/experiments/E23-route-gates-report.md), neither are the gates on
the route that produced the four accepted assets** — its **57 sites across twelve
tools**, converted as a pure move on files no test had ever executed, each one now
refusing under `-O` and `PYTHONOPTIMIZE=1` as well as under a normal interpreter.
**And since [E25](docs/experiments/E25-ruling.md) the class is closed.** Its **133 sites
across 43 files** — the measurement instruments that produced the evidence for the four
accepted assets above — convert the same way, bringing the total that `raise` to **278**.
Exactly **one** bare ANDON `assert` remains anywhere under `tools/`:
`superseded/texpass_thin_mask.py`, which is **never** converted, because those tools are
kept so anyone can run them and watch them fail the same way. That remainder is pinned
**by name** in the test suite, so a future sweep cannot tidy it away without editing the
test on purpose.

**État du support :** ce dépôt est développé en mode ouvert, sur une seule machine, par un seul responsable et une paire d’experts et d’exécutants qui se relaient. `main` est le seul état pris en charge. Il n’y a pas de canal de publication, pas de politique de rétroportage et pas de SLA : à la place, il y a le registre : chaque affirmation est placée à côté du code qui la produit, et [docs/experiments](docs/experiments/) contient les spécifications, le rapport et la décision pour chacun.

## Exigences

Blender 5.x, Python 3.11+ avec `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Une installation locale de ComfyUI n’est nécessaire que pour le pinceau d’inpainting. Développé avec une RTX 5090 ; la marge de VRAM est plus importante que la vitesse brute.

**Deux interpréteurs, et la séparation est intentionnelle.** La suite, les outils MCP servis et chaque mesure sont exécutés sous l’environnement qui contient les paramètres CI (3.12). L’étape de reconstruction est exécutée sous un deuxième interpréteur, dont la version est fixée à **3.10**, car les roues TRELLIS dont il a besoin sont compilées pour cette version. Un outil qui échoue à l’importation est généralement exécuté avec l’autre interpréteur.

CI exécute le sous-ensemble hermétique de la suite sur **ubuntu-latest / Python 3.12** avec des installations fixes (`.github/workflows/ci.yml`) ; la couche des artefacts a besoin des arbres enregistrés sous `E:\AI\training`, qui ne sont pas dans git, de sorte que CI les désélectionne par conception. Localement, `python -m pytest` exécute les **1376** tests et `python -m pytest -m "not artifacts"` exécute les **1319** tests reproduits par CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
