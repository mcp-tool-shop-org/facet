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

Le style est appliqué **sur l’élément**, dans l’espace de texture, et non pas peint pour chaque vue puis assemblé par la suite. Fournissez à la chaîne un concept d’argile aux formes exagérées, et elle renverra une maille texturée dont la couleur provient d’une référence stylisée de *cette* maille, avec tout ce que la référence ne pouvait pas voir, comblé par un pinceau de retouche masqué et une dilatation tenant compte de la surface.

Nommé en fonction des deux aspects du problème : les polygones et la face qu’ils doivent représenter.

## Installation

La chaîne elle-même est un ensemble de scripts locaux que vous exécutez sur des chemins que vous tapez : clonez le dépôt et lisez [comment démarrer](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Deux serveurs sont fournis dans un seul package** : l’index des enregistrements, afin qu’un assistant puisse interroger la trace des preuves au lieu de la lire, et **à partir de la version 0.4.0, le serveur de mesure**, afin que deux éléments mesurés à plusieurs mois d’intervalle passent par un seul chemin de code.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` est le serveur MCP stdio qui traite les enregistrements (six outils, dont la vérification à quatre points servant de surface de santé qui refuse), et `facet-index` est l’index lui-même (`build` / `verify` / `q` / `claims`). Exécutez l’un ou l’autre depuis un répertoire extrait ; `--db` désigne un index différent.

### Le serveur de mesure, nouveauté dans la version 0.4.0

`facet-measure` répond à la **partie numérique** d’une comparaison et n’indique jamais si le résultat est bon. Chaque charge utile contient la version du serveur, le hachage du fichier de l’instrument et un hachage de configuration, et `measure_report` **refuse** de comparer des éléments qui ne correspondent pas, ce qui est précisément la raison d’être de tout cela.

Vérifié en exécutant une **commande** plutôt que `--help` : une maille de contrôle renvoie 786 432 faces avec un enveloppe d’identité complète sur une machine qui ne contient pas de répertoire extrait.

**Ce que vous obtenez dépend d’une seule chose, et c’est votre version de Python :**

| votre Python | `[measure-full]` vous donne |
|---|---|
| **3.11 / 3.12** | **les huit outils** : `open3d` s’installe à partir de PyPI |
| **3.13** | quatre outils : `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 est la dernière *version* et publie des roues cp38–cp312 **sans sdist**, de sorte que sur 3.13, il n’y a rien à installer sur PyPI. L’élément supplémentaire le fournit en arrière-plan via `python_version < "3.13"`, de sorte que l’installation **réussie** et les quatre outils de géométrie renvoient **`4` REFUSÉ**, indiquant ce dont ils ont besoin, plutôt que l’échec complet de l’installation.

**Pour obtenir les huit sur Python 3.13**, Open3D publie des roues cp313 actuelles sur son canal de développement continu. Une URL directe est acceptable dans une ligne de commande ; elle n’est interdite que dans les métadonnées du package publié :

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **Sur Windows et macOS, les roues de développement sont suffixées par `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` au moment de la rédaction), et le nom change lorsque `main` change. Listez les éléments sur [la version `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) et prenez la version actuelle. **C’est avec cette version que les nombres de cette chaîne, qui dépendent d’Open3D, ont été mesurés**, et c’est une véritable limite de comparabilité : l’enveloppe d’identité enregistre le hachage de l’instrument, et non ses dépendances — [E31](docs/experiments/E31-ruling.md).

*Jusqu’à la version 0.3.1, la roue contenait deux fichiers `.py` et aucun des instruments de mesure, de sorte qu’un serveur de mesure installé n’avait rien à exécuter. Personne ne l’a remarqué pendant quatre versions parce que ce dépôt EST le répertoire extrait : l’outil fonctionnait là où il était construit et n’avait jamais été ailleurs.*

⚠ **`pip install facet-mcp` était défectueux dans toutes les versions publiées jusqu’à la version 0.3.0, et est corrigé dans la version 0.3.1.** La roue installe `facet_index` en tant que module de niveau supérieur, de sorte que jusqu’à et y compris la version 0.3.0, elle résolvait l’emplacement de l’enregistrement par rapport à `<venv>/Lib`, qui ne contient ni corpus ni index, et `build`, `claims` et `q` sans `--db` échouaient tous. **Pour la version 0.3.0 ou antérieure, utilisez le binaire `npx` ci-dessus.**

À partir de la version 0.3.1, la racine est résolue en **vérifiant l’existence de l’enregistrement** plutôt qu’en supposant son existence : exécutez l’une ou l’autre commande depuis un répertoire extrait et elle le trouvera ; exécutez-la depuis n’importe quel autre endroit et elle renverra **`4` REFUSÉ**, en indiquant les deux répertoires qu’elle a essayés et les deux marqueurs qu’elle a recherchés. `$FACET_INDEX_DB` est maintenant lu par les deux commandes, et il sélectionne l’*index*, jamais le *corpus*. Mesuré sur une roue construite à partir de `main` et installée dans un environnement virtuel propre — [E24](docs/experiments/E24-ruling.md).

*Ce bloc a été corrigé deux fois. Il indiquait d’abord `pipx install facet-mcp # ou le package Python directement `, until v0.3.0's read-back ran a **verb** instead of ` --help`. Ensuite, il affirmait que la roue « ne fonctionne que pour `q` et `claims` » — **`claims` ne fonctionnait pas non plus**, ce que E24 a découvert en l’exécutant. Les deux corrections se trouvent dans [known-defects.md](docs/known-defects.md) avec leurs mesures.*

## Où cela en est

**Quatre éléments acceptés, répartis sur quatre classes de sujets, pour zéro crédit.** Chacun a été validé par le directeur à son propre niveau de zoom : sur le fichier GLB ou sur des feuilles de taille réelle, et non pas par une métrique qui dépasse un seuil.

| sujet | classe | accepté | référence / pinceau / dilatation |
|---|---|---|---|
| **Character (W3)** | humanoïde | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | véhicule, gréement fin | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bête, membranes des ailes | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | accessoire, presque 2D, gris sur gris | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Les parts sont constituées de texels valides, et **elles ne sont pas comparables entre les sujets** : un navire cache la majeure partie de lui-même vue au niveau des yeux et un animal en cache la moitié. Évaluez chaque élément par rapport à son propre plafond d’étendue préenregistré, par rapport auquel ils atteignent **86 à 93 %** : la différence entre les lignes est la géométrie, et non une régression. [Nombres complets, avec leurs dénominateurs](docs/handbook/subjects.md).

**Il s’agit d’un pipeline, et non d’un générateur à un seul caractère.** Contredisez les spécifications sur huit éléments nommés et la requête remporte **8 sur 8** : ΔE médian de 46,3 contre 6,2 sur cinq contrôles maintenus, tandis que la figure reste le même homme. La structure est assurée par la maille et le contrôle ; les attributs nommés sont liés à la requête.

**La question concernant le projecteur a étéClose le 2026-08-16** ([E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
Les huit plaques **composent**: reconstruites à partir de l’ensemble par vue, en utilisant les
poids de bordure × orientation × visibilité, l’atlas rend le résultat tel que le directeur l’a jugé *"nettement meilleur"* et ensuite *"très réussi" — contrairement à un atlas déjà utilisé dont la méthode avait
tendance à abîmer la peinture. Les plaques sont d’accord sur ce point. La chaîne qui a permis cela se trouve dans `tools/`
(`emit_view_aovs`, `s3_composite`, `flow_estimate`, `s3_run`, `s3_sheet`,
`atlas_from_aovs`, `twin_mesh_warp`), dont cinq des sept ont été créées par un canal externe
dont les revendications de calibration nominatives se sont avérées **valides dans tous les cas**, chacune ayant été vérifiée ici
avant d’être approuvée. Ce qui reste est indiqué ci-dessous, et non caché : une classe de polygones pour le remplissage en cours
d’étude, une surface inédite en attente d’une politique, et la construction canonique que
le directeur a qualifiée d’élément essentiel.

## Le trajet

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

Étape par étape, avec le raisonnement pour chaque étape : **[le manuel](docs/handbook/index.md)**.

**Le saut en pointillés est nouveau et n’est pas intentionnellement continu.** La première boîte du trajet affichait toujours
*concept d’argile*, et jusqu’à présent, rien ici ne le rendait possible : chaque argile était créée à la main et
modifiée au fur et à mesure. Un outil concept→argile existe désormais et sa première paire a été testée
à taille réelle : pose, bracelets, médaillon de ceinture et ourlet déchiré, tous intégrés ; la masse de crinière n’a pas été incluse ; le déversement de couleur mesuré sur l’ensemble de l’image est de **C\* p99.9 = 13.15** avec un arrière-plan achromatique uniforme. **Ce que cette paire ne peut pas montrer, c’est si la maille s’améliore**, ce qui est
la seule question qui justifie son utilisation, elle reste donc une candidate dont les preuves sont enregistrées :
**[préparation du concept](docs/concept-prep.md)**.

## Ce qui le rend efficace

Six découvertes, chacune ayant nécessité une expérience et chacune s’appliquant au-delà
du sujet qui l’a produite. [La version longue, avec les
mesures](docs/findings.md).

- **D’abord la forme, puis le style.** Les outils de reconstruction interprètent le bruit de surface comme une géométrie. Une argile propre, semblable à une sculpture et dotée de plans délibérément exagérés, donne un résultat avec une meilleure topologie
que celle d’un sprite stylisé ; le jumeau stylisé est généré en parallèle et devient la
référence de couleur.
- **Encadrez le visage, obtenez un visage.** Un recadrage du buste place **3,1 à 4,5 fois** plus de polygones sur
la tête, et la différence est structurelle : paupières séparées, sillon frontal, cavités des narines modélisées — pas seulement un flou plus prononcé.
- **Les jumeaux appartiennent à une maille, et non à un personnage.** Réutilisez un jumeau sur différentes mailles et la couverture diminue de **62 % à 22,7 %**, car les bras se projettent dans l’espace vide à côté du modèle.
Générez des jumeaux à partir de la maille que vous allez texturer, à chaque fois.
- **L’identité appartient à l’invite.** Un élément canonique non mentionné dans l’invite apparaît
par hasard et disparaîtra de la même manière : cela a été mesuré lorsque les plaques dorées des genoux se sont avérées
n’apparaître que par le biais du bruit dans un ControlNet défectueux.
- **Demandez à la géométrie, pas à un seuil.** Le remplacement d’un masque clé par la silhouette exacte du lancer de rayons a amélioré la couverture de référence de **28,4 % à 39,1 %** des texels valides — uniquement additive, sans diffusion, sans GPU. La technique de masquage basée sur la médiane des coins a échoué trois fois ici et est abandonnée.
- **Supprimez ce qu’aucune caméra ne peut voir, de l’atlas et jamais de la maille.** 49 % des texels de l’atlas
sont invisibles depuis l’extérieur ; l’exclusion de ces faces réduit l’interpolation de **68 %**. L’exclusion plutôt que la suppression rend l’échec impossible au lieu d’être simplement détectable.

## Ce qui n’est pas résolu

Nommé et mesuré, sur la première page plutôt que dans une note de bas de page. [Tous, situés dans le code](docs/known-defects.md).

- **Certaines parties visibles de la surface sont mappées sur l'espace de l'atlas, mais aucune n'est jamais écrite lors du processus de « bake »**, et elles s'affichent comme le noir par défaut non modifié de l'image. Le système de « baking » de Blender utilise un échantillonnage au centre des texels, donc un triangle qui ne chevauche aucun centre de texel reste vide — ses propres développeurs
[ont nommé ce mécanisme et ont intégré une correction](https://projects.blender.org/blender/blender/pulls/161752)
deux semaines après la version sur laquelle toutes les mesures ici ont été effectuées. Il s'agit d'une propriété de la séquence,
et non d'un élément spécifique : mesurée sur un actif, **non mesurée sur les quatre autres**.
- **La bande de lame représente 0,00 % de la référence de l'étape 1** sur les huit caméras — l'acier sur un fond gris se trouve exactement au seuil défini. La combinaison permet d'obtenir 55,72 %.
- **Les joints des textures ne sont pas uniformisés.** Une limite de provenance présente une variation de texture ordinaire de **5,5×** ; la région que le directeur a nommée présente une variation de **9,5×**.
- **La dilatation se propage entre les îles de l'atlas non liées** — 74,9 % des texels dilatés tirent leur couleur d'une autre île, avec une distance médiane de 0,177 sur une figure de hauteur 1,0. ⚠ **Cette part concerne les texels de l'atlas et ne représente pas ce qu'une caméra voit** : la dilatation représente 26,95 % de l'atlas généré et **4,95 % des pixels rendus de la figure**, soit un rapport de 0,18×. Les textures se trouvent sur de grandes cartes, les trous sur de petites, donc un texel dilaté est peu coûteux en termes d'espace d'affichage.
- **⚑ Le défaut qui détermine l'acceptation est lié à la PEINTURE, et non à aucun remplissage** — régions affichant la couleur d'un autre matériau, ce que aucune statistique de « speckle » ne peut détecter. Mesuré de trois manières différentes lors de trois sessions dans trois espaces différents : **91,05 % `reference`, avec un enrichissement de 0,99×**, correspondant parfaitement au taux de base ; la même classe en vert « tissu » représente **68,46 % `reference`** ; et sur une fine lame, les propres texels peints de la surface représentent **18,77 %**, contre 5,55 % pour le remplissage de dilatation.
Le remplissage provient correctement du voisin peint le plus proche — et ce voisin est déjà incorrect. Le mélange lui-même est une division à deux bandes non documentée
(`M + gaussian_blur_σ16(B − M)`) qui mesure **la pire des quatre** alternatives sur les mêmes points.
- **Les vues ne sont jamais indépendantes, ce qui limite toute correction de mélange.** Pour chaque groupe de défauts,
**100 % des faces avec deux caméras ou plus ont toutes ces caméras à l'intérieur d'un angle de 90°**
(médiane de 45°), et 21 % des faces défectueuses sont vues par une seule caméra. Les vues adjacentes soumises à un contrôle presque identique échouent ensemble, de sorte que les gains multi-vues publiés de la photogrammétrie ne se traduisent pas directement ici.
- **Chaque reconstruction dans cette séquence est une coquille creuse à double paroi**, avec des parois d'environ deux voxels. Aucune condition volumétrique n'est valide pour l'un ou l'autre.
- **Les plaques divergent aux limites de matériaux non nommés, et le canon est la clé**
(16 août 2026). La déformation intérieure « jumeau vers maillage » mesurée a donné une valeur comprise entre **3,5 et 11,1 px en médiane** sur les huit vues, par rapport aux médianes de silhouette comprises entre 1,2 et 3,0 ; chaque région résiduelle que le directeur a encerclée — coupe de manche, main, dessus de botte — est un joint de matériau que l'invite de génération n'a jamais nommé (l'invite enregistrée contient six éléments ; la prise, le brassard, le jambier et
la main apparaissent **zéro** fois). Son diagnostic est celui du dossier : « nous n'avons pas correctement développé le canon. » Le développement du canon W3 et la régénération alimentée par le canon sont
la réparation en plusieurs étapes ([enregistrement de l'expédition E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
- **Entre 4,65 % et 5,57 % des texels valides représentent une surface qu'aucune caméra à anneau plat ne peut voir** — ils échouent au niveau du filtre de profondeur dans toutes les vues, aucune route de projection ne peut les peindre, et la chaîne de traitement fournie a utilisé un remplissage aveugle aux îles qui a créé les marques sombres. Ils ont besoin d'une politique (matériau neutre, pinceau ou acceptation), pas d'une correction
([rapport E49](docs/experiments/E49-finish-and-cap-report.md)).
- **Le passage de remplissage « candidat complet » rend des polygones colorés plats** — la seule classe ouverte du directeur sur les feuilles de qualité acceptée (« ça a l'air bien, mais il y a des formes polygonales colorées »). Hypothèse en cours de test, masques de provenance déjà étiquetés : îles orphelines de la taille de triangles uniques, remplies à plat à partir d'échantillons jumeaux adjacents à la limite, pris avec la silhouette non érodée.

## Comment ce dépôt est géré

La discipline est aussi importante que le produit lui-même et qu'il existe une raison : une séquence antérieure a comporté dix sessions qui ont chacune évalué leur propre résultat et rédigé des conclusions que la session suivante a lues comme un fait établi. Rien dans cette boucle n'était vérifiable.

- **Spécifications avant le travail, rapport après, décision finale** — et la session qui conçoit une expérience n'évalue jamais ses propres résultats. Quarante-quatre expériences sont disponibles dans
[le dossier](docs/experiments/).
- **Les corrections sont appliquées en place, à côté de la mesure qui les a invalidées**, et non sous forme de suppressions discrètes. Six affirmations héritées ont été réfutées lors de la session initiale, et les six sont toujours lisibles à côté de ce qui les a remplacées.
- **Les échecs restent dans le dépôt avec leur raison.** [`tools/superseded/`](docs/tools.md)
n'est pas un archive — n'importe qui peut exécuter ces outils et observer qu'ils échouent de la même manière.
- **Un résultat négatif est un succès total**, rapporté et clôturé plutôt que modifié pour atteindre une valeur cible.
- **Les tests sont liés au commit qui touche le code** — 1 223 tests réussis, évalués par deux personnes, avec des CI à accès limité sur les 1 173 tests hermétiques.
- **Le dossier est interrogeable.** Un index SQLite + FTS5 sur l'ensemble de la séquence, vérifié sur quatre systèmes. Il a trouvé un nombre de décisions que le texte avait mal indiqué à trois endroits différents en comptant le dossier lui-même.

## Où tout se trouve

| | |
|---|---|
| **[Le manuel](docs/handbook/index.md)** | le guide — la séquence étape par étape, les sujets, le système de profil |
| **[Préparation du concept](docs/concept-prep.md)** | l'étape candidate « clay hop » : son parcours à l'étape 0, son placement et l'élément de licence qu'il ouvre |
| **[Le dossier](docs/experiments/)** | quarante-quatre expériences : spécifications, rapport, décision et chaque prédiction énoncée avant la mesure |
| **[Ce que la séquence a appris](docs/findings.md)** | les conclusions durables et les règles difficiles à obtenir, dans leur intégralité |
| **[État de chaque outil](docs/tools.md)** | ce qui fonctionne, ce qui est obsolète et les preuves pour chacun |
| **[Défauts connus](docs/known-defects.md)** | tout ce qui n’est pas résolu, mesuré et localisé dans le code |
| **[Le déroulement, tel qu’il s’est produit](docs/arc-history.md)** | l’historique chronologique, avec les corrections intactes |
| **[CLAUDE.md](CLAUDE.md)** | comment travailler ici : les rôles, les règles et ce que chacun implique |

## Position concernant la licence

Chaque étape s’exécute localement et est conforme aux exigences commerciales : SDXL (OpenRAIL++), MV-Adapter (open), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Exclusion délibérée, avec la justification : **nvdiffrast** (non commercial — appliqué ici par un mécanisme de sécurité structurel, et non par une attestation), **Hunyuan3D-Paint** (licence invalide dans l’UE, au Royaume-Uni et en Corée du Sud), **MVPaint** et **TEXGen** (aucune licence) et **UltraSharp / SUPIR / StableSR** (algorithmes d’amélioration non commerciaux).

**La limite de la revendication est définie plutôt que laissée à la découverte.** Elle décrit le **parcours enregistré** — les étapes du diagramme ci-dessus, à partir de l’image vers la 3D. L’étape candidate de préparation des modèles en amont s’exécute actuellement sur une API cloud fermée dont les conditions ce dépôt n’a pas vérifiées, de sorte qu’aucune revendication de licence ici ne couvre un élément créé à partir d’un de ses modèles. Il s’agit d’un point ouvert avec un chemin défini pour le résoudre : le modèle local conforme aux exigences de la licence est **Qwen-Image-Edit (Apache-2.0)**, et **FLUX.1-Kontext [dev] est exclu pour les mêmes raisons que nvdiffrast** — poids non commerciaux. Les deux ont été vérifiés par rapport au catalogue de modèles du studio plutôt qu’ils ont été rappelés ; la justification se trouve dans [la préparation des concepts](docs/concept-prep.md).

## Modèle de confiance et de menace

chaque facette s’exécute entièrement sur votre propre machine — chaque outil est un script que vous exécutez en utilisant les chemins que vous tapez, la question pertinente n’est donc pas *quelles sont les autorisations demandées par cette application*, mais *ce que font ces scripts sur votre machine*. La réponse est fournie par la mesure, et chaque cycle peut être répété ; la politique complète se trouve dans [SECURITY.md](SECURITY.md) :

- **Données concernées :** maillages, textures, images et JSON sur le disque local, aux chemins que vous spécifiez dans la ligne de commande. De plus, `docs/index/facet.db`, qui est *dérivé* — il ne contient rien qui n’était pas déjà un fichier dans ce dépôt, et `facet_index.py build` le régénère à partir de zéro.
- **Données NON concernées :** aucune information d’identification, jamais. Rien ici ne lit, ne stocke ou ne transmet de jeton, de clé ou de mot de passe, et rien de tel n’est présent dans l’arborescence — recherche effectuée pour les clés préfixées par le fournisseur, les PAT GitHub, les jetons Slack, les ID de clé AWS, les blocs de clé privée, les jetons porteurs et les affectations en ligne `api_key`/`password`, **zéro correspondance**, aucun fichier ressemblant à une information d’identification suivi.
- **Pas de télémétrie.** Aucune donnée n’est collectée ni envoyée. Il n’y a pas d’option de désactivation car il n’y a rien à désactiver.
- **Échange réseau :** deux des trente-six outils ouvrent un socket — `restylize_views.py` et `texpass_brush.py` — et les deux appellent une API HTTP ComfyUI à l’adresse `--host`, **par défaut `127.0.0.1:8188`**. Rien d’autre dans `tools/` n’effectue d’appel réseau.
- **Autorisations :** utilisateur ordinaire. Pas d’élévation de privilèges, pas d’installation de service, pas d’écriture dans les paramètres système ou le registre.

Trois points critiques sont divulgués plutôt que dissimulés, car une note de sécurité qui ne contient que des assurances n’est pas un modèle de menace : **les opérations sur les fichiers ne sont pas exécutées dans un environnement isolé** (un outil écrit à l’endroit indiqué par ses arguments) ; **des chemins locaux absolus sont intégrés dans de nombreux outils et documents** — 114 occurrences dans 26 fichiers, ce ne sont pas des secrets mais une divulgation de la disposition d’une machine, et c’est pourquoi la plupart des outils ne fonctionneront pas sans modification ailleurs ; et **les échecs inattendus se manifestent sous forme de traces Python dans les 36 scripts de recherche non publiés**, sans passerelle `--debug`. Les arrêts délibérés sont des messages `ANDON:` qui contiennent la mesure qui les a déclenchés. Il s’agit du contrat d’instrument de recherche, et [SHIP_GATE.md](SHIP_GATE.md) enregistre exactement le moment où il cesse d’être suffisant — ce qui était le cas pour les deux commandes que facet installe à la version 0.2.0 : `facet-index` et `facet-mcp` renvoient `0` OK / `1` erreur utilisateur / `2` erreur d’exécution — et, depuis [E22](docs/experiments/E22-ruling.md), **`4` REFUSÉ** pour une porte déclenchée ou une étape `verify` qui échoue, ce qui signifie que l’outil fonctionne et vous indique de ne pas continuer plutôt qu’une erreur d’exécution. Tous refusent avec un échec structuré indiquant la prochaine étape au lieu d’une trace ([E21](docs/experiments/E21-cli-contract-report.md)).

**Et les portes de ces deux commandes ne sont plus supprimables.** Chaque ANDON dans ce que facet installe est `raise` ; un simple `assert` est une instruction `python -O` qui se supprime silencieusement, et 87 des portes de ce dépôt pouvaient être supprimées par une variable d’environnement jusqu’à ce qu’E22 les convertisse. Mesuré avant et après sur la même porte, dans quatre modes interpréteur.
**Et depuis [E23](docs/experiments/E23-route-gates-report.md), les portes du parcours qui a produit les quatre éléments acceptés ne le sont plus non plus** — ses **57 sites répartis sur douze outils**, convertis en une simple modification de fichiers qu’aucun test n’a jamais exécutée, chacun refusant désormais sous `-O` et `PYTHONOPTIMIZE=1` ainsi que sous un interpréteur normal.
**Et depuis [E25](docs/experiments/E25-ruling.md), la classe est fermée.** Ses **133 sites répartis sur 43 fichiers** — les instruments de mesure qui ont produit les preuves des quatre éléments acceptés ci-dessus — se convertissent de la même manière, portant le total que `raise` à **278**.
Exactement **un** ANDON simple `assert` reste quelque part sous `tools/` : `superseded/texpass_thin_mask.py`, qui n’est **jamais** converti, car ces outils sont conservés afin que chacun puisse les exécuter et observer leur échec de la même manière. Ce reste est épinglé **par son nom** dans la suite de tests, de sorte qu’une analyse future ne puisse pas le supprimer sans modifier intentionnellement le test.

**État du support :** ce dépôt est développé en mode ouvert, sur une seule machine, par un seul responsable et une équipe de conseillers et d’exécutants qui se relaient. `main` est le seul état pris en charge. Il n’y a pas de canal de publication, pas de politique de rétroportage et pas d’accord de niveau de service (SLA). Ce qui existe à la place, c’est un registre : chaque demande est associée au code qui la génère, et [docs/experiments](docs/experiments/) contient les spécifications, le rapport et la décision pour chacune.

## Exigences

Blender 5.x, Python 3.11+ avec `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Une installation locale de ComfyUI n’est nécessaire que pour le pinceau de retouche. Développé sur une RTX 5090 ; la marge de VRAM est plus importante que la vitesse brute.

L’intégration continue (CI) exécute l’ensemble hermétique de la suite sur **ubuntu-latest / Python 3.12** avec des installations fixes (`.github/workflows/ci.yml`) ; le niveau d’artefacts a besoin des arbres enregistrés sous `E:\AI\training`, qui ne sont pas dans Git, donc la CI les exclut intentionnellement. Localement, `python -m pytest` exécute les **1 223** tests et `python -m pytest -m "not artifacts"` exécute les **1 173** tests reproduits par la CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
