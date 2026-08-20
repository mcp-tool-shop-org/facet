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

Le style est appliqué **sur l’élément**, dans l’espace de texture — et non peint pour chaque vue, puis assemblé par la suite. Fournissez à la séquence une représentation en argile aux formes exagérées, et elle renverra un maillage texturé dont la couleur provient d’une référence stylisée de *ce* maillage, avec tout ce que la référence ne pouvait pas voir, rempli par un pinceau de retouche masqué et une dilatation tenant compte de la surface.

Nommé en fonction des deux aspects du problème : les polygones et la face qu’ils doivent représenter.

## Installation

La séquence elle-même est un ensemble de scripts locaux que vous exécutez sur des chemins que vous tapez — clonez le dépôt et lisez [comment démarrer](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Deux serveurs sont fournis dans un seul package** : l’index des enregistrements, afin qu’un assistant puisse interroger la trace des preuves au lieu de la lire, et **à partir de la version 0.4.0, le serveur de mesure**, de sorte que deux éléments mesurés à plusieurs mois d’intervalle passent par un seul chemin de code.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` est le serveur MCP stdio qui traite les enregistrements (six outils, dont la vérification sur quatre points comme surface de contrôle) et `facet-index` est l’index lui-même (`build` / `verify` / `q` / `claims`). Exécutez l’un ou l’autre à partir d’un répertoire cloné ; `--db` désigne un index différent.

### Le serveur de mesure — nouveauté dans la version 0.4.0

`facet-measure` répond à la **partie numérique** d’une comparaison et n’indique jamais si le résultat est bon. Chaque charge utile contient la version du serveur, le hachage du fichier de l’instrument et un hachage de configuration, et `measure_report` **refuse** de comparer en cas de divergence — ce qui est la propriété pour laquelle tout cela existe.

Vérifié en exécutant une **commande** plutôt que `--help` : un maillage de contrôle renvoie 786 432 faces avec une enveloppe d’identité complète sur une machine où aucun répertoire cloné n’est présent.

**Ce que vous obtenez dépend d’une seule chose, et c’est votre version de Python :**

| votre Python | `[measure-full]` vous donne |
|---|---|
| **3.11 / 3.12** | **les huit outils** — `open3d` s’installe à partir de PyPI |
| **3.13** | quatre outils ; `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 est la dernière *version* et publie des roues cp38–cp312 **sans sdist**, de sorte que sur 3.13, il n’y a rien sur PyPI à installer. Le fichier supplémentaire le fournit en arrière-plan via `python_version < "3.13"`, de sorte que l’installation **réussit** et les quatre outils de géométrie renvoient **`4` REFUSÉ**, indiquant ce dont ils ont besoin — plutôt que l’échec complet de l’installation.

**Pour obtenir les huit sur Python 3.13**, Open3D publie des roues cp313 actuelles sur son canal de développement continu. Une URL directe est acceptable dans la ligne de commande ; elle n’est interdite que dans les métadonnées du package publié :

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **Sur Windows et macOS, les roues de développement sont suffixées par `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` au moment de la rédaction) et le nom change lorsque `main` change — listez les éléments sur [la version `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) et prenez la version actuelle. **Cette version est celle par rapport à laquelle les nombres de cette séquence, qui dépendent d’open3d, ont été mesurés**, et elle constitue une véritable limite de comparabilité : l’enveloppe d’identité enregistre le hachage de l’instrument, et non ses dépendances — [E31](docs/experiments/E31-ruling.md).

*Jusqu’à la version 0.3.1, la roue contenait deux fichiers `.py` et aucun des instruments de mesure, de sorte qu’un serveur de mesure installé n’avait rien à exécuter. Personne ne l’a remarqué pendant quatre versions parce que ce dépôt EST le répertoire cloné : l’outil fonctionnait là où il était construit et n’avait jamais été ailleurs.*

⚠ **`pip install facet-mcp` était défectueux dans toutes les versions publiées jusqu’à la version 0.3.0, et est corrigé dans la version 0.3.1.** La roue installe `facet_index` comme un module de niveau supérieur, de sorte que jusqu’à et y compris la version 0.3.0, elle résolvait l’emplacement de l’enregistrement par rapport à `<venv>/Lib` — qui ne contient ni corpus ni index — et `build`, `claims` et `q` sans `--db` échouaient tous. **Pour la version 0.3.0 ou antérieure, utilisez le fichier binaire `npx` ci-dessus.**

À partir de la version 0.3.1, la racine est résolue en **testant l’existence de l’enregistrement** plutôt qu’en supposant son existence : exécutez l’une ou l’autre commande à partir d’un répertoire cloné et elle le trouvera ; exécutez-la depuis n’importe quel autre endroit et elle renverra **`4` REFUSÉ**, en indiquant les deux répertoires qu’elle a essayés et les deux marqueurs qu’elle a recherchés. `$FACET_INDEX_DB` est maintenant lu par les deux commandes, et il sélectionne l’*index*, jamais le *corpus*. Mesuré sur une roue construite à partir de `main` et installée dans un environnement virtuel propre — [E24](docs/experiments/E24-ruling.md).

*Ce bloc a été corrigé deux fois. Il indiquait d’abord `pipx install facet-mcp # ou le package Python directement `, until v0.3.0's read-back ran a **verb** instead of ` --help`. Ensuite, il affirmait que la roue « ne fonctionne que pour `q` et `claims` » — **`claims` ne fonctionnait pas non plus**, ce qu’E24 a découvert en l’exécutant. Les deux corrections se trouvent dans [known-defects.md](docs/known-defects.md) avec leurs mesures.*

## État actuel

**Quatre éléments acceptés, répartis sur quatre classes de sujets, pour zéro crédit.** Chacun a été validé par le directeur à son propre niveau de zoom — sur le fichier GLB ou sur des feuilles de taille réelle — et non par une métrique qui dépasse un seuil.

| sujet | classe | accepté | référence / pinceau / dilatation |
|---|---|---|---|
| **Character (W3)** | humanoïde | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | véhicule, armature fine | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bête, membranes des ailes | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | accessoire, presque 2D, gris sur gris | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Les parts sont constituées de texels valides et **elles ne sont pas comparables entre les sujets** : un navire cache la majeure partie de lui depuis le niveau des yeux et un animal en cache la moitié. Évaluez chacun par rapport à son propre plafond d’étendue préenregistré, par rapport auquel ils atteignent **86 à 93 %** : la différence entre les lignes est géométrique, et non une régression. [Nombres complets avec leurs dénominateurs](docs/handbook/subjects.md).

**Un cinquième sujet est en cours de traitement, et il s'agit de la première référence construite en premier.** (2026-08-17 → 2026-08-19). A1, « l’archiviste », a été créé à partir d’une référence contenant sa propre recette intégrée, plutôt que d’un concept basé sur de l’argile, et chaque étape ultérieure a été validée en fonction de cela : le canon a été approuvé avec **16/16 surfaces** avant même qu’un maillage n’existe, un maillage a été approuvé par le directeur, un environnement a reproduit la référence **pixel pour pixel trois fois**, une paire d’images à huit vues acceptée avec un manifeste sha256, et deux erreurs de contamination nommées ont été mesurées sur chaque mécanisme avant que quoi que ce soit ne soit modifié. La cuisson a été approuvée [2026-08-19](docs/experiments/E70-baked-look-report.md) — **en termes d’identité et de l’ensemble des vêtements, et c’est la totalité du champ d’application de cette approbation.**

**Ensuite, le pinceau s’est ouvert et il n’écrit que dans les trous.** La première passe a été effectuée avec un angle de lacet de 90 degrés le 2026-08-19 : l’invariance ANDON affichait **0,014 lv avec la plus grande composante chaude de 0 px** en dehors de la figure sur les 472 318 px testés, et `commit` a écrit **3 585 texels**, remplissant les trous **2 044 423 → 2 040 838** avec l’atlas source vérifié byte par byte par la suite. Au niveau du zoom du directeur, le triangle pâle au niveau du col et de l’épaule du gilet est devenu pourpre et la couture apparaît comme un seul vêtement. Il n’a pas inventé un visage, tourné la tête ou peint un deuxième gilet.

**Le résultat méthodologique compte plus que l’actif.** Tout au long de cette période, la force de ControlNet n’a jamais été modifiée : chaque correction a **éliminé une cause** plutôt que d’appliquer une force contre celle-ci. Deux des erreurs étaient des défauts de spécification propres à l’expert, détectés par les systèmes d’exécution et par un canal d’examen externe avant qu’un crédit ne soit dépensé, et les deux sont nommés dans le registre avec la mesure qui les a invalidées.

**Il s’agit d’un pipeline, pas d’un générateur à un seul caractère.** Contredisez la spécification sur huit éléments nommés et l’invite remporte **8 sur 8** — ΔE médian de 46,3 contre 6,2 sur cinq contrôles maintenus — tandis que la figure reste la même. La structure est maintenue par le maillage et le contrôle ; les attributs nommés sont liés à l’invite.

**La question du projecteur a été close le 2026-08-16** ([E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md)). Les huit plaques **composent** : reconstruites à partir de l’ensemble par vue en utilisant les poids de bordure × orientation × visibilité, le rendu de l’atlas a franchi pour la première fois la barre d’acceptation du directeur sur cet itinéraire — deux fois, sur deux périodes — à côté d’un atlas publié dont l’itinéraire avait pour effet de dégrader la peinture des plaques. La chaîne qui a permis cela se trouve dans `tools/` (`emit_view_aovs`, `s3_composite`, `flow_estimate`, `s3_run`, `s3_sheet`, `atlas_from_aovs`, `twin_mesh_warp`), construite en grande partie par le biais d’un canal d’examen externe dont les revendications de calibration nominatives ont été maintenues **vingt sur vingt**, chacune étant vérifiée ici en l’exécutant avant que quoi que ce soit ne fasse confiance à la construction.

**Le canon est une donnée, et il contrôle la dépense (2026-08-17).** La spécification d’identité a nommé dix-sept éléments ; le flux de travail qui a généré les paires a nommé seize ; la valeur par défaut du profil, une nouvelle exécution utiliserait six. Rien ne les reliait, donc quatre périodes ont corrigé la composition en aval de la peinture qui était incorrecte à la source. Le canon est maintenant une base de données indexée sur **surface** — une liste d’éléments ne peut pas vous montrer ce qui manque, et un occupant nullable transforme un trou en une ligne — et `canon_gate` s’exécute **à l’intérieur** des outils qui créent une génération, avant que le répertoire de sortie n’existe. Une génération dont l’invite ne couvre pas le canon approuvé est refusée et rien n’est écrit.

**Il s’agit d’un routeur, et il est configuré pour être sécurisé.** Il résout un sujet dans son fichier de canon, couvre une invite dans **les deux** sens et transporte un champ d’application. **Un outil qui crée une dépense et à qui aucun canon n’est fourni ne procède pas en douceur — il refuse.** La solution pour un sujet qui n’en a réellement pas est basée sur des données statistiques et ne peut pas être utilisée par un sujet qui en a : `--no-canon --subject GALLEON` procède et s’annonce ; `--no-canon --subject W3` est **refusé**, car W3 a des surfaces. Cela ferme la case à cocher par construction plutôt que par convention, et cela compte parce que la forme précédente — `if args.canon:` — a permis au pilote PowerShell publié de passer silencieusement la barrière.

**La deuxième direction est celle qui détecte un défaut réel.** Vérifier que l’invite *contient* le canon révèle une invite peu précise. Vérifier que tout dans l’invite *est* du canon révèle une phrase nommant quelque chose que le personnage n’a pas — et il y en avait une dans la valeur par défaut active : **`gold necklace`**, ce référentiel l’avait déjà mesurée comme ayant mal nommé la médaille de ceinture dorée, *"et l’élément survit par accident."* Une invite complète avec cette phrase ajoutée renvoie maintenant `missing: 0` et refuse quand même, en nommant la clause.

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

`prof_hit 5/19` est un **échantillon délibérément cassé** : il s’agit de la valeur par défaut active qu’une exécution utiliserait réellement, donc le premier `--profile character.json` est censé s’arrêter. La réparation de la chaîne supprimerait les preuves.

**Et il existe une feuille de calcul, car les quatre sujets sans canon ne vont pas se déplacer tout seuls.** Elle émet chaque surface qu’un *type* de sujet implique — donc un trou est une ligne avant que quelqu’un ne l’ait nommé — transforme un fichier IDENTITY.md en un inventaire, transporte des joints par paires pour confirmer et réserve des emplacements de champ d’application par vue. Il est **structurellement incapable de remplir un occupant**, et c’est la propriété sur laquelle il est testé : une phrase toxique arrivant avec une surface déjà attribuée n’est pas écrite. La génération du canon consiste pour un humain à parcourir une référence ; la feuille de calcul ne fait que rendre cette tâche moins coûteuse et plus complète.

**La limite de la porte est définie explicitement plutôt que laissée à la découverte.** Elle vérifie les phrases du canon validé dans les deux sens, sur une certaine étendue. Elle ne vérifie pas les paraphrases ou les synonymes — un appariement sémantique placerait un modèle à l’intérieur d’une porte, ce que ce dépôt refuse en principe —, ni les éléments par vue tant qu’une portée de vue n’est pas déclarée, ni si un matériau nommé est apparu sur la surface *correcte*. Des emplacements de portée existent et leurs listes de surfaces sont vides : les remplir nécessite une intervention humaine, comme pour remplir des espaces. Quatre sujets ont un fichier IDENTITY.md et aucun fichier JSON de surfaces — ce qui a été laissé inachevé plutôt que généré sans avoir parcouru la référence.

**Le nombre d’éléments qu’une requête peut contenir est mesuré, mais il n’atteint pas le canon.** La documentation évalue chaque élément ajouté à une requête en fonction du coût de son apparition, sur une plage bien inférieure à la nôtre, de sorte qu’un ensemble Opus a demandé si les éléments déjà payés pouvaient suffire. **Ce n’est pas possible, et la raison est structurelle** : aucun élément du corpus ne conserve sa phrase constante alors que le nombre qui l’entoure varie *et* peut être absent. Ce qu’ils fournissent, c’est une limite unilatérale, à partir de cinq requêtes pour une caméra avec un contrôle, un masque et une graine identiques : sur une échelle d’éléments allant de **10 à 17**, le nombre supprimé n’a rien changé par rapport à ce qui était présent à 10, tandis qu’un changement d’identité au niveau *zéro* a modifié l’intervalle d’étalonnage complet. **Le canon de W3 exige 19 éléments, et le corpus ne l’atteint jamais** ([E55](docs/experiments/E55-density-vs-identity-report.md)). Le studio affiche les trois nombres qui sont combinés : 24 surfaces de requête, 25 vérifications requises, 19 éléments uniques — ainsi, un nombre de couverture n’est jamais comparé à une mesure du nombre d’éléments.

## Le parcours

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

Étape par étape, avec la justification pour chaque étape : **[le manuel](docs/handbook/index.md)**.

**Le saut en pointillés est nouveau et n’est pas intentionnellement solide.** La première boîte du parcours affiche toujours *concept d’argile*, et jusqu’à présent, rien ici ne l’avait créé — chaque argile arrivait à la main et était hachée en cours de route. Un outil concept→argile existe maintenant et sa première paire a été testée à pleine échelle : pose, bracelets, médaillon de ceinture et ourlet déchiré ont tous été pris en compte ; la masse de crinière n’a pas été prise en compte ; le débordement de couleur a été mesuré sur l’ensemble de l’image avec **C\* p99,9 = 13,15** et un arrière-plan achromatique uniforme. **Ce que cette paire ne peut pas montrer, c’est si le maillage s’améliore**, ce qui est la seule question qui justifie son utilisation, il reste donc un candidat avec ses preuves enregistrées : **[préparation du concept](docs/concept-prep.md)**.

## Ce qui le rend efficace

Six découvertes, chacune d’entre elles nécessitant une expérience et chacune d’entre elles étant applicable au-delà du sujet qui l’a produite. [La version longue, avec les mesures](docs/findings.md).

- **D’abord la forme, puis le style.** Les outils de reconstruction interprètent le bruit de surface comme une géométrie. Une argile propre et sculpturale, avec des plans délibérément exagérés, donne un meilleur résultat en termes de topologie qu’un sprite stylisé ; le jumeau stylisé est généré simultanément et devient la référence de couleur.
- **Encadrez le visage, obtenez un visage.** Un recadrage du buste place **3,1 à 4,5 fois** plus de polygones sur la tête, et la différence est structurelle — paupières séparées, sillon frontal, cavités des narines modélisées — et non une simple amélioration du flou.
- **Les jumeaux appartiennent à un maillage, pas à un personnage.** Réutilisez un jumeau dans différents maillages et la couverture diminue de **62 % à 22,7 %**, car les bras se projettent dans l’espace vide à côté du modèle. Générez des jumeaux à partir du maillage que vous allez texturer, à chaque fois.
- **L’identité appartient à la requête.** Un élément du canon qui n’est pas nommé dans la requête arrive par hasard et repartira de la même manière — ce qui est mesuré lorsque les plaques dorées sur les genoux se sont avérées n’apparaître que par le biais du bruit dans un ControlNet défectueux.
- **Demandez à la géométrie, pas à un seuil.** Le remplacement d’un masque clé par la silhouette exacte du lancer de rayons a amélioré la couverture de référence de **28,4 % à 39,1 %** des texels valides — strictement additif, sans diffusion, sans GPU. La technique de masquage basée sur les coins a maintenant échoué trois fois ici et est abandonnée.
- **Supprimez ce que aucune caméra ne peut voir, à partir de l’atlas et jamais du maillage.** 49 % des texels de l’atlas sont invisibles depuis l’extérieur ; l’exclusion de ces faces réduit l’interpolation de **68 %**. L’exclusion plutôt que la suppression rend l’échec impossible au lieu d’être simplement détectable.

## Ce qui n’est pas résolu

Nommé et mesuré, en première page plutôt que dans une note de bas de page. [Tous, situés dans le code](docs/known-defects.md).

- **Certaines zones de la surface visible sont mappées sur l'espace de l'atlas, mais ne sont jamais écrites lors du processus de « bake »**, et s'affichent donc en noir par défaut. Le système de « baking » de Blender utilise un échantillonnage au centre des texels ; ainsi, si un triangle chevauche une zone sans centre de texel, cette zone reste vide. Les développeurs ont identifié ce mécanisme et intégré une correction deux semaines après la date à laquelle les données suivantes ont été collectées. Il s'agit d'une propriété du processus, et non d'un élément spécifique : mesuré sur un actif, **non mesuré sur les quatre autres**.
- **La bande de texture occupe 0,00 % de la référence de l'étape 1** sur les huit caméras. L'acier sur un fond gris se positionne exactement au seuil défini. La combinaison permet d'obtenir un résultat de 55,72 %.
- **Les joints des textures ne sont pas uniformisés.** Une limite de provenance présente une variation de texture ordinaire de **5,5×** ; la zone désignée par le directeur présente une variation de **9,5×**.
- **La dilatation se propage entre les différentes zones de l'atlas** : 74,9 % des texels dilatés prennent leur couleur d'une autre zone, avec une distance médiane de 0,177 sur une figure de hauteur 1,0. ⚠ **Cette proportion concerne les texels de l'atlas et ne représente pas ce qu'une caméra voit** : la dilatation représente 26,95 % de l'atlas généré et **4,95 % des pixels rendus**, soit un rapport de 0,18×. La peinture est présente dans les grandes cartes, les trous dans les petites ; par conséquent, un texel dilaté est peu coûteux en termes d'espace d'affichage.
- **⚑ Le défaut qui détermine l'acceptation est lié à la PEINTURE, et non à un remplissage quelconque** : il s'agit de zones affichant la couleur d'un autre matériau, ce que les statistiques sur les motifs ne peuvent pas détecter. Mesuré de trois manières différentes, lors de trois sessions dans trois espaces différents : **91,05 % `reference` avec un enrichissement de 0,99×**, correspondant parfaitement au taux de base ; la même classe en vert pour le tissu : **68,46 % `reference`** ; et sur une fine bande, les texels peints de la surface elle-même présentent une contamination de **18,77 %** par rapport à un remplissage de dilatation de **5,55 %**. Le remplissage est correctement issu du voisin peint le plus proche, et ce voisin présente déjà un défaut. Le mélange lui-même est une division en deux bandes non documentée (`M + gaussian_blur_σ16(B − M)`) qui mesure la valeur la plus faible parmi quatre alternatives sur les mêmes points.
- **⚑ Une face peinte présente des bandes, et c'est cette caractéristique qui détermine si l'actif est accepté.** La face jumelle de A1 est une surface continue ; le « bake » est divisé en bandes verticales de différentes nuances de pêche. `project_twins` est un système du type « celui qui gagne remporte tout » : chaque texel est définitivement attribué à une caméra en fonction de son angle d'incidence, et non par moyenne. La face est visible depuis l'avant et les deux quarts à 45°, ce qui entraîne une différence de valeur de couleur de **R 13,0 / G 13,9 / B 18,3** sur le pourtour accepté. Partout où deux cartes UV sur la face sont attribuées à des caméras différentes, cette différence se manifeste sous forme d'une démarcation nette ; par conséquent, **les bandes correspondent aux limites des zones de l'atlas et non à des imperfections**. **Le pinceau ne peut pas corriger cela structurellement** : `commit` écrit uniquement dans les texels vides et les texels stylisés sont figés. Deux solutions sont proposées, mais aucune n'est retenue : laisser la vue avant posséder toute la bande de la tête, ou autoriser un mélange des joints à **réécrire la texture de la peau**, ce que l'étape actuelle du processus ne permet pas. La moyenne pondérée est déjà calculée dans l'outil et l'atlas mélangé existe déjà sur le disque ; personne n'a encore présenté ces données au directeur. **Ces informations étaient présentes dans la feuille à partir de laquelle le « bake » a été approuvé**, et l'approbation couvrait l'identité et l'ensemble des vêtements. Un défaut apparent sur un artefact accepté n'est pas une contradiction, mais le compte rendu ne doit pas indiquer qu'une approbation couvre une propriété qui n'a pas été évaluée.
- **Les vues ne sont jamais indépendantes, ce qui limite les corrections possibles.** Pour chaque groupe de défauts, **100 % des faces avec deux caméras ou plus ont toutes ces caméras dans un angle de 90°** (médiane de 45°) et 21 % des faces présentant des défauts sont vues par une seule caméra. Les vues adjacentes soumises à des contrôles presque identiques échouent ensemble, de sorte que les gains multi-vues publiés par la photogrammétrie ne se traduisent pas directement ici.
- **Chaque reconstruction dans ce processus est une coquille creuse à double paroi**, avec des parois d'environ deux voxels. Aucune condition volumétrique n'est valide pour un seul voxel.
- **Les plaques présentent des différences aux limites des matériaux non nommés, et c'est là que réside le problème** (2026-08-16). La déformation de l'intérieur vers le maillage mesurée est de **3,5 à 11,1 px en médiane** sur les huit vues, par rapport aux médianes de silhouette de 1,2 à 3,0 ; chaque région que le directeur a identifiée (couture de la manche, main, haut de la botte) est un joint de matériau que l'invite de génération n'a pas nommé. ⚠ **CORRIGÉ le 2026-08-17, et cette correction renforce les conclusions.** Le texte initial indiquait : « l'invite enregistrée contient six éléments », mais il s'avère qu'elle fusionne en réalité deux fichiers différents. Le processus qui a généré les jumeaux identifie **16 des 17** éléments, ne manquant que la prise ; le *profil par défaut du pinceau* en nomme six. Les deux affirmations sont vraies, mais la phrase contenait une affirmation fausse parmi celles-ci. Ce qui est important et reste valable : la prise, le gantelet, le jambier et la main apparaissent **zéro** fois dans l'invite de 16 phrases, car **aucun élément correspondant n'existe dans le canon**. Une invite complète ne peut toujours pas nommer une main qui n'a jamais été spécifiée. ✅ **CLÔTURÉ le 2026-08-17** : la liste des surfaces est parcourue, complétée et **les 24/24 éléments sont validés**, et le système refuse désormais une invite qui ne les couvre pas.
- **De 4,65 % à 5,57 % des texels valides se trouvent sur une surface qu'aucune caméra n'est capable de voir** : ils échouent au test de profondeur dans toutes les vues, aucune route de projection ne peut les peindre, et le pipeline final a masqué ces zones avec un remplissage uniforme qui a créé les marques sombres. Ils nécessitent une politique (matériau neutre, pinceau ou acceptation), et non une correction ([rapport E49](docs/experiments/E49-finish-and-cap-report.md)).
- **Polygones colorés unis sur les feuilles de qualité acceptée** : c'est la seule classe ouverte du directeur. ⚠ **L'hypothèse du remplissage est RÉFUTÉE (2026-08-17).** Le remplissage orphelin présente une valeur *inférieure* à son taux de base au niveau du défaut (0,27×), les zones sont situées à 90 à 99 % sur des texels peints ordinaires, et le même défaut est présent dans un rendu créé à partir d'un atlas antérieur à la correction qui en était responsable. L'origine a été retracée : la vue jumelle du rendu est propre à cet endroit, et une **vue différente** possède 97 des 115 pixels défectueux avec un angle de 0,68 contre 0,60. La zone angulaire est un **artefact de diffusion**, et la couleur est une réelle différence entre les vues sur une surface déjà nommée ; par conséquent, une régénération jumelle n'est pas justifiée par le fait que « le défaut se trouve dans les jumeaux ».
⚠ **Et la correction proposée dans cette page est également RÉFUTÉE (2026-08-17).** Le texte indiquait : « un compositeur préférant la vue cible est la solution, et elle ne coûte rien. » Or, le compositeur existait déjà et était déjà la valeur par défaut ; en le comparant au classificateur plat sur les images fixes d'une exécution enregistrée, l'utilisation de la vue cible en premier **augmente** le nombre à la cible nommée (38 → 40) et l'augmente considérablement dans deux autres cas (23 → 64, 36 → 110), ce qui rend le résultat *plus* cohérent. Le mécanisme : **la forme est une propriété, la couleur ne l'est pas.** L'olive est la peinture de la vue 6 sur une surface que la vue 6 peint correctement ; par conséquent, à la cible 6 (où « utiliser la vue cible en premier » signifie *préférer la vue 6*), la politique maximise précisément la peinture dont le défaut est constitué. **Une politique de propriété ne peut pas corriger une différence de couleur entre les vues sur une surface correctement attribuée**, ce qui élimine l'ensemble plutôt qu'une seule partie ([E52](docs/experiments/E52-target-first-flats-ruling.md)). Il reste alors une question de peinture, et cela coûte une génération. *Texte supprimé, conservé conformément à la règle des corrections : « îles orphelines de la taille de simples triangles, remplies uniformément à partir d'échantillons adjacents pris sur les jumeaux avec la silhouette non érodée ».

## Comment ce dépôt est utilisé

La rigueur est aussi importante que le processus lui-même, et elle répond à un objectif : une série précédente a comporté dix sessions au cours desquelles chaque participant a évalué son propre travail et rédigé des conclusions qui ont été lues lors de la session suivante comme des faits établis. Rien dans cette boucle n’était vérifiable.

- **Définir les spécifications avant le travail, rédiger un rapport après, prendre une décision finale** — et la session qui conçoit une expérience n’évalue jamais ses propres résultats. Soixante-douze expériences sont disponibles dans [les archives](docs/experiments/).
- **Les corrections sont intégrées en même temps que les mesures qui les ont invalidées**, et non sous forme de suppressions discrètes. Six affirmations initiales ont été réfutées lors de la première session, et les six sont toujours accessibles à côté de ce qui les a remplacées.
- **Les échecs restent dans le dépôt avec leur justification.** [`tools/superseded/`](docs/tools.md) n’est pas une archive ; chacun peut exécuter ces outils et observer qu’ils échouent de la même manière.
- **Un résultat négatif est un succès total**, qui est signalé et clôturé plutôt que d’être ajusté pour atteindre une valeur cible.
- **Les tests sont liés au commit qui modifie le code** — 1 346 tests réussis, évalués par deux personnes, avec une intégration continue basée sur les chemins pour les 1 289 tests hermétiques.
- **Les archives peuvent être consultées.** Un index SQLite + FTS5 couvre l’ensemble du processus et a été vérifié à quatre reprises. Il a identifié un nombre de décisions erroné dans le texte à trois endroits, en comptant les entrées des archives elles-mêmes.

## Où tout se trouve

| | |
|---|---|
| **[Le guide](docs/handbook/index.md)** | le guide — le déroulement étape par étape, les sujets et le système de profilage |
| **[Préparation du concept](docs/concept-prep.md)** | l’étape candidate de préparation des modèles : son déroulement à l’étape 0, son placement et l’élément de licence qu’elle ouvre |
| **[Les archives](docs/experiments/)** | soixante-douze expériences : spécifications, rapport, décision et chaque prédiction formulée avant la mesure |
| **[Ce que le processus a permis de découvrir](docs/findings.md)** | les conclusions durables et les règles obtenues avec difficulté, en intégralité |
| **[État de chaque outil](docs/tools.md)** | ce qui fonctionne, ce qui est obsolète et les preuves pour chacun |
| **[Défauts connus](docs/known-defects.md)** | tout ce qui n’a pas été résolu, mesuré et localisé dans le code |
| **[Le déroulement du processus, tel qu’il s’est produit](docs/arc-history.md)** | l’historique chronologique, avec les corrections intactes |
| **[CLAUDE.md](CLAUDE.md)** | comment travailler ici — les rôles, les règles et ce que chacun implique |

## Position concernant la licence

Chaque étape s’exécute localement et est conforme aux exigences commerciales : SDXL (OpenRAIL++), MV-Adapter (open source), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Exclusions délibérées, avec justification : **nvdiffrast** (non commercial — appliqué ici par un mécanisme de sécurité structurel, et non par une attestation), **Hunyuan3D-Paint** (licence invalide dans l’UE, au Royaume-Uni et en Corée du Sud), **MVPaint** et **TEXGen** (aucune licence) et **UltraSharp / SUPIR / StableSR** (améliorateurs d’image non commerciaux).

**La limite de la revendication est définie plutôt que laissée à la découverte.** Elle décrit le **processus enregistré** — les étapes du diagramme ci-dessus, de l’image au modèle 3D. L’étape candidate de préparation des modèles en amont exécute actuellement une API cloud fermée dont les conditions d’utilisation n’ont pas été vérifiées par ce dépôt. Par conséquent, aucune revendication de licence ici ne couvre un élément créé à partir de l’un de ses modèles. Il s’agit d’un point ouvert pour lequel il existe un cheminement défini pour le résoudre : le modèle local conforme aux exigences de la licence est **Qwen-Image-Edit (Apache-2.0)**, et **FLUX.1-Kontext [dev] est exclu pour les mêmes raisons que nvdiffrast** — poids non commerciaux. Les deux ont été vérifiés par rapport au catalogue de modèles du studio plutôt qu’ils ont été rappelés ; la justification se trouve dans [la préparation du concept](docs/concept-prep.md).

## Modèle de confiance et de menace

facet s’exécute entièrement sur votre propre machine — chaque outil est un script que vous exécutez sur des chemins que vous saisissez, la question pertinente n’est donc pas *quelles sont les autorisations demandées par cette application*, mais *ce que font ces scripts sur votre machine*. La réponse est fournie par la mesure, et chaque cycle peut être répété ; la politique complète se trouve dans [SECURITY.md](SECURITY.md) :

- **Données concernées :** maillages, textures, images et fichiers JSON sur le disque local, aux chemins que vous indiquez dans la ligne de commande. De plus, `docs/index/facet.db`, qui est *dérivé* — il ne contient rien qui n’était pas déjà un fichier dans ce dépôt, et `facet_index.py build` le régénère à partir de zéro.
- **Données non concernées :** aucune information d’identification, jamais. Rien ici ne lit, ne stocke ou ne transmet de jeton, de clé ou de mot de passe, et rien de tel n’est présent dans l’arborescence — recherche effectuée pour les clés préfixées par le fournisseur, les GitHub PAT, les jetons Slack, les ID de clé AWS, les blocs de clé privée, les jetons d’authentification et les affectations en ligne `api_key`/`password`, **zéro correspondance**, aucun fichier ressemblant à une information d’identification suivi.
- **Aucune télémétrie.** Rien n’est collecté ni envoyé. Il n’y a pas de possibilité de désactivation car il n’y a rien à désactiver.
- **Échange réseau :** deux outils ouvrent un socket — `restylize_views.py` et `texpass_brush.py` — et les deux appellent une API HTTP ComfyUI à l’adresse `--host`, **par défaut `127.0.0.1:8188`**. Rien d’autre dans `tools/` n’effectue d’appel réseau.
- **Autorisations :** utilisateur ordinaire. Aucune élévation de privilèges, aucune installation de service, aucune écriture dans les paramètres du système ou le registre.

Trois arêtes vives sont révélées plutôt que niées, car une note de sécurité qui ne contient que des assurances n’est pas un modèle de menace : les opérations sur les fichiers ne sont pas exécutées dans un environnement isolé (un outil écrit partout où ses arguments l’indiquent) ; les chemins locaux absolus sont intégrés à de nombreux outils et documents — 114 occurrences dans 26 fichiers, ce n’est pas des secrets mais la divulgation de la configuration d’une machine, et la raison pour laquelle la plupart des outils ne fonctionneront pas sans modification ailleurs ; et les échecs inattendus se manifestent sous forme de traces Python dans les scripts de recherche non publiés, sans `--debug`. Les arrêts intentionnels sont des messages `ANDON:` qui contiennent la mesure qui les a déclenchés. C’est le contrat de l’instrument de recherche, et [SHIP_GATE.md](SHIP_GATE.md) enregistre précisément quand il cesse d’être suffisant — ce qui était le cas pour les deux commandes, à la version 0.2.0 : `facet-index` et `facet-mcp` renvoient `0` (OK) / `1` (erreur utilisateur) / `2` (erreur d’exécution), et, depuis [E22](docs/experiments/E22-ruling.md), `4` est REFUSÉ pour un déclencheur activé ou une branche `verify` défaillante, ce qui signifie que l’outil fonctionne et vous indique de ne pas continuer plutôt qu’il s’agisse d’une erreur d’exécution. Tous les éléments refusent avec un message d’erreur structuré indiquant l’étape suivante au lieu d’une trace ([E21](docs/experiments/E21-cli-contract-report.md)).

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

**État du support :** ce dépôt est développé en mode ouvert, sur une seule plateforme, par un seul responsable et une paire d’experts et d’exécutants qui se relaient. `main` est le seul état pris en charge. Il n’y a pas de canal de publication, pas de politique de rétroportage et pas de SLA : ce qu’il y a à la place, c’est l’enregistrement : chaque affirmation est placée à côté du code qui la produit, et [docs/experiments](docs/experiments/) contient les spécifications, le rapport et le résultat pour chacun.

## Exigences

Blender 5.x, Python 3.11+ avec `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Une installation locale de ComfyUI n’est nécessaire que pour le pinceau d’inpainting. Développé sur une RTX 5090 ; la marge de VRAM est plus importante que la vitesse brute.

CI exécute l’ensemble hermétique de la suite sur ubuntu-latest / Python 3.12 avec des installations fixes (`.github/workflows/ci.yml`) ; le niveau des artefacts nécessite les arbres enregistrés sous `E:\AI\training`, qui ne sont pas dans git, de sorte que CI les désélectionne par conception. Localement, `python -m pytest` exécute les 1 346 tests et `python -m pytest -m "not artifacts"` exécute les 1 289 tests reproduits par CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
