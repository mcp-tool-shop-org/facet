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

Il a été nommé en fonction des deux aspects du problème : les polygones et la forme qu’ils doivent conserver.

## Installation

La chaîne elle-même est un ensemble de scripts locaux que vous exécutez sur les chemins que vous tapez — clonez le dépôt et lisez [comment démarrer](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**L’index des enregistrements est fourni sous forme de package**, afin qu’un assistant puisse interroger la chaîne de preuves au lieu de la lire :

```bash
npx @mcptoolshop/facet          # zero-prerequisite; verified binary, no Python needed
pipx install facet-mcp          # or the Python package directly
```

Deux commandes sont fournies : `facet-mcp`, le serveur MCP stdio (six outils, dont la vérification à quatre points comme surface de santé qui refuse), et `facet-index` (`build` / `verify` / `q` / `claims`). Indiquez l’un ou l’autre vers un index avec `--db` ou `$FACET_INDEX_DB`.

## Sa position actuelle

**Quatre éléments acceptés, répartis dans quatre classes de sujets, sans coût.** Chacun a été validé par le directeur en utilisant son propre niveau de zoom — sur le fichier GLB ou sur des feuilles de taille réelle — et non en fonction d’une valeur seuil.

| sujet | classe | accepté | référence / pinceau / dilatation |
|---|---|---|---|
| **Character (W3)** | humanoïde | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | véhicule, armature fine | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bête, membranes des ailes | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | accessoire, quasi-2D, gris sur gris | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Les données sont constituées de texels valides et **elles ne sont pas comparables entre les sujets** — un vaisseau cache la majeure partie de lui depuis le niveau des yeux et un animal en cache la moitié. Analysez chaque élément par rapport à son propre seuil prédéfini, ce qui donne un résultat de **86 à 93 %** : la différence entre les lignes est géométrique, et non une régression. [Chiffres complets avec leurs
dénominateurs](docs/handbook/subjects.md).

**Il s’agit d’une chaîne de traitement, et non d’un générateur à un seul caractère.** Contredisez la spécification sur huit éléments nommés, et l’invite remporte **8 sur 8** — ΔE médian de 46,3 contre 6,2 sur cinq contrôles maintenus — alors que la figure reste la même. La structure est assurée par la maille et le contrôle ; les attributs nommés sont liés à l’invite.

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

Six découvertes, chacune d’entre elles nécessitant une expérience et chacune d’entre elles s’appliquant au-delà du sujet qui l’a produite. [La version longue, avec les
mesures](docs/findings.md).

- **D’abord la forme, puis le style.** Les outils de reconstruction interprètent le bruit de surface comme une géométrie. Une argile propre, semblable à une sculpture et dotée de plans délibérément exagérés, donne un meilleur résultat en termes de topologie qu’un sprite stylisé ; le jumeau stylisé est généré simultanément et devient la référence de couleur.
- **Définissez le visage, obtenez un visage.** Un recadrage du buste place **3,1 à 4,5 fois** plus de polygones sur la tête, et la différence est structurelle — paupières séparées, sillon frontal, cavités des narines modélisées — et non une flou plus prononcé.
- **Les jumeaux appartiennent à une maille, et non à un personnage.** Réutilisez un jumeau dans différentes mailles et la couverture diminue de **62 % à 22,7 %**, car les bras se projettent dans l’espace vide à côté du modèle. Générez des jumeaux à partir de la maille que vous allez texturer, à chaque fois.
- **L’identité appartient à l’invite.** Un élément canonique non nommé dans l’invite apparaît par hasard et disparaîtra de la même manière — mesuré lorsque les plaques de genoux dorées se sont avérées n’apparaître dans l’image que grâce au bruit d’un ControlNet défectueux.
- **Demandez à la géométrie, et non une valeur seuil.** Le remplacement d’un masque clé par le contour exact du lancer de rayons a déplacé la couverture de référence de **28,4 % à 39,1 %** des texels valides — strictement additif, sans diffusion, sans GPU. La méthode de masquage basée sur les coins a échoué trois fois ici et est abandonnée.
- **Supprimez ce qu’aucune caméra ne peut voir, à partir de l’atlas et jamais de la maille.** 49 % des texels de l’atlas sont invisibles depuis l’extérieur ; l’exclusion de ces faces réduit l’interpolation de **68 %**. L’exclusion plutôt que la suppression rend l’échec impossible au lieu d’être simplement détectable.

## Ce qui n’est pas résolu

Nommé et mesuré, sur la page de garde plutôt que dans une note de bas de page. [Tous, situés dans le
code](docs/known-defects.md).

- **La bande de lame représente 0 % de la référence de l’étape 1** sur les huit caméras — l’acier sur un fond gris se situe exactement au seuil du masque. L’union sauve 55,72 %.
- **Les joints des traits ne sont pas uniformisés.** Une limite de provenance représente **5,5 fois** la variation normale de la texture ; la région que le directeur a nommée représente **9,5 fois**.
- **La dilatation déborde entre les îles d’atlas non liées** — 74,9 % des texels dilatés tirent leur couleur d’une autre île, avec une distance médiane de 0,177 sur une figure de hauteur 1,0.
- **Chaque reconstruction dans cette chaîne est une double coque creuse**, les parois faisant environ deux voxels. Aucune condition volumétrique n’est valide pour l’un d’eux.

## Comment ce dépôt est exécuté

La discipline est aussi importante que la chaîne de traitement, et elle existe pour une raison : une série précédente a duré dix sessions au cours desquelles chaque session a évalué sa propre production et a rédigé des conclusions que la session suivante a lues comme un fait établi. Rien dans cette boucle n’était vérifiable.

- **Définir les spécifications avant le travail, rédiger un rapport après, et établir une conclusion finale** — et la session qui conçoit une expérience n’évalue jamais ses propres résultats. Vingt expériences sont disponibles dans [les archives](docs/experiments/).
- **Les corrections sont intégrées en place, à côté de la mesure qui les a invalidées**, et non sous forme de suppressions discrètes. Six affirmations initiales ont été réfutées lors de la session initiale, et les six sont toujours consultables à côté de ce qui les a remplacées.
- **Les échecs restent dans le dépôt avec leur raison.** [`tools/superseded/`](docs/tools.md) n’est pas une archive — chacun peut exécuter ces outils et observer qu’ils échouent de la même manière.
- **Un résultat négatif est un succès total**, qui est rapporté et clôturé plutôt que modifié pour atteindre une valeur cible.
- **Les tests sont associés au commit qui modifie le code** — 218 tests réussis avec deux personnes, avec une intégration continue basée sur les chemins d’accès pour les 210 tests hermétiques.
- **Les archives peuvent être consultées.** Un index SQLite + FTS5 est appliqué à l’ensemble des données, et vérifié sur quatre ensembles de données. Il a identifié un nombre de résultats que le texte avait mal indiqué à trois endroits, en comptant les enregistrements eux-mêmes.

## Où tout se trouve :

| | |
|---|---|
| **[Le manuel](docs/handbook/index.md)** | le guide — le déroulement étape par étape, les sujets, le système de profilage |
| **[Les archives](docs/experiments/)** | vingt expériences : spécifications, rapport, conclusion et chaque prédiction formulée avant la mesure |
| **[Ce que le processus a appris](docs/findings.md)** | les conclusions durables et les règles obtenues avec difficulté, en intégralité |
| **[État de chaque outil](docs/tools.md)** | ce qui fonctionne, ce qui est obsolète et les preuves pour chacun |
| **[Défauts connus](docs/known-defects.md)** | tout ce qui n’a pas été résolu, mesuré et localisé dans le code |
| **[Le déroulement, tel qu’il s’est produit](docs/arc-history.md)** | l’historique chronologique, avec les corrections intactes |
| **[CLAUDE.md](CLAUDE.md)** | comment travailler ici — les rôles, les règles et ce que chacun implique |

## Position concernant la licence

Chaque étape s’exécute localement et est conforme aux exigences commerciales : SDXL (OpenRAIL++), MV-Adapter (open source), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Exclusions délibérées, avec la raison : **nvdiffrast** (non commercial — appliqué ici par un mécanisme de sécurité structurel, et non par une attestation), **Hunyuan3D-Paint** (licence invalide dans l’UE, au Royaume-Uni et en Corée du Sud), **MVPaint** et **TEXGen** (aucune licence) et **UltraSharp / SUPIR / StableSR** (algorithmes d’amélioration non commerciaux).

## Modèle de confiance et de menace

facet s’exécute entièrement sur votre propre machine — chaque outil est un script que vous exécutez sur des chemins que vous saisissez, la question pertinente n’est donc pas *quelles sont les autorisations demandées par cette application*, mais *ce que font ces scripts sur votre machine*. La réponse est fournie par la mesure, et chaque cycle peut être répété ; la politique complète se trouve dans [SECURITY.md](SECURITY.md) :

- **Données concernées :** maillages, textures, images et fichiers JSON sur le disque local, aux chemins que vous indiquez dans la ligne de commande. De plus, `docs/index/facet.db`, qui est *dérivé* — il ne contient rien qui n’était pas déjà un fichier dans ce dépôt, et `facet_index.py build` le régénère à partir de zéro.
- **Données NON concernées :** aucune information d’identification, jamais. Rien ici ne lit, ne stocke ou ne transmet de jeton, de clé ou de mot de passe, et rien de tel n’est présent dans l’arborescence — une recherche a été effectuée pour détecter les clés préfixées par le fournisseur, les GitHub PAT, les jetons Slack, les ID de clé AWS, les blocs de clé privée, les jetons d’authentification et les affectations en ligne `api_key`/`password`, **zéro correspondance**, aucun fichier ressemblant à une information d’identification n’a été détecté.
- **Pas de télémétrie.** Aucune donnée n’est collectée ni envoyée. Il n’y a pas d’option de désactivation car il n’y a rien à désactiver.
- **Échange réseau :** deux des trente-quatre outils ouvrent une connexion — `restylize_views.py` et `texpass_brush.py` — et les deux appellent l’API HTTP ComfyUI à `--host`, **par défaut `127.0.0.1:8188`**. Rien d’autre dans `tools/` n’effectue d’appel réseau.
- **Autorisations :** utilisateur standard. Aucune élévation de privilèges, aucune installation de service, aucune écriture dans les paramètres système ou le registre.

Trois points critiques sont divulgués plutôt que dissimulés, car une note de sécurité qui ne contient que des assurances n’est pas un modèle de menace : **les opérations sur les fichiers ne sont pas exécutées dans un environnement isolé** (un outil écrit à l’endroit indiqué par ses arguments) ; **des chemins d’accès locaux absolus sont intégrés dans de nombreux outils et documents** — 114 occurrences dans 26 fichiers, ce ne sont pas des secrets mais une divulgation de la configuration d’une machine, et la raison pour laquelle la plupart des outils ne fonctionneront pas sans modification ailleurs ; et **les échecs inattendus se manifestent sous forme de traces Python**, sans passerelle `--debug` ni format d’erreur structuré. Les arrêts délibérés sont des messages `ANDON:` qui contiennent la mesure qui les a déclenchés. C’est le contrat de l’instrument de recherche, et [SHIP_GATE.md](SHIP_GATE.md) indique exactement quand il cesse d’être suffisant.

**État du support :** ce dépôt est développé en mode ouvert, sur une seule machine, par un seul responsable et une paire rotative de sessions de conseil et d’exécution. `main` est le seul état pris en charge. Il n’y a pas de canal de publication, pas de politique de rétroportage et pas de SLA — ce qu’il y a à la place, c’est l’historique : chaque affirmation se trouve à côté du code qui la produit, et [docs/experiments](docs/experiments/) contient les spécifications, le rapport et la conclusion pour chacun.

## Exigences

Blender 5.x, Python 3.11+ avec `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Une installation locale de ComfyUI est nécessaire uniquement pour le pinceau d’inpainting. Développé sur une RTX 5090 ; la capacité de la VRAM compte plus que la vitesse brute.

L’intégration continue exécute l’ensemble hermétique de tests sur **ubuntu-latest / Python 3.12** avec des installations fixes (`.github/workflows/ci.yml`) ; le niveau d’artefacts nécessite les arbres enregistrés sous `E:\AI\training`, qui ne sont pas dans git, de sorte que l’intégration continue les désactive par conception. Localement, `python -m pytest` exécute les **218** tests et `python -m pytest -m "not artifacts"` exécute les **210** tests reproduits par l’intégration continue.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
