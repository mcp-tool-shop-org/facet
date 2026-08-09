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
  Local hardware end to end · no non-commercial licence anywhere in the chain
</p>

---

Le style est appliqué **sur l’élément**, dans l’espace de texture — et non peint pour chaque vue, puis assemblé par la suite. Fournissez à la chaîne un modèle d’argile aux formes exagérées, et elle renverra une maille texturée dont la couleur provient d’une référence stylisée de *cette* maille, avec tout ce que la référence ne pouvait pas voir, rempli par un pinceau de retouche masqué et une dilatation tenant compte de la surface.

Il a été nommé en fonction des deux aspects du problème : les polygones et la forme qu’ils doivent conserver.

## Installation

La chaîne elle-même est un ensemble de scripts locaux que vous exécutez sur des chemins que vous tapez — clonez le dépôt et lisez [comment démarrer](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**L’index des enregistrements est fourni sous forme de package**, afin qu’un assistant puisse interroger la trace des preuves au lieu de la lire :

```bash
npx @mcptoolshop/facet          # zero-prerequisite; verified binary, no Python needed
```

Deux commandes sont fournies : `facet-mcp`, le serveur MCP stdio (six outils, dont la vérification à quatre points comme surface de santé qui refuse), et `facet-index` (`build` / `verify` / `q` / `claims`). Exécutez-les depuis l’intérieur d’un répertoire extrait ; `--db` désigne un index différent.

⚠ **`pip install facet-mcp` était défectueux dans toutes les versions publiées jusqu’à la v0.3.0, et a été corrigé dans la v0.3.1.** Le package installe `facet_index` comme module de premier niveau, de sorte que jusqu’à et y compris la v0.3.0, il résolvait l’emplacement de l’enregistrement par rapport à `<venv>/Lib` — qui ne contient ni corpus ni index — et `build`, `claims` et `q` sans `--db` échouaient tous.
**Pour la v0.3.0 ou une version antérieure, utilisez le fichier binaire `npx` ci-dessus.**

À partir de la v0.3.1, la racine est résolue en **vérifiant l’existence de l’enregistrement** plutôt qu’en supposant son existence : exécutez l’une ou l’autre des commandes depuis l’intérieur d’un répertoire extrait et elle le trouvera ; exécutez-la depuis n’importe quel autre endroit et elle se terminera avec **`4` REFUSÉ**, en indiquant les deux répertoires qu’elle a essayés et les deux marqueurs qu’elle a recherchés.
`$FACET_INDEX_DB` est maintenant lu par les deux commandes, et il sélectionne l’*index*, jamais le *corpus*. Mesuré sur un package construit à partir de `main` et installé dans un environnement virtuel propre — [E24](docs/experiments/E24-ruling.md).

*Ce bloc a été corrigé deux fois. Il indiquait d’abord `pipx install facet-mcp # ou le package Python directement`, until v0.3.0's read-back ran a **verb** instead of `--help`.
Il affirmait ensuite que le package « ne fonctionne que pour `q` et `claims` » — **`claims` ne fonctionnait pas non plus**, ce qu’E24 a découvert en l’exécutant. Les deux corrections se trouvent dans [known-defects.md](docs/known-defects.md) avec leurs mesures.*

## Où il en est

**Quatre éléments acceptés, répartis sur quatre classes de sujets, sans coût.** Chacun a été validé par le directeur à son propre niveau de zoom — sur le fichier GLB ou sur des feuilles de taille réelle — et non par une métrique qui dépasse un seuil.

| sujet | classe | accepté | référence / pinceau / dilatation |
|---|---|---|---|
| **Character (W3)** | humanoïde | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | véhicule, gréement fin | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bête, membranes des ailes | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | accessoire, presque 2D, gris sur gris | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Les parts sont constituées de texels valides, et **elles ne sont pas comparables entre les sujets** — un navire cache la majeure partie de lui-même depuis le niveau des yeux et un animal en cache la moitié. Évaluez chaque élément par rapport à son propre plafond d’étendue préenregistré, par rapport auquel ils atteignent **86 à 93 %** : la différence entre les lignes est géométrique, pas une régression. [Chiffres complets, avec leurs dénominateurs](docs/handbook/subjects.md).

**Il s’agit d’une chaîne de traitement, et non d’un générateur à un seul caractère.** Contredisez la spécification sur huit éléments nommés, et l’invite gagne **8 sur 8** — ΔE médian de 46,3 contre 6,2 sur cinq contrôles maintenus — tandis que la figure reste le même homme. La structure est assurée par la maille et le contrôle ; les attributs nommés sont liés à l’invite.

## La chaîne de traitement

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

Étape par étape, avec la justification pour chaque étape : **[le manuel](docs/handbook/index.md)**.

## Ce qui le fait fonctionner

Six découvertes, chacune d’entre elles ayant nécessité une expérience et chacune d’elles étant applicable au-delà du sujet qui l’a produite. [La version longue, avec les mesures](docs/findings.md).

- **D’abord la forme, puis le style.** Les reconstructeurs interprètent le bruit de surface comme une géométrie. Une argile propre et sculpturale, dotée de plans délibérément exagérés, donne un meilleur résultat en termes de topologie qu’un sprite stylisé ; le jumeau stylisé est généré simultanément et devient la référence de couleur.
- **Encadrez le visage, obtenez un visage.** Un recadrage du buste place **3,1 à 4,5 fois** plus de polygones sur la tête, et la différence est structurelle — paupières séparées, sillon du front, cavités des narines modélisées — et non une simple amélioration.
- **Les jumeaux appartiennent à une maille, pas à un personnage.** Réutilisez un jumeau sur différentes mailles et la couverture diminue de **62 % à 22,7 %**, car les bras se projettent dans l’espace vide à côté du modèle. Générez des jumeaux à partir de la maille que vous allez texturer, à chaque fois.
- **L’identité appartient à l’invite.** Un élément canonique qui n’est pas nommé dans l’invite apparaît par hasard et disparaîtra de la même manière — mesuré lorsque les plaques dorées sur les genoux se sont avérées apparaître dans l’image uniquement en raison du bruit dans un ControlNet défectueux.
- **Demandez à la géométrie, et non à un seuil.** Le remplacement d’un masque clé par le contour exact du lancer de rayons a déplacé la couverture de référence de **28,4 % à 39,1 %** des texels valides — strictement additif, sans diffusion, sans GPU. La sélection basée sur les coins a maintenant échoué trois fois ici et est abandonnée.
- **Supprimez ce qu’aucune caméra ne peut voir, de l’atlas et jamais de la maille.** 49 % des texels de l’atlas sont invisibles depuis l’extérieur ; l’exclusion de ces faces réduit l’interpolation de 68 %. L’exclusion plutôt que la suppression rend l’échec impossible au lieu d’être simplement détectable.

## Ce qui n’est pas résolu

Nommé et mesuré, sur la page d’accueil plutôt que dans une note de bas de page. [Tous, situés dans le code](docs/known-defects.md).

- La bande de découpe représente 0,00 % de la référence de l’étape 1 sur les huit caméras — l’acier sur un fond gris est parfaitement aligné avec le seuil de la clé. L’ensemble permet d’obtenir un résultat de 55,72 %.
- Les joints ne sont pas nivelés. Une limite de provenance représente une variation de texture ordinaire de **5,5×** ; la région désignée par le réalisateur représente une variation de **9,5×**.
- La dilatation se propage entre les îles d’atlas non apparentées — 74,9 % des texels dilatés tirent leur couleur d’une autre île, à une distance médiane de 0,177 sur une figure de 1,0.
- Chaque reconstruction sur cet itinéraire est une coquille creuse à double paroi, les parois mesurant environ deux voxels. Aucune condition volumétrique n’est valide pour l’un d’eux.

## Comment ce dépôt est utilisé

La rigueur est aussi importante que le processus lui-même, et elle a une raison d’être : un cycle précédent a comporté dix sessions au cours desquelles chaque session a évalué ses propres résultats et rédigé des conclusions qui ont été lues lors de la session suivante comme des faits établis. Rien dans ce cycle n’était vérifiable.

- Définir les spécifications avant le travail, rédiger un rapport après, et prendre une décision finale — et la session qui conçoit une expérience n’évalue jamais ses propres résultats. Vingt-six expériences sont disponibles dans [les archives](docs/experiments/).
- Les corrections sont appliquées en place, à côté de la mesure qui les a invalidées, et non sous forme de suppressions discrètes. Six affirmations héritées ont été réfutées lors de la session initiale, et les six sont toujours visibles à côté de ce qui les a remplacées.
- Les échecs restent dans le dépôt avec leur raison. [`tools/superseded/`](docs/tools.md) n’est pas une archive — chacun peut exécuter ces outils et observer qu’ils échouent de la même manière.
- Un résultat négatif est un succès total, qui est signalé et clôturé plutôt que d’être ajusté pour atteindre une valeur cible.
- Les tests sont associés au commit qui modifie le code — 736 tests réussis sur deux postes, avec une intégration continue basée sur les chemins pour les 727 tests hermétiques.
- Les archives peuvent être consultées. Un index SQLite + FTS5 est appliqué à l’ensemble du parcours et vérifié sur quatre points. Il a trouvé un nombre de décisions erroné dans le texte à trois endroits, en comptant les données elles-mêmes.

## Où tout se trouve

| | |
|---|---|
| **[Le manuel](docs/handbook/index.md)** | le guide — l’itinéraire étape par étape, les sujets, le système de profilage |
| **[Les archives](docs/experiments/)** | vingt-six expériences : spécifications, rapport, décision et chaque prédiction formulée avant la mesure |
| **[Ce que l’itinéraire a appris](docs/findings.md)** | les conclusions durables et les règles acquises avec difficulté, en intégralité |
| **[État de chaque outil](docs/tools.md)** | ce qui fonctionne, ce qui est obsolète et les preuves pour chacun |
| **[Défauts connus](docs/known-defects.md)** | tout ce qui n’a pas été résolu, mesuré et localisé dans le code |
| **[Le cycle, tel qu’il s’est déroulé](docs/arc-history.md)** | l’historique chronologique, avec les corrections intactes |
| **[CLAUDE.md](CLAUDE.md)** | comment travailler ici — les rôles, les règles et ce que chacun implique |

## Position concernant la licence

Chaque étape s’exécute localement et est conforme aux exigences commerciales : SDXL (OpenRAIL++), MV-Adapter (open source), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Exclusions délibérées, avec la raison : **nvdiffrast** (non commercial — appliqué ici par un mécanisme de sécurité structurel, et non par une attestation), **Hunyuan3D-Paint** (licence invalide dans l’UE, au Royaume-Uni et en Corée du Sud), **MVPaint** et **TEXGen** (aucune licence) et **UltraSharp / SUPIR / StableSR** (algorithmes d’amélioration non commerciaux).

## Modèle de confiance et de menace

facet s’exécute entièrement sur votre propre machine — chaque outil est un script que vous exécutez sur des chemins que vous saisissez, la question pertinente n’est donc pas *quelles sont les autorisations demandées par cette application*, mais *ce que font ces scripts sur votre machine*. La réponse est fournie par la mesure, et chaque cycle peut être réexécuté ; la politique complète figure dans [SECURITY.md](SECURITY.md) :

- **Données concernées :** maillages, textures, images et fichiers JSON sur le disque local, aux chemins que vous indiquez dans la ligne de commande. De plus, `docs/index/facet.db`, qui est *dérivé* — il ne contient rien qui n’était pas déjà un fichier dans ce dépôt, et `facet_index.py build` le régénère à partir de zéro.
- **Données NON concernées :** aucune donnée d’identification, jamais. Rien ici ne lit, ne stocke ou ne transmet de jeton, de clé ou de mot de passe, et rien de tel n’est présent dans l’arborescence — recherche effectuée pour les clés préfixées par le fournisseur, les GitHub PAT, les jetons Slack, les ID de clé AWS, les blocs de clé privée, les jetons porteurs et les affectations en ligne `api_key`/`password`, **zéro correspondance**, aucun fichier ressemblant à une donnée d’identification suivi.
- **Pas de télémétrie.** Aucune donnée n’est collectée ni envoyée. Il n’y a pas d’option de désactivation car il n’y a rien à désactiver.
- **Échange réseau :** deux des trente-quatre outils ouvrent un socket — `restylize_views.py` et `texpass_brush.py` — et les deux appellent une API HTTP ComfyUI à l’adresse `--host`, **par défaut `127.0.0.1:8188`**. Rien d’autre dans `tools/` n’effectue d’appel réseau.
- **Autorisations :** utilisateur ordinaire. Aucune élévation de privilèges, aucune installation de service, aucune écriture dans les paramètres système ou le registre.

Trois arêtes vives sont révélées plutôt que niées, car une note de sécurité qui ne contient que des assurances n’est pas un modèle de menace : les opérations sur les fichiers ne sont pas exécutées dans un environnement isolé (un outil écrit partout où ses arguments l’indiquent) ; les chemins locaux absolus sont intégrés à de nombreux outils et documents — 114 occurrences dans 26 fichiers, ce ne sont pas des secrets mais la divulgation de la configuration d’une machine, et la raison pour laquelle la plupart des outils ne fonctionneront pas sans modification ailleurs ; et les échecs inattendus se manifestent sous forme de traces Python dans les 34 scripts de recherche non publiés, sans aucun filtre `--debug`. Les arrêts intentionnels sont des messages `ANDON:` qui contiennent la mesure qui les a déclenchés. C’est le contrat de l’instrument de recherche, et [SHIP_GATE.md](SHIP_GATE.md) enregistre précisément le moment où il cesse d’être suffisant — ce qui était le cas pour les deux commandes *d’installation* à la version 0.2.0 : `facet-index` et `facet-mcp` renvoient `0` (ok) / `1` (erreur utilisateur) / `2` (erreur d’exécution), et, depuis [E22](docs/experiments/E22-ruling.md), `4` est REFUSÉ pour un filtre déclenché ou une branche défaillante `verify`, ce qui signifie que l’outil fonctionne et vous indique de ne pas continuer plutôt qu’il s’agisse d’une erreur d’exécution. Tous les éléments refusent avec un message d’erreur structuré indiquant l’étape suivante au lieu d’une trace ([E21](docs/experiments/E21-cli-contract-report.md)).

Et les filtres de ces deux commandes ne sont plus supprimables. Chaque ANDON dans la facette d’installation `raise` ; un simple `assert` est une instruction que `python -O` supprime silencieusement, et 87 des filtres de ce dépôt pouvaient être supprimés par une variable d’environnement jusqu’à ce qu’E22 les modifie. Mesuré avant et après sur le même filtre, dans quatre modes interpréteur. Et depuis [E23](docs/experiments/E23-route-gates-report.md), les filtres de la route qui a produit les quatre actifs acceptés ne sont plus supprimables — ses 57 sites répartis sur douze outils, convertis en un simple déplacement de fichiers qu’aucun test n’a jamais exécuté, chacun refusant désormais sous `-O` et `PYTHONOPTIMIZE=1` ainsi que dans un interpréteur normal. Et depuis [E25](docs/experiments/E25-ruling.md), la classe est fermée. Ses 133 sites répartis sur 43 fichiers — les instruments de mesure qui ont produit les preuves des quatre actifs acceptés ci-dessus — se convertissent de la même manière, portant le total à 278 (`raise`). Exactement un seul ANDON simple `assert` reste quelque part sous `tools/` : `superseded/texpass_thin_mask.py`, qui n’est jamais converti, car ces outils sont conçus pour que chacun puisse les exécuter et observer leur échec de la même manière. Ce reste est fixé par son nom dans la suite de tests, de sorte qu’une future analyse ne puisse pas le supprimer sans modifier intentionnellement le test.

**État du support :** ce dépôt est développé en mode ouvert, sur une seule plateforme, par un seul responsable et une équipe rotative de conseillers et d’exécutants. `main` est le seul état pris en charge. Il n’y a pas de canal de publication, pas de politique de rétroportage et pas de SLA : à la place, il existe un enregistrement : chaque affirmation se trouve à côté du code qui la produit, et [docs/experiments](docs/experiments/) contient les spécifications, le rapport et le jugement pour chacun.

## Exigences

Blender 5.x, Python 3.11+ avec `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Une installation locale de ComfyUI n’est nécessaire que pour le pinceau d’inpainting. Développé sur une RTX 5090 ; la marge de VRAM est plus importante que la vitesse brute.

CI exécute le sous-ensemble hermétique de la suite sur **ubuntu-latest / Python 3.12** avec des installations fixes (`.github/workflows/ci.yml`) ; la couche d’artefacts a besoin des arbres enregistrés sous `E:\AI\training`, qui ne se trouvent pas dans git, donc CI les désélectionne par conception. Localement, `python -m pytest` exécute les 736 tests et `python -m pytest -m "not artifacts"` exécute les 727 tests reproduits par CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
