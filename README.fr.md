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

Le style est appliqué **sur l’élément**, dans l’espace de texture, et non pas peint pour chaque vue puis assemblé par la suite. Fournissez à la chaîne un concept d’argile aux formes exagérées, et elle renverra une maille texturée dont la couleur provient d’une référence stylisée de *cette* maille, avec tout ce que la référence ne pouvait pas voir, complété par un pinceau de remplissage masqué et une dilatation tenant compte de la surface.

Nommé en fonction des deux aspects du problème : les polygones et la face qu’ils doivent représenter.

## Installation

La chaîne elle-même est un ensemble de scripts locaux que vous exécutez sur des chemins que vous tapez ; clonez le dépôt et lisez [comment démarrer](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Deux serveurs sont fournis dans un seul package** : l’index des enregistrements, afin qu’un assistant puisse interroger la trace des preuves au lieu de la lire, et **à partir de la version 0.4.0, le serveur de mesure**, afin que deux éléments mesurés à plusieurs mois d’intervalle passent par une seule chaîne de traitement.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` est le serveur MCP stdio qui traite les enregistrements (six outils, dont la vérification sur quatre points comme surface de référence) et `facet-index` est l’index lui-même (`build` / `verify` / `q` / `claims`). Exécutez l’un ou l’autre à partir d’un répertoire cloné ; `--db` désigne un index différent.

### Le serveur de mesure : nouveauté dans la version 0.4.0

`facet-measure` répond à la **partie numérique** d’une comparaison et n’indique jamais si le résultat est bon. Chaque charge utile contient la version du serveur, le hachage du fichier de l’instrument et un hachage de configuration, et `measure_report` **refuse** de comparer des éléments qui ne correspondent pas, ce qui est précisément la raison d’être de tout cela.

Vérifié en exécutant une **commande** plutôt que `--help` : une maille de contrôle renvoie 786 432 faces avec une enveloppe d’identité complète sur une machine qui ne contient pas le code source cloné.

**Ce que vous obtenez dépend d’une seule chose, et c’est votre version de Python :**

| votre Python | `[measure-full]` vous donne |
|---|---|
| **3.11 / 3.12** | **les huit outils** ; `open3d` s’installe à partir de PyPI |
| **3.13** | quatre outils : `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 est la dernière *version* et publie des roues cp38–cp312 **sans sdist**, de sorte que sur 3.13, il n’y a rien à installer sur PyPI. Le fichier supplémentaire le fournit en arrière-plan via `python_version < "3.13"`, de sorte que l’installation **réussie** et les quatre outils géométriques renvoient **`4` REFUSED** pour indiquer ce dont ils ont besoin, plutôt que l’échec complet de l’installation.

**Pour obtenir les huit sur Python 3.13**, Open3D publie des roues cp313 actuelles sur son canal de développement continu. Une URL directe est acceptable dans la ligne de commande ; elle n’est interdite que dans les métadonnées du package publié :

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **Sur Windows et macOS, les roues de développement sont suffixées par `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` au moment de la rédaction), et le nom change lorsque `main` change ; listez les éléments sur [la version `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) et prenez la version actuelle. **Cette version est celle par rapport à laquelle les nombres de cette chaîne, qui dépendent d’Open3D, ont été mesurés**, et elle constitue une véritable limite de comparabilité : l’enveloppe d’identité enregistre le hachage de l’instrument, et non ses dépendances — [E31](docs/experiments/E31-ruling.md).

*Jusqu’à la version 0.3.1, la roue contenait deux fichiers `.py` et aucun des instruments de mesure, de sorte qu’un serveur de mesure installé n’avait rien à exécuter. Personne ne l’a remarqué pendant quatre versions parce que ce dépôt EST le répertoire cloné : l’outil fonctionnait là où il était compilé et n’avait jamais été ailleurs.*

⚠ **`pip install facet-mcp` était défectueux dans toutes les versions publiées jusqu’à la version 0.3.0, et est corrigé dans la version 0.3.1.** La roue installe `facet_index` comme un module de premier niveau, de sorte que jusqu’à et y compris la version 0.3.0, elle résolvait l’emplacement de l’enregistrement par rapport à `<venv>/Lib`, qui ne contient ni corpus ni index, et `build`, `claims` et `q` sans `--db` échouaient tous. **Pour la version 0.3.0 ou antérieure, utilisez le fichier binaire `npx` ci-dessus.**

À partir de la version 0.3.1, la racine est résolue en **vérifiant l’existence de l’enregistrement** plutôt qu’en supposant son existence : exécutez l’une ou l’autre commande à partir d’un répertoire cloné et elle le trouvera ; exécutez-la depuis n’importe quel autre endroit et elle renverra **`4` REFUSED**, en indiquant les deux répertoires qu’elle a essayés et les deux marqueurs qu’elle a recherchés. `$FACET_INDEX_DB` est maintenant lu par les deux commandes, et il sélectionne l’*index*, jamais le *corpus*. Mesuré sur une roue compilée à partir de `main` et installée dans un environnement virtuel propre — [E24](docs/experiments/E24-ruling.md).

*Ce bloc a été corrigé deux fois. Il indiquait d’abord `pipx install facet-mcp # ou le package Python directement `, until v0.3.0's read-back ran a **verb** instead of ` --help`. Ensuite, il affirmait que la roue « ne fonctionne que pour `q` et `claims` » — **`claims` ne fonctionnait pas non plus**, ce qu’E24 a découvert en l’exécutant. Les deux corrections se trouvent dans [known-defects.md](docs/known-defects.md) avec leurs mesures.*

## Où cela en est

**Quatre éléments acceptés, répartis sur quatre classes de sujets, pour zéro crédit.** Chacun a été validé par le directeur à son propre niveau de zoom — sur le fichier GLB ou sur des feuilles de taille réelle — et non pas par une métrique qui dépasse un seuil.

| sujet | classe | accepté | référence / pinceau / dilatation |
|---|---|---|---|
| **Character (W3)** | humanoïde | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | véhicule, armature fine | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bête, membranes des ailes | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | accessoire, presque 2D, gris sur gris | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Les parts sont constituées de texels valides, et **elles ne sont pas comparables entre les sujets** : un navire cache la majeure partie de lui depuis le niveau des yeux et un animal en cache la moitié. Évaluez chaque élément par rapport à son propre plafond d’étendue préenregistré, par rapport auquel ils atteignent **86 à 93 %** : la différence entre les lignes est géométrique, et non une régression. [Chiffres complets avec leurs dénominateurs](docs/handbook/subjects.md).

**Il s’agit d’une chaîne de traitement, et non d’un générateur à un seul caractère.** Contredisez la spécification sur huit éléments nommés et l’invite gagne **8 sur 8** — ΔE médian de 46,3 contre 6,2 sur cinq contrôles maintenus — tandis que la figure reste le même homme. La structure est assurée par la maille et le contrôle ; les attributs nommés sont liés à l’invite.

**La question du projecteur est close le 16 août 2026** ([E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
Les huit calques **composent**: ils sont reconstitués à partir de l’ensemble par vue, en utilisant les poids de bordure × d’orientation × de visibilité. Le rendu de l’atlas a permis de satisfaire pour la première fois les exigences du directeur sur cette séquence — deux fois, sur deux arcs — à côté d’un atlas dont la séquence avait pour effet de détériorer la peinture des calques. La chaîne qui a permis cela se trouve dans `tools/`
(`emit_view_aovs`, `s3_composite`, `flow_estimate`, `s3_run`, `s3_sheet`,
`atlas_from_aovs`, `twin_mesh_warp`), et est principalement construite grâce à un canal d’évaluation externe dont les revendications de calibration nominées ont été validées **vingt fois sur vingt**, chacune étant vérifiée ici en l’exécutant avant que quoi que ce soit ne valide la construction.

**Le canon est une donnée, et il détermine le budget (17 août 2026).** La spécification d’identité a nommé dix-sept éléments ; le flux de travail qui a généré les jumeaux en a nommé seize ; la configuration par défaut pour une nouvelle exécution en a nommé six. Rien ne les relie, donc quatre arcs ont réparé la composition en aval de la peinture qui était incorrecte à la source. Le canon est maintenant une base de données indexée sur **la surface** — une liste d’éléments ne peut pas vous montrer ce qui manque, et un occupant nullable crée un trou dans une ligne — et `canon_gate` s’exécute **à l’intérieur** des outils qui créent une génération, avant que le répertoire de sortie n’existe. Une génération dont la requête ne couvre pas le canon validé est refusée et rien n’est écrit.

**C’est un routeur, et il est configuré pour être en mode sécurisé.** Il résout un sujet vers son fichier de canon, couvre une requête dans **les deux** sens et transporte une portée. Un **outil qui crée une séquence et à qui aucun canon n’est fourni ne procède pas silencieusement — il refuse.** La solution pour un sujet qui n’en a réellement pas est basée sur des données statistiques et ne peut être utilisée par un sujet qui en a : `--no-canon --subject GALLEON` procède et s’annonce ; `--no-canon --subject W3` est
**refusé**, car W3 possède des surfaces. Cela ferme la case à cocher par construction plutôt que par convention, et cela compte parce que la forme précédente — `if args.canon:` — permettait au pilote PowerShell expédié de passer le seuil en silence.

**La deuxième direction est celle qui détecte un défaut réel.** Vérifier que la requête *contient* le canon révèle une requête peu étoffée. Vérifier que tout dans la requête *est* du canon révèle une phrase nommant quelque chose que le personnage n’a pas — et il y en avait une présente dans la configuration par défaut : **`gold necklace`**, ce dépôt l’avait déjà identifiée comme désignant incorrectement le médaillon de ceinture dorée, *"et l’élément survit par hasard."* Une requête couvrant cette phrase est maintenant renvoyée `missing: 0` et est quand même refusée, nommant la clause.

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

`prof_hit 5/19` est un **échantillon délibérément laissé cassé** : c’est la configuration par défaut réelle qu’une exécution utiliserait, donc le premier `--profile character.json` est censé s’arrêter. La réparation de la chaîne supprimerait les preuves.

**Et il existe une feuille de calcul, car les quatre sujets sans canon ne vont pas se débrouiller tout seuls.** Elle émet chaque surface qu’un *type* de sujet implique — donc un trou est une ligne avant que quelqu’un ne l’ait nommé — et transforme un fichier IDENTITY.md en un inventaire, transporte des joints par paires pour confirmer et réserve des emplacements de portée par vue. Il est **structurellement incapable de remplir un occupant**, et c’est la propriété qui est testée : une phrase toxique arrivant avec une surface déjà attribuée n’est pas écrite. La génération d’un canon est un humain qui parcourt une référence ; la feuille de calcul ne fait que rendre cette tâche moins coûteuse et plus complète.

**La limite du seuil, indiquée plutôt que laissée à découvrir.** Elle vérifie les phrases du canon validé dans les deux sens, au niveau d’une portée. Elle ne vérifie **pas** les paraphrases ou les synonymes — une correspondance sémantique placerait un modèle à l’intérieur d’un seuil, ce que ce dépôt refuse en principe — ni les éléments par vue jusqu’à ce qu’une portée de vue soit déclarée, ni si un matériau nommé a atterri sur la *bonne* surface. Les emplacements de portée existent et leurs listes de surfaces sont vides : les remplir est une tâche humaine, comme remplir des occupants. Quatre sujets ont un fichier IDENTITY.md et aucun fichier JSON de surfaces — laissé inachevé plutôt que généré sans parcourir la référence.

**Le nombre d’éléments qu’une requête peut contenir est mesuré, et il n’atteint pas le canon.** La documentation fixe le prix de chaque élément de requête ajouté en fonction de l’impact sur la présence des éléments, dans une fourchette bien inférieure à la nôtre. Ainsi, un siège Opus a demandé si les calques déjà payés pouvaient résoudre ce problème. **Ils ne peuvent pas, et la raison est structurelle** — aucun élément du corpus ne maintient sa phrase constante pendant que le nombre qui l’entoure varie *et* qu’il peut être absent. Ce qu’ils donnent, c’est une limite unilatérale, à partir de cinq requêtes avec une caméra, un contrôle, un masque et une graine identiques : sur une échelle d’éléments de **10 → 17**, le nombre supprimé n’a **rien** enlevé de ce qui était présent à 10, tandis qu’un changement d’identité à *zéro* a déplacé l’intervalle de calibration complet. **Le canon de W3 demande 19 éléments, et le corpus ne l’atteint jamais** ([E55](docs/experiments/E55-density-vs-identity-report.md)). Le studio imprime les trois nombres qui sont combinés — 24 surfaces de requête, 25 vérifications requises, 19 éléments uniques — donc un nombre de couverture n’est jamais cité par rapport à une mesure du nombre d’éléments.

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

Étape par étape, avec la justification pour chaque étape : **[le manuel](docs/handbook/index.md)**.

**Le saut en pointillés est nouveau et il est délibérément non solide.** La première case de la séquence a toujours affiché *concept d’argile*, et jusqu’à présent, rien ici n’en créait un — chaque argile arrivait à la main et était hachée en cours de route. Un outil concept→argile existe maintenant et sa première paire a été testée à pleine échelle : pose, bracelets, médaillon de ceinture et ourlet déchiré ont tous été pris en compte ; la masse de crinière n’a pas été prise en compte ; une fuite de couleur mesurée sur toute l’image **C\* p99.9 = 13.15** avec un fond parfaitement achromatique. **Ce que cette paire ne peut pas montrer, c’est si le maillage revient meilleur**, ce qui est la seule question qui permettrait de le promouvoir, il reste donc un candidat avec ses preuves enregistrées : **[préparation du concept](docs/concept-prep.md)**.

## Ce qui fait que cela fonctionne

Six observations, chacune nécessitant une expérimentation et chacune ayant une portée plus large que le sujet qui l’a générée. [La version complète, avec les mesures](docs/findings.md).

- **Privilégiez la forme, puis le style.** Les outils de reconstruction interprètent le bruit de surface comme de la géométrie. Une argile propre et sculpturale, avec des plans délibérément exagérés, donne un meilleur résultat en termes de topologie qu’un sprite stylisé ; le jumeau stylisé est généré simultanément et sert de référence pour les couleurs.
- **Définissez le visage, obtenez un visage.** Un cadrage du buste ajoute **3,1 à 4,5 fois** plus de polygones sur la tête, et la différence est structurelle : paupières séparées, sillon frontal, cavités nasales modélisées – ce n’est pas simplement un flou plus net.
- **Les jumeaux appartiennent à une maille, et non à un personnage.** Réutilisez un jumeau sur différentes mailles et la couverture diminue de **62 % à 22,7 %**, car les bras se projettent dans l’espace vide à côté du modèle. Générez des jumeaux à partir de la maille que vous allez texturer, à chaque fois.
- **L’identité appartient à l’invite.** Un élément canonique non mentionné dans l’invite apparaît par erreur et disparaîtra de la même manière : cela a été mesuré lorsque les plaques dorées aux genoux se sont avérées n’apparaître que grâce au bruit dans un ControlNet défectueux.
- **Demandez à la géométrie, pas à un seuil.** Le remplacement d’un masque clé par le contour exact obtenu par lancer de rayons a amélioré la couverture de référence de **28,4 % à 39,1 %** des texels valides – uniquement additif, sans diffusion, sans GPU. La technique de masquage basée sur les coins et la médiane a échoué trois fois ici et est abandonnée.
- **Supprimez ce qu’aucune caméra ne peut voir, à partir de l’atlas et jamais de la maille.** 49 % des texels de l’atlas sont invisibles de l’extérieur ; en excluant ces faces, on réduit l’interpolation de 68 %. Plutôt que de supprimer, il est préférable d’exclure, ce qui rend l’échec impossible au lieu de simplement détectable.

## Ce qui n’est pas résolu

Identifié et mesuré, sur la page d’accueil plutôt que dans une note de bas de page. [Tous, situés dans le code](docs/known-defects.md).

- **Certaines zones de surface visibles sont mappées à l'espace de l'atlas, mais aucune n'est jamais écrite lors du processus de « bake »**, et elles apparaissent comme le noir par défaut non modifié de l’image. Le moteur de « baking » de Blender utilise un échantillonnage au centre des texels, donc un triangle qui ne chevauche aucun centre de texel reste vide — ses propres développeurs
[ont nommé ce mécanisme et ont intégré une correction](https://projects.blender.org/blender/blender/pulls/161752)
deux semaines après la version sur laquelle tous les chiffres ici ont été mesurés. Il s’agit d’une propriété de la trajectoire,
et non d’un seul objet : mesuré sur un actif, **non mesuré sur les quatre autres**.
- **La bande de texture prend 0,00 % de la référence de l’étape 1** sur toutes les huit caméras — l’acier sur un fond gris se trouve exactement au seuil du modèle. L’union sauve 55,72 %.
- **Les joints des textures ne sont pas uniformisés.** Une limite de provenance présente une variation de texture ordinaire de **5,5×** ; la région que le Directeur a nommée présente une variation de **9,5×**.
- **La dilatation se propage entre les îles d’atlas non liées** — 74,9 % des texels dilatés tirent leur couleur d’une autre île, avec une distance médiane de 0,177 sur une figure de hauteur 1,0. ⚠ **Cette part concerne les texels de l’atlas et ne constitue pas une affirmation sur ce qu’une caméra voit :** la dilatation représente 26,95 % de l’atlas généré et **4,95 % des pixels rendus de la figure**, soit un rapport de 0,18×. La peinture se trouve dans les grandes cartes, les trous se trouvent dans les petites, donc un texel dilaté est peu coûteux en termes d’espace à l’écran.
- **⚑ Le défaut qui détermine l’acceptation est porté par la PEINTURE, et non par aucun remplissage** — régions affichant la couleur d’un autre matériau, ce que aucune statistique de « speckle » ne peut détecter. Mesuré de trois manières différentes sur trois sessions dans trois espaces : **91,05 % `reference`, avec un enrichissement de 0,99×**, correspondant parfaitement au taux de base ; la même classe en vert « cloth » **68,46 % `reference`** ; et sur une fine bande, les propres texels peints de la surface **18,77 %** sont contaminés par rapport à son remplissage de dilatation de **5,55 %**.
Le remplissage provient correctement de son voisin peint le plus proche — et ce voisin est déjà incorrect. Le mélange lui-même est une division en deux bandes non documentée
(`M + gaussian_blur_σ16(B − M)`) qui mesure la **pire des quatre** alternatives sur les mêmes points.
- **Les vues ne sont jamais indépendantes, ce qui limite toute correction de mélange.** Pour chaque groupe de défauts,
**100 % des faces avec deux caméras ou plus contribuant ont toutes ces caméras à l’intérieur d’un angle de 90°**
(médiane de 45°), et 21 % des faces défectueuses sont vues par une seule caméra. Les vues adjacentes soumises à un contrôle presque identique échouent ensemble, de sorte que les gains multi-vues publiés de la photogrammétrie ne se traduisent pas directement ici.
- **Chaque reconstruction sur cette trajectoire est une coquille creuse à double paroi**, avec des parois d’environ deux voxels. Aucune condition volumétrique n’est valide pour l’un d’eux.
- **Les plaques divergent au niveau des limites de matériaux non nommées, et le modèle est la clé**
(2026-08-16). La déformation intérieure « twin-to-mesh » mesurée a une médiane de **3,5 à 11,1 px** sur les huit vues, par rapport aux médianes de silhouette de 1,2 à 3,0 ; chaque région résiduelle que le Directeur a encerclée — coupe de manche, main, dessus de botte — est un joint de matériau que l’invite de génération n’a jamais nommé. ⚠ **CORRIGÉ le 2026-08-17, et la correction affine les résultats.** Il était écrit : « l’invite enregistrée contient six éléments » — mesuré, ce qui fusionne deux fichiers différents. Le flux de travail qui a généré les « twins » nomme **16 des 17**, ne manquant que la prise ; le *profil par défaut du pinceau* en nomme six. Les deux sont vrais, et la phrase contenait une seule affirmation fausse parmi celles-ci. Ce qui est important et persiste : la prise, le bracelet et le protège-jambe apparaissent **zéro** fois dans l’invite de 16 phrases — car **aucun élément pour eux n’existe dans le modèle**. Une invite complète ne peut toujours pas nommer une main qui n’a jamais été spécifiée.
✅ **FERMÉ le 2026-08-17** — la liste des surfaces est parcourue, remplie et **24/24 validée**, et la porte refuse désormais une invite qui ne la couvre pas.
- **4,65 à 5,57 % des texels valides sont des surfaces qu’aucune caméra à anneau plat ne peut voir** — ils échouent au niveau du filtre de profondeur dans toutes les vues, aucune trajectoire de projection ne peut les peindre, et le pipeline livré les a recouverts avec un remplissage aveugle aux îles qui a créé les marques sombres. Ils ont besoin d’une politique (matériau neutre, pinceau ou acceptation), pas d’une correction
([rapport E49](docs/experiments/E49-finish-and-cap-report.md)).
- **Polygones colorés plats sur les feuilles de qualité acceptée** — la seule classe ouverte du Directeur.
⚠ **L’hypothèse du « fill-pass » est RÉFUTÉE (2026-08-17).** Le remplissage orphelin mesure *en dessous* de son propre taux de base au niveau du défaut (0,27x), les correctifs se trouvent à 90 à 99 % sur des texels peints ordinaires, et le même défaut est présent dans un rendu construit à partir d’un atlas qui précède la correction dont il est accusé. Il a plutôt été retracé jusqu’à sa source : le « twin » de la vue de rendu est propre à cet endroit, et une **vue différente** possède 97 des 115 pixels défectueux avec un angle de 0,68 par rapport à 0,60. Le correctif angulaire est un **artefact de diffusion**, et la couleur est une réelle divergence entre les vues sur une surface qui a déjà été nommée — donc une régénération « twin » n’est pas justifiée par le fait que « le défaut se trouve dans les « twins » ».
⚠ **Et la correction que cette page proposait est également RÉFUTÉE (2026-08-17).** Il était écrit : « un compositeur préférant la vue cible est la correction à portée et ne coûte rien. » Le compositeur existait déjà et était déjà le paramètre par défaut ; mesuré par rapport au classificateur plat sur les images fixes d’une seule exécution enregistrée, en privilégiant la vue cible, cela **augmente** le nombre de la cible nommée (38 → 40) et l’augmente considérablement dans deux autres (23 → 64, 36 → 110), devenant *plus* cohérent. Le mécanisme : **la forme est une propriété, la couleur ne l’est pas.** L’olive est la propre peinture de la vue 6 d’une surface que la vue 6 peint correctement, donc à la cible 6 — où « privilégier la vue 6 » signifie *préférer la vue 6* — la politique maximise exactement la peinture dont le défaut est constitué. **Une politique de propriété ne peut pas corriger une divergence de couleur entre les vues sur une surface correctement attribuée**, ce qui abandonne l’ensemble plutôt qu’un seul bras ([E52](docs/experiments/E52-target-first-flats-ruling.md)). Il reste une question de peinture, et cela coûte une génération. *Texte remplacé, conservé conformément à la règle des corrections : « îles orphelines de la taille de simples triangles, remplies à plat à partir d’échantillons adjacents du « twin » pris avec la silhouette non érodée. »

## Comment ce dépôt est-il géré ?

La discipline est autant un produit qu’un processus, et elle existe pour une raison : une série précédente comprenait dix sessions au cours desquelles chaque participant évaluait son propre travail et rédigeait des conclusions que la session suivante prenait comme acquis. Rien dans cette boucle n’était vérifiable.

- **Définir les spécifications avant le travail, faire un rapport après, trancher en dernier** — et la session qui conçoit une expérience n’évalue jamais ses propres résultats. Cinquante-six expériences sont disponibles dans [les archives](docs/experiments/).
- **Les corrections sont appliquées sur place, à côté de la mesure qui les a invalidées**, et non sous forme de suppressions discrètes. Six affirmations initiales ont été réfutées lors de la première session, et les six sont toujours accessibles à côté de ce qui les a remplacées.
- **Les échecs restent dans le dépôt avec leur raison.** [`tools/superseded/`](docs/tools.md) n’est pas une archive — chacun peut exécuter ces outils et observer qu’ils échouent de la même manière.
- **Un résultat négatif est un succès total**, qui est signalé et clôturé plutôt que d’être ajusté pour atteindre une valeur cible.
- **Les tests sont liés au commit qui modifie le code** — 1 339 tests réussis, évalués par deux personnes, avec des contrôles CI basés sur les chemins pour les 1 285 tests hermétiques.
- **Les archives peuvent être interrogées.** Un index SQLite + FTS5 couvre l’ensemble du processus, et a été vérifié à quatre reprises. Il a identifié un nombre de résultats que le texte avait mal indiqué à trois endroits, en comptant les enregistrements eux-mêmes.

## Où tout est…

| | |
|---|---|
| **[Le manuel](docs/handbook/index.md)** | le guide — le déroulement étape par étape, les sujets, le système de profilage |
| **[Préparation du concept](docs/concept-prep.md)** | l’étape candidate de préparation des modèles : son parcours d’évaluation initiale (Gate 0), son placement et l’élément de licence qu’elle ouvre |
| **[Les archives](docs/experiments/)** | cinquante-six expériences : spécifications, rapport, conclusions et chaque prédiction formulée avant la mesure |
| **[Ce que le processus a appris](docs/findings.md)** | les résultats durables et les règles obtenues de haute lutte, en intégralité |
| **[État de chaque outil](docs/tools.md)** | ce qui fonctionne, ce qui est obsolète et les preuves pour chacun |
| **[Défauts connus](docs/known-defects.md)** | tout ce qui n’a pas été résolu, mesuré et localisé dans le code |
| **[Le déroulement du processus, tel qu’il s’est produit](docs/arc-history.md)** | l’historique chronologique, avec les corrections intactes |
| **[CLAUDE.md](CLAUDE.md)** | comment travailler ici — les rôles, les règles et ce que chacun implique |

## Position concernant la licence

Chaque étape s’exécute localement et est conforme aux exigences commerciales : SDXL (OpenRAIL++), MV-Adapter (open source), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Exclusion délibérée, avec la justification : **nvdiffrast** (non commercial — appliqué ici par un mécanisme de sécurité structurel, et non par une attestation), **Hunyuan3D-Paint** (licence invalide dans l’UE, au Royaume-Uni et en Corée du Sud), **MVPaint** et **TEXGen** (aucune licence) et **UltraSharp / SUPIR / StableSR** (algorithmes d’amélioration non commerciaux).

**La limite de la revendication est définie plutôt que laissée à la découverte.** Elle décrit le **processus enregistré** — les étapes du diagramme ci-dessus, de l’image vers la 3D. L’étape candidate de préparation des modèles en amont exécute actuellement une API cloud fermée dont les conditions d’utilisation n’ont pas été vérifiées par ce dépôt, de sorte qu’aucune revendication de licence ici ne couvre un élément créé à partir de l’un de ses modèles. Il s’agit d’un point ouvert avec un chemin défini pour le résoudre : le modèle local conforme aux exigences de licence est **Qwen-Image-Edit (Apache-2.0)**, et **FLUX.1-Kontext [dev] est exclu pour les mêmes raisons que nvdiffrast** — pondérations non commerciales. Les deux ont été vérifiés par rapport au catalogue de modèles du studio plutôt qu’ils ont été rappelés ; la justification se trouve dans [la préparation du concept](docs/concept-prep.md).

## Modèle de confiance et de menace

l’exécution se fait entièrement sur votre propre machine — chaque outil est un script que vous exécutez sur des chemins que vous tapez, la question pertinente n’est donc pas *quelles sont les autorisations demandées par cette application*, mais *que font ces scripts sur votre machine*. La réponse est fournie par la mesure, et chaque cycle peut être réexécuté ; la politique complète se trouve dans [SECURITY.md](SECURITY.md) :

- **Données concernées :** maillages, textures, images et fichiers JSON sur le disque local, aux chemins que vous indiquez dans la ligne de commande. De plus, `docs/index/facet.db`, qui est *dérivé* — il ne contient rien qui n’était pas déjà un fichier dans ce dépôt, et `facet_index.py build` le régénère à partir de zéro.
- **Données NON concernées :** aucune information d’identification, jamais. Rien ici ne lit, ne stocke ou ne transmet de jeton, de clé ou de mot de passe, et rien de tel n’est présent dans l’arborescence — recherche effectuée pour les clés préfixées par le fournisseur, les GitHub PAT, les jetons Slack, les ID de clé AWS, les blocs de clé privée, les jetons d’authentification et les affectations en ligne `api_key`/`password`, **zéro correspondance**, aucun fichier ressemblant à une information d’identification suivi.
- **Pas de télémétrie.** Rien n’est collecté ni envoyé. Il n’y a pas d’option de désactivation car il n’y a rien à désactiver.
- **Échange réseau :** deux outils ouvrent un socket — `restylize_views.py` et `texpass_brush.py` — et les deux appellent une API HTTP ComfyUI à l’adresse `--host`, **par défaut `127.0.0.1:8188`**. Rien d’autre dans `tools/` n’effectue d’appel réseau.
- **Autorisations :** utilisateur ordinaire. Pas d’élévation de privilèges, pas d’installation de service, pas d’écriture dans les paramètres système ou le registre.

Trois arêtes vives sont révélées plutôt que niées, car une note de sécurité qui ne contient que des assurances n’est pas un modèle de menace : les opérations sur les fichiers ne sont pas exécutées dans un environnement isolé (un outil écrit partout où ses arguments l’indiquent) ; les chemins locaux absolus sont intégrés à de nombreux outils et documents — 114 occurrences dans 26 fichiers, ce ne sont pas des secrets mais la divulgation de la configuration d’une machine, et la raison pour laquelle la plupart des outils ne fonctionneront pas sans modification ailleurs ; et les échecs inattendus se manifestent sous forme de traces Python dans les scripts de recherche non publiés, sans `--debug`. Les arrêts intentionnels sont des messages `ANDON:` qui contiennent la mesure qui les a déclenchés. C’est le contrat de l’instrument de recherche, et [SHIP_GATE.md](SHIP_GATE.md) enregistre exactement quand il cesse d’être suffisant — ce qui est le cas pour les deux commandes dont il gère l’installation, à la version 0.2.0 : `facet-index` et `facet-mcp` renvoient `0` (OK) / `1` (erreur utilisateur) / `2` (erreur d’exécution), et, depuis [E22](docs/experiments/E22-ruling.md), `4` est REFUSÉ pour un déclencheur activé ou une branche défaillante `verify`, ce qui signifie que l’outil fonctionne et vous indique de ne pas continuer plutôt qu’il s’agisse d’une erreur d’exécution. Tous les éléments refusent avec une erreur structurée indiquant l’étape suivante au lieu d’une trace ([E21](docs/experiments/E21-cli-contract-report.md)).

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

**État du support :** ce dépôt est développé en mode ouvert, sur une seule plateforme, par un seul responsable et une paire rotative de sessions de conseil et d’exécution. `main` est le seul état pris en charge. Il n’y a pas de canal de publication, pas de politique de rétroportage et pas de SLA : ce qu’il y a à la place, c’est l’enregistrement : chaque affirmation se trouve à côté du code qui la produit, et [docs/experiments](docs/experiments/) contient les spécifications, le rapport et la décision pour chacun.

## Exigences

Blender 5.x, Python 3.11+ avec `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Une installation locale de ComfyUI n’est nécessaire que pour le pinceau d’inpainting. Développé sur une RTX 5090 ; la marge de VRAM est plus importante que la vitesse brute.

CI exécute le sous-ensemble hermétique de la suite sur ubuntu-latest / Python 3.12 avec des installations fixes (`.github/workflows/ci.yml`) ; la couche d’artefacts a besoin des arbres enregistrés sous `E:\AI\training`, qui ne sont pas dans git, donc CI les désélectionne par conception. Localement, `python -m pytest` exécute les 1 339 tests et `python -m pytest -m "not artifacts"` exécute les 1 285 tests reproduits par CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
