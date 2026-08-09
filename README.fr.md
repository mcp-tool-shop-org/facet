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

Le style est appliqué **sur l’élément**, dans l’espace de texture — et non peint pour chaque vue, puis assemblé par la suite. Fournissez à la chaîne un concept d’argile aux formes exagérées, et elle renverra une maille texturée dont la couleur provient d’une référence stylisée de *cette* maille, avec tout ce que la référence ne pouvait pas voir, rempli par un pinceau de retouche masqué et une dilatation tenant compte de la surface.

Il a été nommé en fonction des deux aspects du problème : les polygones et la forme qu’ils doivent conserver.

## Installation

La chaîne elle-même est un ensemble de scripts locaux que vous exécutez sur les chemins que vous tapez — clonez le dépôt et lisez [comment démarrer](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**L’index des enregistrements est fourni sous forme de package**, afin qu’un assistant puisse interroger la chaîne de preuves au lieu de la lire :

```bash
npx @mcptoolshop/facet          # zero-prerequisite; verified binary, no Python needed
pipx install facet-mcp          # or the Python package directly
```

Deux commandes sont fournies : `facet-mcp`, le serveur MCP stdio (six outils, dont la vérification à quatre points comme surface de santé qui refuse), et `facet-index` (`build` / `verify` / `q` / `claims`). Dirigez l’un ou l’autre vers un index avec `--db` ou `$FACET_INDEX_DB`.

## Sa position actuelle

**Quatre éléments acceptés, répartis dans quatre classes de sujets, sans coût.** Chacun a été validé par le directeur en utilisant son propre niveau de zoom — sur le fichier GLB ou sur des feuilles de taille réelle — et non en fonction d’une valeur seuil.

| sujet | classe | accepté | référence / pinceau / dilatation |
|---|---|---|---|
| **Character (W3)** | humanoïde | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | véhicule, armature fine | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bête, membranes des ailes | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | accessoire, quasi-2D, gris sur gris | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Les données sont constituées de texels valides et **elles ne sont pas comparables entre les sujets** — un vaisseau cache la majeure partie de lui depuis le niveau des yeux et un animal en cache la moitié. Analysez chaque élément par rapport à son propre seuil prédéfini, ce qui donne un résultat de **86 à 93 %** : la différence entre les lignes est géométrique, pas une régression. [Chiffres complets avec leurs
dénominateurs](docs/handbook/subjects.md).

**Il s’agit d’une chaîne de traitement, et non d’un générateur à un seul élément.** Contredisez la spécification sur huit éléments nommés, et l’invite remporte **8 sur 8** — ΔE médian de 46,3 contre 6,2 sur cinq contrôles maintenus — alors que la figure reste la même. La structure est assurée par la maille et le contrôle ; les attributs nommés sont liés à l’invite.

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

Six découvertes, chacune d’entre elles ayant nécessité une expérience et chacune d’elles étant applicable au-delà du sujet qui l’a produite. [La version longue, avec les
mesures](docs/findings.md).

- **D’abord la forme, puis le style.** Les outils de reconstruction interprètent le bruit de surface comme une géométrie. Une argile propre et sculpturale, dotée de plans délibérément exagérés, donne un meilleur résultat en termes de topologie qu’un sprite stylisé ; le jumeau stylisé est généré simultanément et devient la référence de couleur.
- **Définissez le visage, obtenez un visage.** Un recadrage du buste place **3,1 à 4,5 fois** plus de polygones sur la tête, et la différence est structurelle — paupières séparées, sillon frontal, cavités des narines modélisées — et non une flou plus prononcé.
- **Les jumeaux appartiennent à une maille, pas à un personnage.** Réutilisez un jumeau dans différentes mailles et la couverture diminue de **62 % à 22,7 %**, car les bras se projettent dans l’espace vide à côté du modèle. Générez des jumeaux à partir de la maille que vous allez texturer, à chaque fois.
- **L’identité appartient à l’invite.** Un élément canonique qui n’est pas nommé dans l’invite apparaît par hasard et disparaîtra de la même manière — mesuré lorsque les plaques de genoux dorées se sont avérées ne parvenir à l’image que par le biais du bruit dans un ControlNet défectueux.
- **Demandez une géométrie, pas une valeur seuil.** Le remplacement d’un masque clé par le contour exact du lancer de rayons a déplacé la couverture de référence de **28,4 % à 39,1 %** des texels valides — strictement additif, sans diffusion, sans GPU. La technique de masquage basée sur les coins a échoué trois fois ici et est abandonnée.
- **Supprimez ce qu’aucune caméra ne peut voir, à partir de l’atlas et jamais de la maille.** 49 % des texels de l’atlas sont invisibles depuis l’extérieur ; l’exclusion de ces faces réduit l’interpolation de **68 %**. L’exclusion plutôt que la suppression rend l’échec impossible au lieu d’être simplement détectable.

## Ce qui n’est pas résolu

Nommé et mesuré, sur la page de garde plutôt que dans une note de bas de page. [Tous, situés dans le
code](docs/known-defects.md).

- **La bande de lame représente 0 % de la référence de l’étape 1** sur les huit caméras — l’acier sur un fond gris se situe exactement au seuil du masque. L’union sauve 55,72 %.
- **Les joints des traits ne sont pas uniformisés.** Une limite de provenance représente **5,5 fois** la variation normale de la texture ; la région que le directeur a nommée représente **9,5 fois**.
- **La dilatation déborde entre les îles d’atlas non apparentées** — 74,9 % des texels dilatés tirent leur couleur d’une autre île, avec une distance médiane de 0,177 sur une figure de hauteur 1,0.
- **Chaque reconstruction dans cette chaîne est une double coque creuse**, les parois faisant environ deux voxels. Aucun prédicat volumétrique n’est valide sur l’un d’eux.

## Comment ce dépôt est exécuté

La discipline est aussi importante que la chaîne de traitement, et elle existe pour une raison : une série précédente a duré dix sessions au cours desquelles chaque session a évalué sa propre production et a rédigé des conclusions que la session suivante a lues comme un fait établi. Rien dans cette boucle n’était vérifiable.

- **Définir les spécifications avant le travail, faire un rapport après, et établir une conclusion finale** — et la session qui conçoit une expérience n’évalue jamais ses propres résultats. Vingt-trois expériences sont disponibles dans [les archives](docs/experiments/).
- **Les corrections sont intégrées à leur emplacement, à côté de la mesure qui les a invalidées**, et non sous forme de suppressions discrètes. Six affirmations initiales ont été réfutées lors de la session initiale, et les six sont toujours consultables à côté de ce qui les a remplacées.
- **Les échecs restent dans le dépôt avec leur raison.** [`tools/superseded/`](docs/tools.md) n’est pas une archive — chacun peut exécuter ces outils et observer qu’ils échouent de la même manière.
- **Un résultat négatif est un succès total**, qui est signalé et clôturé plutôt que modifié pour atteindre une valeur cible.
- **Les tests sont liés au commit qui modifie le code** — 648 réussis avec deux personnes, avec une intégration continue basée sur les chemins pour les 640 éléments hermétiques.
- **Les archives peuvent être interrogées.** Un index SQLite + FTS5 sur l’ensemble de la série, vérifié sur quatre axes. Il a trouvé un nombre de conclusions que le texte avait mal indiqué à trois endroits, en comptant les données elles-mêmes.

## Où tout est…

| | |
|---|---|
| **[Le manuel](docs/handbook/index.md)** | le guide — l’étape par étape, les sujets, le système de profil |
| **[Les archives](docs/experiments/)** | vingt-trois expériences : spécifications, rapport, conclusion et chaque prédiction énoncée avant la mesure |
| **[Ce que le parcours a appris](docs/findings.md)** | les conclusions durables et les règles durement acquises, en intégralité |
| **[État de chaque outil](docs/tools.md)** | ce qui fonctionne, ce qui est obsolète et les preuves pour chacun |
| **[Défauts connus](docs/known-defects.md)** | tout ce qui n’a pas été résolu, mesuré et localisé dans le code |
| **[Le déroulement, tel qu’il s’est produit](docs/arc-history.md)** | l’historique chronologique, les corrections intactes |
| **[CLAUDE.md](CLAUDE.md)** | comment travailler ici — les rôles, les règles et ce que chacun implique |

## Position concernant la licence

Chaque étape s’exécute localement et est conforme aux exigences commerciales : SDXL (OpenRAIL++), MV-Adapter (open), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Exclu intentionnellement, avec la raison : **nvdiffrast** (non commercial — appliqué ici par un mécanisme de sécurité structurel, et non par une attestation), **Hunyuan3D-Paint** (licence invalide dans l’UE, au Royaume-Uni et en Corée du Sud), **MVPaint** et **TEXGen** (aucune licence) et **UltraSharp / SUPIR / StableSR** (améliorateurs non commerciaux).

## Modèle de confiance et de menace

facet s’exécute entièrement sur votre propre machine — chaque outil est un script que vous exécutez sur des chemins que vous tapez, la question pertinente n’est donc pas *quelles sont les autorisations demandées par cette application*, mais *que font ces scripts sur votre machine*. La réponse est fournie par la mesure, et chaque cycle peut être réexécuté ; la politique complète se trouve dans [SECURITY.md](SECURITY.md) :

- **Données concernées :** maillages, textures, images et JSON sur le disque local, aux chemins que vous indiquez dans la ligne de commande. De plus, `docs/index/facet.db`, qui est *dérivé* — il ne contient rien qui n’était pas déjà un fichier dans ce dépôt, et `facet_index.py build` le régénère à partir de zéro.
- **Données NON concernées :** aucune information d’identification, jamais. Rien ici ne lit, ne stocke ni ne transmet de jeton, de clé ou de mot de passe, et rien de tel n’est présent dans l’arborescence — recherche effectuée pour les clés préfixées par le fournisseur, les GitHub PAT, les jetons Slack, les ID de clé AWS, les blocs de clé privée, les jetons porteurs et les affectations en ligne `api_key`/`password`, **zéro correspondance**, aucun fichier ressemblant à une information d’identification suivi.
- **Pas de télémétrie.** Aucune donnée n’est collectée ni envoyée. Il n’y a pas d’option de désactivation car il n’y a rien à désactiver.
- **Échange réseau :** deux des trente-quatre outils ouvrent un socket — `restylize_views.py` et `texpass_brush.py` — et les deux appellent une API HTTP ComfyUI à `--host`, **par défaut `127.0.0.1:8188`**. Rien d’autre dans `tools/` n’effectue d’appel réseau.
- **Autorisations :** utilisateur ordinaire. Pas de privilèges élevés, pas d’installation de service, pas d’écriture dans les paramètres système ou le registre.

Trois points critiques sont divulgués plutôt que dissimulés, car une note de sécurité qui ne contient que des assurances n’est pas un modèle de menace : **les opérations sur les fichiers ne sont pas exécutées dans un environnement isolé** (un outil écrit à l’endroit indiqué par ses arguments) ; **des chemins locaux absolus sont intégrés dans de nombreux outils et documents** — 114 occurrences dans 26 fichiers, ce ne sont pas des secrets mais une divulgation de la disposition d’une machine, et la raison pour laquelle la plupart des outils ne fonctionneront pas sans modification ailleurs ; et **les échecs inattendus se manifestent sous forme de traces Python dans les 34 scripts de recherche non publiés**, sans passerelle `--debug`. Les arrêts intentionnels sont des messages `ANDON:` qui contiennent la mesure qui les a déclenchés. C’est le contrat d’instrument de recherche, et [SHIP_GATE.md](SHIP_GATE.md) indique exactement quand il cesse d’être suffisant — ce qui était le cas pour les deux commandes que facet *installe*, à la version 0.2.0 : `facet-index` et `facet-mcp` renvoient `0` ok / `1` erreur utilisateur / `2` erreur d’exécution — et, depuis [E22](docs/experiments/E22-ruling.md), **`4` REFUSÉ** pour une passerelle déclenchée ou un élément `verify` défaillant, ce qui signifie que l’outil fonctionne et vous indique de ne pas continuer plutôt qu’une erreur d’exécution. Tous refusent avec un échec structuré indiquant la prochaine étape au lieu d’une trace ([E21](docs/experiments/E21-cli-contract-report.md)).

**De plus, les portes dans ces deux commandes ne peuvent plus être supprimées.** Chaque module ANDON installe `raise` ; un simple `assert` est une instruction que `python -O` supprime silencieusement, et 87 des portes de ce dépôt pouvaient être supprimées à l’aide d’une variable d’environnement jusqu’à ce qu’E22 les modifie. Mesure effectuée avant et après sur la même porte, dans quatre modes d’interprétation.
**Et depuis [E23](docs/experiments/E23-route-gates-report.md), les portes du parcours qui a produit les quatre éléments acceptés ne peuvent plus être supprimées non plus** — ses **57 sites répartis sur douze outils**, convertis en un simple déplacement de fichiers sans qu’aucun test n’ait jamais été exécuté, chacun refusant désormais sous `-O` et `PYTHONOPTIMIZE=1` ainsi que sous un interpréteur normal.
**134 portes dans les outils de recherche restants sont toujours des assertions** — nommées ici plutôt que supprimées, définies par [E22 Ruling 4](docs/experiments/E22-ruling.md), et aucune d’entre elles ne se trouve dans un module qui installe : 132 sont des instruments de mesure sous `diagnostics/`, l’un est une vérification du rendu, et celui de `superseded/` n’est **jamais** converti, car ces outils sont conservés afin que chacun puisse les exécuter et observer leur échec de la même manière.

**État du support :** ce dépôt est développé en mode ouvert, sur une seule plateforme, par un seul responsable et une équipe d’experts et d’exécutants qui se relaient. `main` est le seul état pris en charge. Il n’y a pas de canal de publication, pas de politique de rétroportage et pas d’accord de niveau de service (SLA) ; à la place, il existe un enregistrement : chaque affirmation est associée au code qui la produit, et [docs/experiments](docs/experiments/) contient les spécifications, le rapport et la décision pour chacun.

## Exigences

Blender 5.x, Python 3.11+ avec `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Une installation locale de ComfyUI n’est nécessaire que pour le pinceau d’inpainting. Développé sur une RTX 5090 ; la marge de VRAM est plus importante que la vitesse brute.

Le CI exécute le sous-ensemble hermétique de la suite sur **ubuntu-latest / Python 3.12** avec des installations fixes (`.github/workflows/ci.yml`) ; la couche d’artefacts a besoin des arbres enregistrés sous `E:\AI\training`, qui ne sont pas dans git, donc le CI les désélectionne intentionnellement. Localement, `python -m pytest` exécute les **648** tests et `python -m pytest -m "not artifacts"` exécute les **640** tests reproduits par le CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
