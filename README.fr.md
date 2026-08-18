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

Le style est appliqué **sur l’élément**, dans l’espace de texture, et non pas peint pour chaque vue puis assemblé par la suite. Fournissez à la chaîne un concept d’argile aux formes exagérées, et elle renverra une maille texturée dont la couleur provient d’une référence stylisée de *cette* maille, avec tout ce que la référence ne pouvait pas voir rempli par un pinceau de retouche masqué et une dilatation tenant compte de la surface.

Nommé en fonction des deux aspects du problème : les polygones et la face qu’ils doivent représenter.

## Installation

La chaîne elle-même est un ensemble de scripts locaux que vous exécutez sur des chemins que vous tapez : clonez le dépôt et lisez [comment démarrer](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Deux serveurs sont fournis dans un seul package** : l’index des enregistrements, afin qu’un assistant puisse interroger la trace des preuves au lieu de la lire, et **à partir de la version 0.4.0, le serveur de mesure**, afin que deux éléments mesurés à plusieurs mois d’intervalle passent par un seul chemin de code.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` est le serveur MCP stdio qui traite les enregistrements (six outils, dont la vérification à quatre points servant de surface de santé qui refuse), et `facet-index` est l’index lui-même (`build` / `verify` / `q` / `claims`). Exécutez l’un ou l’autre depuis un répertoire extrait ; `--db` désigne un index différent.

### Le serveur de mesure : nouveauté dans la version 0.4.0

`facet-measure` répond à la **partie numérique** d’une comparaison et n’indique jamais si le résultat est bon. Chaque charge utile contient la version du serveur, le hachage du fichier de l’instrument et un hachage de configuration, et `measure_report` **refuse** de comparer des éléments qui ne correspondent pas, ce qui est précisément la raison d’être de tout cela.

Vérifié en exécutant une **commande** plutôt que `--help` : une maille de contrôle renvoie 786 432 faces avec un enveloppe d’identité complète sur une machine qui ne contient pas de répertoire extrait.

**Ce que vous obtenez dépend d’une seule chose, et c’est votre version de Python :**

| votre Python | `[measure-full]` vous donne |
|---|---|
| **3.11 / 3.12** | **les huit outils** : `open3d` s’installe à partir de PyPI |
| **3.13** | quatre outils : `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 est la dernière *version* et publie des roues cp38–cp312 **sans sdist**, de sorte que sur 3.13, il n’y a rien à installer sur PyPI. Le fichier supplémentaire le fournit en arrière-plan via `python_version < "3.13"`, de sorte que l’installation **réussit** et les quatre outils de géométrie renvoient **`4` REFUSÉ**, indiquant ce dont ils ont besoin, plutôt que de faire échouer toute l’installation.

**Pour obtenir les huit sur Python 3.13**, Open3D publie des roues cp313 actuelles sur son canal de développement continu. Une URL directe est acceptable dans une ligne de commande ; elle n’est interdite que dans les métadonnées du package publié :

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **Sur Windows et macOS, les roues de développement sont suffixées par `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` au moment de la rédaction), et le nom change lorsque `main` change : listez les éléments sur [la version `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) et prenez la version actuelle. **C’est avec cette version que les nombres de cette chaîne, qui dépendent d’Open3D, ont été mesurés**, et c’est une véritable limite de comparabilité : l’enveloppe d’identité enregistre le hachage de l’instrument, pas ses dépendances — [E31](docs/experiments/E31-ruling.md).

*Jusqu’à la version 0.3.1, la roue contenait deux fichiers `.py` et aucun des instruments de mesure, de sorte qu’un serveur de mesure installé n’avait rien à exécuter. Personne ne l’a remarqué pendant quatre versions parce que ce dépôt EST le répertoire extrait : l’outil fonctionnait là où il était construit et n’avait jamais été ailleurs.*

⚠ **`pip install facet-mcp` était défectueux dans toutes les versions publiées jusqu’à la version 0.3.0, et est corrigé dans la version 0.3.1.** La roue installe `facet_index` en tant que module de premier niveau, de sorte que jusqu’à et y compris la version 0.3.0, elle résolvait l’emplacement de l’enregistrement par rapport à `<venv>/Lib`, qui ne contient ni corpus ni index, et `build`, `claims` et `q` sans `--db` échouaient tous.
**Pour la version 0.3.0 ou antérieure, utilisez le fichier binaire `npx` ci-dessus.**

À partir de la version 0.3.1, la racine est résolue en **vérifiant l’existence de l’enregistrement** plutôt qu’en supposant son existence : exécutez l’une ou l’autre des commandes depuis un répertoire extrait et elle le trouvera ; exécutez-la depuis n’importe quel autre endroit et elle renverra **`4` REFUSÉ**, en indiquant les deux répertoires qu’elle a essayés et les deux marqueurs qu’elle a recherchés. `$FACET_INDEX_DB` est maintenant lu par les deux commandes, et il sélectionne l’*index*, jamais le *corpus*. Mesuré sur une roue construite à partir de `main` et installée dans un environnement virtuel propre — [E24](docs/experiments/E24-ruling.md).

*Ce bloc a été corrigé deux fois. Il indiquait d’abord `pipx install facet-mcp # ou le package Python directement `, until v0.3.0's read-back ran a **verb** instead of ` --help`.
Il affirmait ensuite que la roue « ne fonctionne que pour `q` et `claims` » — **`claims` ne fonctionnait pas non plus**, ce que E24 a découvert en l’exécutant. Les deux corrections se trouvent dans [known-defects.md](docs/known-defects.md) avec leurs mesures.*

## Où cela en est

**Quatre éléments acceptés, répartis sur quatre classes de sujets, sans frais.** Chacun a été validé par le directeur à son propre niveau de zoom : sur le fichier GLB ou sur des feuilles de taille réelle, et non pas par une métrique qui dépasse un seuil.

| sujet | classe | accepté | référence / pinceau / dilatation |
|---|---|---|---|
| **Character (W3)** | humanoïde | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | véhicule, gréement fin | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bête, membranes des ailes | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | accessoire, presque 2D, gris sur gris | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Les parts sont constituées de texels valides, et **elles ne sont pas comparables entre les sujets** : un navire cache la majeure partie de lui depuis le niveau des yeux et un animal en cache la moitié. Évaluez chaque élément par rapport à son propre plafond d’étendue préenregistré, par rapport auquel ils atteignent **86 à 93 %** : la différence entre les lignes est géométrique, pas une régression. [Nombres complets, avec leurs dénominateurs](docs/handbook/subjects.md).

**Il s’agit d’un pipeline, et non d’un générateur à un seul caractère.** Contredisez la spécification sur huit éléments nommés et l’invite gagne **8 sur 8** : ΔE médian de 46,3 contre 6,2 sur cinq contrôles maintenus — tandis que la figure reste le même homme. La structure est assurée par la maille et le contrôle ; les attributs nommés sont liés à l’invite.

**La question du projecteur est close le 2026-08-16** ([E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
Les huit calques **composent**: reconstruits à partir de l’ensemble par vue, en utilisant les
poids de bordure × orientation × visibilité, le rendu de l’atlas a franchi pour la première fois
le seuil d’acceptation du directeur sur cette séquence — deux fois, sur deux arcs — à côté d’un
atlas dont la séquence avait pour effet de détériorer la peinture des calques. La chaîne qui a permis cela se trouve dans `tools/`
(`emit_view_aovs`, `s3_composite`, `flow_estimate`, `s3_run`, `s3_sheet`,
`atlas_from_aovs`, `twin_mesh_warp`), construite en grande partie grâce à un canal d’évaluation externe
dont les revendications de calibration désignées se sont avérées exactes **dix-sept fois sur dix-sept**, chacune étant
vérifiée ici en l’exécutant avant que quoi que ce soit ne valide la construction.

**Le canon est une donnée, et il limite les dépenses (2026-08-17).** La spécification d’identité
mentionne dix-sept éléments ; le flux de travail qui a généré les jumeaux en mentionne seize ; la
configuration par défaut qu’une nouvelle exécution utiliserait en mentionne six. Rien ne les relie, donc quatre arcs
ont corrigé la composition en aval de la peinture qui était incorrecte à la source. Le canon est maintenant une
base de données indexée sur **la surface** — une liste d’éléments ne peut pas vous montrer ce qui manque, et un
champ nullable crée un trou dans une ligne — et `canon_gate` s’exécute **à l’intérieur** de `restylize_views`
et `texpass_brush`, avant que le répertoire de sortie n’existe. Une génération dont la requête ne couvre
pas le canon validé est refusée et rien n’est écrit.

```
canon_gate 1.0.0  census  (occupancy is not ratification)
subject      named   occupancy   ratified   prof_hit surfaces
W3              19       24/24      24/24       5/19 canon/w3.surfaces.json
GALLEON         13           -          -      11/13 NONE
DRAGON          11           -          -      10/11 NONE
LONGSWORD        5         5/5        5/5        4/5 canon/longsword.surfaces.json
E10-LAYER        1           -          -          - NONE
LOGO             0           -          -          - NONE
```

`prof_hit 5/19` est un **échantillon intentionnellement laissé incomplet** : c’est la configuration par défaut en direct qu’une exécution
utiliserait réellement, donc la première `--profile character.json` est censée s’arrêter. La réparation
de la chaîne supprimerait les preuves.

**La limite de la grille est définie plutôt que laissée à découvrir.** Elle vérifie que
la requête contient les expressions du canon validé. Elle ne vérifie **pas** les paraphrases,
les éléments par vue, les brouillons non validés, les sujets sans fichier de surfaces ou si un matériau nommé
s’est retrouvé sur la bonne surface. Quatre sujets ont un fichier IDENTITY.md et aucun fichier JSON de surfaces — laissé inachevé plutôt que généré sans parcourir la référence.

## La séquence

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

Étape par étape, avec le raisonnement pour chaque étape : **[le manuel](docs/handbook/index.md)**.

**Le saut en pointillés est nouveau et n’est pas intentionnellement continu.** Le premier bloc de la séquence a toujours
affiché *concept d’argile*, et jusqu’à présent, rien ici ne l’avait créé — chaque argile était apportée à la main et
hachée en cours de route. Un outil concept→argile existe maintenant et sa première paire a été testée
à pleine échelle : pose, bracelets de poignet, médaillon de ceinture et ourlet déchiré, tous inclus ; la masse de crinière n’y était pas ; fuite de couleur mesurée sur toute l’image à **C\* p99,9 = 13,15** avec un arrière-plan monochrome uniforme. **Ce que cette paire ne peut pas montrer, c’est si le maillage est amélioré**, ce qui est
la seule question qui permettrait de la valider, elle reste donc une candidate avec ses preuves enregistrées :
**[préparation du concept](docs/concept-prep.md)**.

## Ce qui fait que cela fonctionne

Six découvertes, chacune d’entre elles nécessitant un test et chacune d’entre elles étant applicable au-delà du
sujet qui l’a produite. [La version longue, avec les
mesures](docs/findings.md).

- **D’abord la forme, ensuite le style.** Les outils de reconstruction interprètent le bruit de surface comme une géométrie. Une argile propre, semblable à une sculpture et dotée de plans délibérément exagérés, donne un meilleur résultat en termes de topologie
qu’un sprite stylisé ; le jumeau stylisé est généré simultanément et devient la
référence de couleur.
- **Encadrez le visage, obtenez un visage.** Un recadrage du buste place **3,1 à 4,5 fois** plus de polygones sur
la tête, et la différence est structurelle — paupières séparées, sillon frontal, cavités des narines modélisées — et non une simple amélioration du flou.
- **Les jumeaux appartiennent à un maillage, pas à un personnage.** Réutilisez un jumeau sur différents maillages et la couverture diminue de **62 % à 22,7 %**, car les bras se projettent dans l’espace vide à côté du modèle.
Générez des jumeaux à partir du maillage que vous allez texturer, à chaque fois.
- **L’identité appartient à la requête.** Un élément du canon qui n’est pas nommé dans la requête arrive
par hasard et repartira de la même manière — mesuré lorsque les plaques de genoux dorées se sont avérées atteindre l’image uniquement par le biais du bruit dans un ControlNet défectueux.
- **Demandez à la géométrie, pas à un seuil.** Le remplacement d’un masque indexé par la silhouette exacte du lancer de rayons a amélioré la couverture de référence de **28,4 % à 39,1 %** des texels valides — strictement
additive, sans diffusion, sans GPU. La clé médiane angulaire a maintenant échoué trois fois ici et est abandonnée.
- **Supprimez ce qu’aucune caméra ne peut voir, de l’atlas et jamais du maillage.** 49 % des texels de l’atlas
sont invisibles depuis l’extérieur ; l’exclusion de ces faces réduit l’interpolation de **68 %**. L’exclusion plutôt que la suppression rend l’échec impossible au lieu d’être simplement détectable.

## Ce qui n’est pas résolu

Nommé et mesuré, sur la page de garde plutôt que dans une note de bas de page. [Tous, situés dans le
code](docs/known-defects.md).

- **Certaines zones de surface visibles sont mappées à l’espace de l’atlas, mais ne sont jamais écrites lors du processus de « bake »**, et elles s’affichent comme le noir par défaut non modifié de l’image. Le moteur de « baking » de Blender utilise un échantillonnage au centre des texels, donc un triangle qui chevauche une zone sans centre de texel reste vide — ses propres développeurs
[ont nommé ce mécanisme et ont intégré une correction](https://projects.blender.org/blender/blender/pulls/161752)
deux semaines après la version sur laquelle tous les chiffres ici ont été mesurés. Il s’agit d’une propriété de la séquence,
et non d’un objet spécifique : mesuré sur un actif, **non mesuré sur les quatre autres**.
- **La bande du bordure représente 0,00 % de la référence de l’étape 1** sur les huit caméras — l’acier sur un fond gris se positionne exactement au seuil défini. La combinaison permet de récupérer 55,72 %.
- **Les joints des textures ne sont pas uniformisés.** Une limite de provenance présente une variation de texture **5,5×** supérieure à la normale ; la zone que le Directeur a identifiée présente une variation de **9,5×**.
- **La dilatation se propage entre les îles de l’atlas non liées** — 74,9 % des texels dilatés tirent leur couleur d’une autre île, avec un écart médian de 0,177 sur une figure de hauteur 1,0. ⚠ **Cette part concerne les texels de l’atlas et ne constitue pas une affirmation sur ce que voit la caméra** : la dilatation représente 26,95 % de l’atlas généré et **4,95 % des pixels rendus de la figure**, soit un rapport de 0,18×. La peinture se trouve dans les grandes cartes, les trous dans les petites, donc un texel dilaté est peu coûteux en termes d’espace à l’écran.
- **⚑ Le défaut qui détermine l’acceptation est lié à la PEINTURE, et non à aucun remplissage** — régions affichant la couleur d’un autre matériau, ce que aucune statistique de « speckle » ne peut détecter. Mesuré de trois manières différentes lors de trois sessions dans trois espaces : **91,05 % `reference`, avec un enrichissement de 0,99×**, correspondant parfaitement au taux de base ; la même classe en vert pour le tissu **68,46 % `reference`** ; et sur une fine bordure, les propres texels peints de la surface **18,77 %** sont contaminés par rapport à ses **5,55 %** de remplissage de dilatation.
Le remplissage provient correctement du voisin peint le plus proche — et ce voisin est déjà incorrect. Le mélange lui-même est une division en deux bandes non documentée
(`M + gaussian_blur_σ16(B − M)`) qui mesure la **pire des quatre** alternatives sur les mêmes points.
- **Les vues ne sont jamais indépendantes, ce qui limite toute correction de mélange.** Pour chaque groupe de défauts,
**100 % des faces avec deux caméras ou plus contribuant ont toutes ces caméras à l’intérieur d’un angle de 90°**
(médiane de 45°), et 21 % des faces défectueuses sont vues par une seule caméra. Les vues adjacentes soumises à un contrôle presque identique échouent ensemble, de sorte que les gains multi-vues publiés de la photogrammétrie ne se traduisent pas directement ici.
- **Chaque reconstruction dans cette séquence est une coquille creuse à double paroi**, avec des parois d’environ deux voxels. Aucune condition volumétrique n’est valide pour l’une d’entre elles.
- **Les plaques divergent aux limites de matériaux non nommés, et le canon est la clé**
(2026-08-16). La déformation intérieure du maillage par rapport à sa jumelle a été mesurée avec une médiane de **3,5 à 11,1 px** sur les huit vues, par rapport aux médianes de silhouette de 1,2 à 3,0 ; chaque région résiduelle que le Directeur a encerclée — coupe de manche, main, dessus de botte — est un joint de matériau que l’invite de génération n’a jamais nommé. ⚠ **CORRIGÉ le 2026-08-17, et la correction affine les résultats.** Ce texte indiquait : « l’invite enregistrée contient six éléments », mais il s’est avéré qu’elle fusionne deux fichiers différents. Le flux de travail qui a généré les jumelles nomme **16 des 17**, ne manquant que la prise ; le *profil par défaut du pinceau* en nomme six. Les deux sont vrais, et la phrase contenait une seule affirmation fausse parmi celles-ci. Ce qui est important : la prise, le bracelet, le protège-jambe et la main apparaissent **zéro** fois dans l’invite de 16 phrases — car **aucun élément pour eux n’existe dans le canon**. Une invite complète ne peut toujours pas nommer une main qui n’a jamais été spécifiée.
✅ **CLÔTURÉ le 2026-08-17** — la liste des surfaces est parcourue, remplie et **validée sur les 24/24**, et la porte refuse désormais une invite qui ne la couvre pas.
- **De 4,65 % à 5,57 % des texels valides sont des surfaces qu’aucune caméra à anneau plat ne peut voir** — ils échouent au niveau du filtre de profondeur dans toutes les vues, aucune route de projection ne peut les peindre, et le pipeline fourni a masqué ces zones avec un remplissage aveugle qui a créé les marques sombres. Ils ont besoin d’une politique (matériau neutre, pinceau ou acceptation), pas d’une correction
([rapport E49](docs/experiments/E49-finish-and-cap-report.md)).
- **Polygones colorés plats sur les feuilles de qualité acceptable** — la seule classe ouverte du Directeur.
⚠ **L’hypothèse du passage de remplissage est RÉFUTÉE (2026-08-17).** Le remplissage orphelin mesure *en dessous* de son propre taux de base au niveau du défaut (0,27×), les zones sont situées à 90 à 99 % sur des texels peints normaux, et le même défaut est présent dans un rendu construit à partir d’un atlas qui précède la correction dont il est accusé. Il a plutôt été retracé jusqu’à sa source : la jumelle de la vue du rendu est propre à cet endroit, et une **vue différente** possède 97 des 115 pixels défectueux avec un angle de 0,68 par rapport à 0,60. La zone angulaire est un **artéfact de diffusion**, et la couleur est une réelle divergence entre les vues sur une surface qui a déjà été nommée — donc une régénération de jumelle n’est pas justifiée par le fait que « le défaut se trouve dans les jumelles ». Un compositeur préférant la vue cible est la correction à portée, et elle ne coûte rien. *Texte supprimé, conservé conformément à la règle des corrections : « îles orphelines de la taille de simples triangles, remplies à plat à partir d’échantillons adjacents de jumelles pris avec la silhouette non érodée ».

## Comment ce dépôt est géré

La rigueur est aussi importante que le pipeline lui-même, et elle existe pour une raison : une séquence précédente a mené dix sessions au cours desquelles chaque session a évalué sa propre production et a rédigé des conclusions que la session suivante a considérées comme des faits établis. Rien dans cette boucle n’était vérifiable.

- **Définir les spécifications avant le travail, rédiger un rapport après, et établir une conclusion finale** — et la session qui conçoit une expérience n'évalue jamais ses propres résultats. Cinquante-et-une expériences sont disponibles dans [les archives](docs/experiments/).
- **Les corrections sont intégrées à leur emplacement, à côté de la mesure qui les a invalidées**, et non sous forme de suppressions discrètes. Six affirmations initiales ont été réfutées lors de la session initiale, et les six sont toujours consultables à côté de ce qui les a remplacées.
- **Les échecs restent dans le dépôt avec leur raison.** [`tools/superseded/`](docs/tools.md) n'est pas une archive — chacun peut exécuter ces outils et observer qu'ils échouent de la même manière.
- **Un résultat négatif est un succès total**, qui est rapporté et clôturé plutôt que modifié pour atteindre une valeur cible.
- **Les tests sont liés au commit qui modifie le code** — 1338 tests réussis, avec des contrôles d'intégration basés sur les chemins pour les 1284 tests hermétiques.
- **Les archives peuvent être consultées.** Un index SQLite + FTS5 sur l'ensemble du parcours, vérifié sur quatre axes. Il a trouvé un nombre de conclusions qui étaient incorrectes dans le texte à trois endroits, en comptant les enregistrements eux-mêmes.

## Où tout est

| | |
|---|---|
| **[Le manuel](docs/handbook/index.md)** | le guide — l'itinéraire étape par étape, les sujets, le système de profilage |
| **[Préparation du concept](docs/concept-prep.md)** | l'étape candidate de préparation de la modélisation : son parcours Gate 0, son placement et l'élément de licence qu'elle ouvre |
| **[Les archives](docs/experiments/)** | cinquante-et-une expériences : spécifications, rapport, conclusions et chaque prédiction énoncée avant la mesure |
| **[Ce que l'itinéraire a appris](docs/findings.md)** | les résultats durables et les règles durement acquises, en intégralité |
| **[État de chaque outil](docs/tools.md)** | ce qui fonctionne, ce qui est obsolète et les preuves pour chacun |
| **[Défauts connus](docs/known-defects.md)** | tout ce qui n'est pas résolu, mesuré et localisé dans le code |
| **[Le déroulement, tel qu'il s'est produit](docs/arc-history.md)** | l'historique chronologique, avec les corrections intactes |
| **[CLAUDE.md](CLAUDE.md)** | comment travailler ici — les rôles, les règles et ce que chacun implique |

## Position de la licence

Chaque étape s'exécute localement et est conforme aux exigences commerciales : SDXL (OpenRAIL++), MV-Adapter (open source), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Exclu intentionnellement, avec la raison : **nvdiffrast** (non commercial — appliqué ici par un mécanisme de sécurité structurel, et non par une attestation), **Hunyuan3D-Paint** (licence invalide dans l'UE, au Royaume-Uni et en Corée du Sud), **MVPaint** et **TEXGen** (aucune licence) et **UltraSharp / SUPIR / StableSR** (améliorateurs non commerciaux).

**La limite de la revendication, énoncée plutôt que laissée à découvrir.** Il décrit l'**itinéraire enregistré** — les étapes du diagramme ci-dessus, de l'image vers la 3D. L'étape candidate de préparation de la modélisation en amont s'exécute actuellement sur une API cloud fermée dont les conditions ce dépôt **n'a pas vérifiées**, de sorte qu'aucune revendication de licence ici ne couvre un élément créé à partir d'un de ses modèles. Il s'agit d'un point ouvert avec un chemin défini pour le résoudre : le modèle local conforme aux exigences de licence est **Qwen-Image-Edit (Apache-2.0)**, et **FLUX.1-Kontext [dev] est exclu pour les mêmes raisons que nvdiffrast** — poids non commerciaux. Les deux sont vérifiés par rapport au catalogue de modèles du studio plutôt qu'ils ne sont rappelés ; le raisonnement se trouve dans [la préparation du concept](docs/concept-prep.md).

## Modèle de confiance et de menace

facet s'exécute entièrement sur votre propre machine — chaque outil est un script que vous exécutez sur des chemins que vous tapez, la question pertinente n'est donc pas *quelles sont les autorisations demandées par cette application*, mais *que font ces scripts à votre machine*. La réponse est fournie par la mesure, et chaque cycle peut être réexécuté ; la politique complète se trouve dans [SECURITY.md](SECURITY.md) :

- **Données concernées :** maillages, textures, images et JSON sur le disque local, aux chemins que vous indiquez dans la ligne de commande. De plus, `docs/index/facet.db`, qui est *dérivé* — il ne contient rien qui n'était pas déjà un fichier dans ce dépôt, et `facet_index.py build` le régénère à partir de zéro.
- **Données NON concernées :** aucune information d'identification, jamais. Rien ici ne lit, ne stocke ou ne transmet de jeton, de clé ou de mot de passe, et rien de tel n'est présent dans l'arborescence — recherche effectuée pour les clés préfixées par le fournisseur, les GitHub PAT, les jetons Slack, les ID de clé AWS, les blocs de clé privée, les jetons porteurs et les affectations en ligne `api_key`/`password`, **zéro correspondance**, aucun fichier ressemblant à une information d'identification suivi.
- **Pas de télémétrie.** Rien n'est collecté ni envoyé. Il n'y a pas d'option de désactivation car il n'y a rien à désactiver.
- **Échange réseau :** deux des trente-six outils ouvrent un socket — `restylize_views.py` et `texpass_brush.py` — et les deux appellent une API HTTP ComfyUI à `--host`, **par défaut `127.0.0.1:8188`**. Rien d'autre dans `tools/` n'effectue d'appel réseau.
- **Autorisations :** utilisateur ordinaire. Pas d'élévation de privilèges, pas d'installation de service, pas d'écriture dans les paramètres du système ou le registre.

Trois arêtes vives sont révélées plutôt que niées, car une note de sécurité qui ne contient que des assurances n’est pas un modèle de menace : les opérations sur les fichiers ne sont pas exécutées dans un environnement isolé (un outil écrit partout où ses arguments l’indiquent) ; les chemins locaux absolus sont intégrés à de nombreux outils et documents — 114 occurrences dans 26 fichiers, ce ne sont pas des secrets mais la divulgation de la configuration d’une machine, et la raison pour laquelle la plupart des outils ne fonctionneront pas sans modification ailleurs ; et les défaillances inattendues se manifestent sous forme de traces Python dans les 36 scripts de recherche non publiés, sans aucun filtre `--debug`. Les arrêts intentionnels sont des messages `ANDON:` qui contiennent la mesure qui les a déclenchés. C’est le contrat de l’instrument de recherche, et [SHIP_GATE.md](SHIP_GATE.md) enregistre précisément quand il cesse d’être suffisant — ce qui était le cas pour les deux commandes *d’installation* à la version 0.2.0 : `facet-index` et `facet-mcp` renvoient `0` ok / `1` erreur utilisateur / `2` erreur d’exécution — et, depuis [E22](docs/experiments/E22-ruling.md), **`4` REFUSÉ** pour un filtre déclenché ou une branche défaillante `verify`, ce qui signifie que l’outil fonctionne et vous indique de ne pas continuer plutôt qu’il s’agisse d’une erreur d’exécution. Tous les éléments refusent avec une défaillance structurée indiquant l’étape suivante au lieu d’une trace ([E21](docs/experiments/E21-cli-contract-report.md)).

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

**État du support :** ce dépôt est développé en mode ouvert, sur une seule plateforme, par un seul responsable et une paire d’experts et d’exécutants qui se relaient. `main` est le seul état pris en charge. Il n’y a pas de canal de publication, pas de politique de rétroportage et pas de SLA — à la place, il y a l’enregistrement : chaque affirmation est placée à côté du code qui la produit, et [docs/experiments](docs/experiments/) contient les spécifications, le rapport et le jugement pour chacun.

## Exigences

Blender 5.x, Python 3.11+ avec `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Une installation locale de ComfyUI n’est nécessaire que pour le pinceau d’inpainting. Développé sur une RTX 5090 ; la marge de VRAM est plus importante que la vitesse brute.

CI exécute le sous-ensemble hermétique de la suite sur **ubuntu-latest / Python 3.12** avec des installations fixes (`.github/workflows/ci.yml`) ; la couche d’artefacts a besoin des arbres enregistrés sous `E:\AI\training`, qui ne sont pas dans git, donc CI les désélectionne par conception. Localement, `python -m pytest` exécute les **1 338** tests et `python -m pytest -m "not artifacts"` exécute les **1 284** tests reproduits par CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
