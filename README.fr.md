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

Le style est appliqué **sur l’élément**, dans l’espace de la texture — et non peint pour chaque vue, puis assemblé par la suite. Fournissez à la chaîne un concept d’argile aux formes exagérées, et elle renverra une maille texturée dont la couleur provient d’une référence stylisée de *cette* maille, avec tout ce que la référence ne pouvait pas voir, rempli par un pinceau de retouche masqué et une dilatation tenant compte de la surface.

Nommé en fonction des deux aspects du problème : les polygones et la face qu’ils doivent représenter.

## Installation

La chaîne elle-même est un ensemble de scripts locaux que vous exécutez sur des chemins que vous tapez — clonez le dépôt et lisez [comment démarrer](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Deux serveurs sont fournis dans un seul package** : l’index des enregistrements, afin qu’un assistant puisse interroger la trace des preuves au lieu de la lire, et **à partir de la version 0.4.0, le serveur de mesure**, de sorte que deux éléments mesurés à plusieurs mois d’intervalle passent par un seul chemin de code.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` est le serveur MCP stdio qui traite les enregistrements (six outils, dont la vérification à quatre points servant de surface de contrôle) et `facet-index` est l’index lui-même (`build` / `verify` / `q` / `claims`). Exécutez l’un ou l’autre depuis un répertoire extrait ; `--db` désigne un index différent.

### Le serveur de mesure — nouveau dans la version 0.4.0

`facet-measure` répond à la **partie numérique** d’une comparaison et n’indique jamais si le résultat est bon. Chaque charge utile contient la version du serveur, le hachage du fichier de l’instrument et un hachage de configuration, et `measure_report` **refuse** de comparer des éléments qui ne correspondent pas — ce qui est la propriété pour laquelle tout cela existe.

Vérifié en exécutant une **commande** plutôt que `--help` : une maille de contrôle renvoie 786 432 faces avec une enveloppe d’identité complète sur une machine où aucun élément n’a été extrait.

**Ce que vous obtenez dépend d’une seule chose, et c’est votre version de Python :**

| votre Python | `[measure-full]` vous donne |
|---|---|
| **3.11 / 3.12** | **les huit outils** — `open3d` s’installe à partir de PyPI |
| **3.13** | quatre outils ; `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 est la dernière *version* et publie des roues cp38–cp312 **sans sdist**, de sorte que sur 3.13, il n’y a rien sur PyPI à installer. L’élément supplémentaire le fournit en arrière-plan via `python_version < "3.13"`, de sorte que l’installation **réussie** et les quatre outils de géométrie renvoient **`4` REFUSÉ**, indiquant ce dont ils ont besoin — plutôt que l’échec complet de l’installation.

**Pour obtenir les huit sur Python 3.13**, Open3D publie des roues cp313 actuelles sur son canal de développement continu. Une URL directe est acceptable dans une ligne de commande ; elle n’est interdite que dans les métadonnées du package publié :

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **Sur Windows et macOS, les roues de développement sont suffixées par `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` au moment de la rédaction), et le nom change lorsque `main` change — listez les éléments sur [la version `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) et prenez la version actuelle. **Cette version est celle par rapport à laquelle les nombres de cette chaîne, qui dépendent d’Open3D, ont été mesurés**, et elle constitue une véritable limite de comparabilité : l’enveloppe d’identité enregistre le hachage de l’instrument, et non ses dépendances — [E31](docs/experiments/E31-ruling.md).

*Jusqu’à la version 0.3.1, la roue contenait deux fichiers `.py` et aucun des instruments de mesure, de sorte qu’un serveur de mesure installé n’avait rien à exécuter. Personne ne l’a remarqué pendant quatre versions parce que ce dépôt EST le répertoire extrait : l’outil fonctionnait là où il était construit et n’avait jamais été ailleurs.*

⚠ **`pip install facet-mcp` était défectueux dans toutes les versions publiées jusqu’à la version 0.3.0, et est corrigé dans la version 0.3.1.** La roue installe `facet_index` en tant que module de niveau supérieur, de sorte que jusqu’à et y compris la version 0.3.0, elle résolvait l’emplacement de l’enregistrement par rapport à `<venv>/Lib` — qui ne contient ni corpus ni index — et `build`, `claims` et `q` sans `--db` échouaient tous. **Pour la version 0.3.0 ou antérieure, utilisez le fichier binaire `npx` ci-dessus.**

À partir de la version 0.3.1, la racine est résolue en **vérifiant l’existence de l’enregistrement** plutôt qu’en supposant son existence : exécutez l’une ou l’autre commande depuis un répertoire extrait et elle le trouvera ; exécutez-la depuis n’importe quel autre endroit et elle renverra **`4` REFUSÉ**, en indiquant les deux répertoires dans lesquels elle a essayé de chercher et les deux marqueurs qu’elle a recherchés. `$FACET_INDEX_DB` est maintenant lu par les deux commandes, et il sélectionne l’*index*, jamais le *corpus*. Mesuré sur une roue construite à partir de `main` et installée dans un environnement virtuel propre — [E24](docs/experiments/E24-ruling.md).

*Ce bloc a été corrigé deux fois. Il indiquait d’abord `pipx install facet-mcp # ou le package Python directement `, until v0.3.0's read-back ran a **verb** instead of ` --help`. Ensuite, il affirmait que la roue « ne fonctionne que pour `q` et `claims` » — **`claims` ne fonctionnait pas non plus**, ce que E24 a découvert en l’exécutant. Les deux corrections se trouvent dans [known-defects.md](docs/known-defects.md) avec leurs mesures.*

## Où cela en est

**Quatre éléments acceptés, répartis sur quatre classes de sujets, sans frais.** Chacun a été validé par le directeur à son propre niveau de zoom — sur le fichier GLB ou sur des feuilles de taille réelle — et non par une métrique qui dépasse un seuil.

| sujet | classe | accepté | référence / pinceau / dilatation |
|---|---|---|---|
| **Character (W3)** | humanoïde | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | véhicule, armature fine | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bête, membranes des ailes | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | accessoire, presque 2D, gris sur gris | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Les parts sont constituées de texels valides, et **elles ne sont pas comparables entre les sujets** : un navire cache la majeure partie de lui-même au niveau des yeux et un animal en cache la moitié. Évaluez chaque élément par rapport à son propre seuil d’étendue préenregistré, par rapport auquel ils atteignent **86 à 93 %** : la différence entre les lignes est une question de géométrie, pas de régression. [Nombres complets, avec leurs dénominateurs](docs/handbook/subjects.md).

**Il s’agit d’un pipeline, et non d’un générateur à un seul caractère.** Contredisez la spécification sur huit éléments nommés et l’invite gagne **8 sur 8** — ΔE médian de 46,3 contre 6,2 sur cinq contrôles maintenus — tandis que la figure reste le même homme. La structure est assurée par la maille et le contrôle ; les attributs nommés sont liés à l’invite.

## La chaîne

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

Étape par étape, avec la justification de chaque étape : **[le manuel](docs/handbook/index.md)**.

**Le « dashed hop » est une nouveauté et n’est délibérément pas uniforme.** La première boîte de la séquence a toujours affiché le texte *clay concept*, et jusqu’à présent, rien ici ne l’avait produit : chaque morceau d’argile était ajouté manuellement et modifié en cours de route. Un outil « concept → argile » existe désormais et sa première version a été testée à taille réelle : la pose, les protège-poignets, le médaillon de ceinture et l’ourlet déchiré ont tous été pris en compte ; la masse de crinière n’a pas été prise en compte ; la fuite de couleur a été mesurée sur toute l’image avec une valeur de **C\* p99.9 = 13.15** et un arrière-plan achromatique uniforme. **Ce que cette version ne peut pas montrer, c’est si le maillage s’améliore**, ce qui est la seule question qui justifie son utilisation, elle reste donc une candidate avec ses preuves enregistrées : **[concept prep](docs/concept-prep.md)**.

## Ce qui permet de l’utiliser

Six découvertes, chacune nécessitant un test et chacune s’appliquant à un domaine plus large que le sujet qui l’a générée. [La version complète, avec les mesures](docs/findings.md).

- **D’abord la forme, ensuite le style.** Les outils de reconstruction interprètent le bruit de surface comme une géométrie. Une argile propre et sculpturale, avec des plans délibérément exagérés, donne un meilleur résultat en termes de topologie qu’un sprite stylisé ; la version jumelle stylisée est générée simultanément et devient la référence de couleur.
- **Délimitez le visage pour obtenir un visage.** Un recadrage du buste ajoute **3,1 à 4,5 fois** plus de polygones sur la tête, et la différence est structurelle : paupières séparées, sillon frontal, cavités des narines modélisées, et non pas un flou plus prononcé.
- **Les jumeaux appartiennent à un maillage, et non à un personnage.** Réutilisez un jumeau sur différents maillages et la couverture diminue de **62 % à 22,7 %**, car les bras se projettent dans l’espace vide à côté du modèle. Générez des jumeaux à partir du maillage que vous allez texturer, à chaque fois.
- **L’identité appartient à la requête.** Un élément canonique qui n’est pas nommé dans la requête apparaît par hasard et disparaîtra de la même manière : cela a été mesuré lorsque les plaques dorées sur les genoux se sont avérées apparaître uniquement dans l’image en raison du bruit dans un ControlNet défectueux.
- **Demandez à la géométrie, pas à un seuil.** Le remplacement d’un masque clé par le contour exact du lancer de rayons a amélioré la couverture de référence de **28,4 % à 39,1 %** des texels valides : uniquement additif, sans diffusion, sans utilisation du GPU. La technique de masquage basée sur la médiane des coins a échoué trois fois ici et est abandonnée.
- **Supprimez ce qu’aucune caméra ne peut voir, à partir de l’atlas et jamais du maillage.** 49 % des texels de l’atlas sont invisibles depuis l’extérieur ; en excluant ces faces, l’interpolation diminue de **68 %.** Plutôt que de supprimer, il est préférable d’exclure, ce qui rend l’échec impossible au lieu de simplement détectable.

## Ce qui n’est pas résolu

Nommé et mesuré, sur la page d’accueil plutôt que dans une note de bas de page. [Tous, situés dans le code](docs/known-defects.md).

- **La bande de lame représente 0 % de la référence de l’étape 1** sur les huit caméras : l’acier sur un fond gris se situe exactement au seuil du masque. L’union permet d’obtenir une amélioration de 55,72 %.
- **Les joints des traits ne sont pas uniformisés.** Une limite de provenance représente **5,5 fois** la variation normale de la texture ; la région que le directeur a nommée représente **9,5 fois**.
- **La dilatation se propage entre les îles d’atlas non apparentées** : 74,9 % des texels dilatés tirent leur couleur d’une autre île, avec une distance médiane de 0,177 sur une figure de 1,0.
- **Chaque reconstruction dans cette séquence est une double coque creuse**, les parois mesurant environ deux voxels. Aucune condition volumétrique n’est valide pour l’une d’entre elles.

## Comment ce dépôt est utilisé

La discipline est aussi importante que le processus, et elle existe pour une raison : un cycle précédent a comporté dix sessions qui ont chacune évalué leurs propres résultats et rédigé des conclusions que la session suivante a considérées comme des faits établis. Rien dans ce cycle n’était vérifiable.

- **Spécifiez avant le travail, faites un rapport après, et prenez une décision en dernier** : et la session qui conçoit un test n’évalue jamais ses propres résultats. Trente-et-un tests sont disponibles dans [le registre](docs/experiments/).
- **Les corrections sont appliquées sur place, à côté de la mesure qui les a invalidées**, et non pas sous forme de suppressions discrètes. Six affirmations héritées ont été réfutées lors de la session initiale, et les six sont toujours lisibles à côté de ce qui les a remplacées.
- **Les échecs restent dans le dépôt avec leur raison.** [`tools/superseded/`](docs/tools.md) n’est pas une archive : tout le monde peut exécuter ces outils et observer qu’ils échouent de la même manière.
- **Un résultat négatif est un succès total**, qui est signalé et clôturé plutôt que modifié pour atteindre un nombre.
- **Les tests sont liés au commit qui touche le code** : 1053 tests réussis, évalués par deux personnes, avec une intégration continue basée sur les chemins pour les 1008 tests hermétiques.
- **Le registre est interrogeable.** Un index SQLite + FTS5 sur l’ensemble de la séquence, vérifié sur quatre systèmes. Il a trouvé un nombre de résultats que le texte avait mal indiqué à trois endroits, en comptant simplement le nombre de résultats dans le registre.

## Où tout se trouve

| | |
|---|---|
| **[Le manuel](docs/handbook/index.md)** | le guide : la séquence étape par étape, les sujets et le système de profil |
| **[Préparation du concept](docs/concept-prep.md)** | la séquence candidate « dashed hop » : sa première itération (Gate 0), son placement et l’élément de licence qu’elle ouvre |
| **[Le registre](docs/experiments/)** | trente-et-un tests : spécifications, rapport, décision et chaque prédiction formulée avant la mesure |
| **[Ce que la séquence a appris](docs/findings.md)** | les résultats durables et les règles acquises avec difficulté, dans leur intégralité |
| **[État de chaque outil](docs/tools.md)** | ce qui fonctionne, ce qui est obsolète et les preuves pour chacun |
| **[Défauts connus](docs/known-defects.md)** | tout ce qui n’est pas résolu, mesuré et situé dans le code |
| **[L’arc, tel qu’il s’est déroulé](docs/arc-history.md)** | l’historique chronologique, avec les corrections intactes |
| **[CLAUDE.md](CLAUDE.md)** | comment travailler ici : les rôles, les règles et ce que chacun implique |

## Position de la licence

Chaque étape s’exécute en local et est propre sur le plan commercial : SDXL (OpenRAIL++), MV-Adapter (open), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Exclu délibérément, avec la raison suivante : **nvdiffrast** (non commercial — appliqué ici par un mécanisme de sécurité structurel, et non par une attestation), **Hunyuan3D-Paint** (licence invalide dans l’UE, au Royaume-Uni et en Corée du Sud), **MVPaint** et **TEXGen** (aucune licence) et **UltraSharp / SUPIR / StableSR** (algorithmes d’amélioration non commerciaux).

**La limite de la revendication est définie explicitement, plutôt que laissée à la découverte.** Elle décrit le **parcours enregistré** — les étapes du schéma ci-dessus, à partir de l’image vers la 3D. L’étape candidate de préparation des modèles en amont s’exécute actuellement sur une API cloud fermée dont les conditions cette archive **n’a pas vérifiées**, donc aucune revendication de licence ici ne couvre un élément créé à partir d’un de ses modèles. Il s’agit d’un point ouvert avec un chemin défini pour le résoudre : le modèle local conforme aux licences est **Qwen-Image-Edit (Apache-2.0)**, et **FLUX.1-Kontext [dev] est exclu pour les mêmes raisons que nvdiffrast** — poids non commerciaux. Les deux ont été vérifiés par rapport au catalogue de modèles du studio plutôt qu’en se basant sur des informations antérieures ; le raisonnement se trouve dans [concept prep](docs/concept-prep.md).

## Modèle de confiance et de menace

facet s’exécute entièrement sur votre propre machine — chaque outil est un script que vous exécutez sur des chemins que vous tapez, la question utile n’est donc pas *quelles sont les autorisations demandées par cette application*, mais *que font ces scripts sur votre machine*. La réponse est fournie par une mesure, et chaque cycle peut être répété ; la politique complète se trouve dans [SECURITY.md](SECURITY.md) :

- **Données concernées :** maillages, textures, images et JSON sur le disque local, aux chemins que vous spécifiez dans la ligne de commande. De plus, `docs/index/facet.db`, qui est *dérivé* — il ne contient rien qui n’était pas déjà un fichier dans cette archive, et `facet_index.py build` le régénère à partir de zéro.
- **Données NON concernées :** aucune information d’identification, jamais. Rien ici ne lit, ne stocke ou ne transmet de jeton, de clé ou de mot de passe, et rien de tel n’est présent dans l’arborescence — une recherche a été effectuée pour les clés préfixées par le fournisseur, les GitHub PAT, les jetons Slack, les ID de clés AWS, les blocs de clés privées, les jetons d’authentification et les affectations en ligne `api_key`/`password`, **zéro correspondance**, aucun fichier ressemblant à une information d’identification n’a été détecté.
- **Pas de télémétrie.** Aucune donnée n’est collectée ni envoyée. Il n’y a pas d’option de désactivation car il n’y a rien à désactiver.
- **Sortie réseau :** deux des trente-quatre outils ouvrent un socket — `restylize_views.py` et `texpass_brush.py` — et les deux appellent une API HTTP ComfyUI à l’adresse `--host`, **par défaut `127.0.0.1:8188`**. Rien d’autre dans `tools/` n’effectue d’appel réseau.
- **Autorisations :** utilisateur ordinaire. Pas d’élévation de privilèges, pas d’installation de service, pas d’écriture dans les paramètres système ou le registre.

Trois points critiques sont explicitement mentionnés plutôt que simplement revendiqués, car une note de sécurité qui ne contient que des assurances n’est pas un modèle de menace : **les opérations sur les fichiers ne sont pas exécutées dans un environnement isolé** (un outil écrit partout où ses arguments l’indiquent) ; **des chemins locaux absolus sont intégrés à de nombreux outils et documents** — 114 occurrences dans 26 fichiers, ce ne sont pas des secrets mais une divulgation de la configuration d’une machine, et c’est la raison pour laquelle la plupart des outils ne fonctionneront pas sans modification ailleurs ; et **les échecs inattendus se manifestent sous forme de traces Python dans les 34 scripts de recherche non publiés**, sans passerelle `--debug`. Les arrêts délibérés sont des messages `ANDON:` qui contiennent la mesure qui les a déclenchés. Il s’agit du contrat d’instrument de recherche, et [SHIP_GATE.md](SHIP_GATE.md) enregistre exactement le moment où il cesse d’être suffisant — ce qui était le cas pour les deux commandes que facet *installe*, à la version 0.2.0 : `facet-index` et `facet-mcp` renvoient `0` ok / `1` erreur utilisateur / `2` erreur d’exécution — et, depuis [E22](docs/experiments/E22-ruling.md), **`4` REFUSÉ** pour une passerelle déclenchée ou une étape `verify` qui échoue, ce qui signifie que l’outil fonctionne et vous indique de ne pas continuer plutôt qu’une erreur d’exécution. Tous les outils refusent avec un échec structuré qui nomme la prochaine étape au lieu d’une trace ([E21](docs/experiments/E21-cli-contract-report.md)).

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

**État du support :** cette archive est développée en open source, sur une seule machine, par un seul responsable et une paire d’experts et d’exécutants qui se relaient. `main` est le seul état pris en charge. Il n’y a pas de canal de publication, pas de politique de rétroportage et pas de SLA — ce qu’il y a à la place, c’est l’enregistrement : chaque revendication est placée à côté du code qui la produit, et [docs/experiments](docs/experiments/) contient les spécifications, le rapport et la décision pour chacun.

## Exigences

Blender 5.x, Python 3.11+ avec `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Une installation locale de ComfyUI n’est nécessaire que pour le pinceau d’inpainting. Développé sur une RTX 5090 ; la capacité de VRAM est plus importante que la vitesse brute.

L’intégration continue exécute le sous-ensemble hermétique de la suite sur **ubuntu-latest / Python 3.12** avec des installations fixes (`.github/workflows/ci.yml`) ; la couche des artefacts a besoin des arborescences enregistrées situées dans `E:\AI\training`, qui ne se trouvent pas dans Git, c’est pourquoi l’intégration continue les exclut intentionnellement. Localement, `python -m pytest` exécute les **1053** tests et `python -m pytest -m "not artifacts"` exécute les **1008** tests reproduits par l’intégration continue.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
