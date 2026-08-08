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

Le style est appliqué **sur l’élément**, dans l’espace de la texture, et non pas peint pour chaque angle de vue, puis assemblé par la suite. Si vous fournissez un modèle en argile aux formes exagérées comme point de départ, le résultat sera une maquette texturée dont la couleur proviendra d’une référence stylisée de cette même maquette, les zones que la référence ne pouvait pas afficher étant remplies à l’aide d’un pinceau de retouche masqué et d’un outil de dilatation tenant compte de la surface.

Il tire son nom des deux aspects du problème : les polygones et la surface qu’ils doivent couvrir.

## Quelle est sa situation actuelle ?

**Quatre éléments ont été acceptés, répartis dans quatre catégories différentes, sans entraîner de décompte de crédits.** Chacun d’eux a été validé par le directeur, selon ses propres critères – soit sur le format GLB, soit sur des feuilles de grand format –, et non en fonction du respect d’une norme prédéfinie.

| sujet | classe | accepté | référence / pinceau / dilatation |
|---|---|---|---|
| **Character (W3)** | humanoïde | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | véhicule, gréement léger | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bête, membrane des ailes | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | objet de scène, rendu proche d’une image 2D, nuances de gris sur fond gris. | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Les échantillons proviennent de zones valides et **ils ne sont pas comparables d’un sujet à l’autre** – un navire dissimule la majeure partie de sa structure au niveau des yeux, tandis qu’un animal n’en cache que la moitié. Évaluez chaque échantillon en fonction de son propre seuil de portée préétabli, par rapport auquel il obtient un résultat de **86 à 93 %** : la différence entre les rangées est géométrique, et non liée à une régression. [Chiffres complets avec leurs dénominateurs](docs/handbook/subjects.md).

**Il s’agit d’un processus en plusieurs étapes, et non d’un simple générateur produisant une seule image.** En contredisant les spécifications sur huit éléments nommés, le modèle génère une image qui obtient un score de **8 sur 8** – la valeur médiane de ΔE est de 46,3 contre 6,2 pour cinq images de référence – tout en conservant l’apparence du même personnage. La structure est maintenue par la grille et les paramètres de contrôle ; les attributs nommés sont déterminés par le modèle.

## Le trajet

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

Étape par étape, avec la justification de chaque étape : **[le manuel](docs/handbook/index.md)**.

## Qu’est-ce qui fait que ça marche ?

Nous avons obtenu six résultats, chacun d’eux nécessitant une expérience et chacun d’eux ayant une portée qui dépasse le sujet qui a permis de l’obtenir. [La version complète, avec les mesures](docs/findings.md).

- **La forme d’abord, le style ensuite.** Les outils de reconstruction interprètent le bruit de surface comme une géométrie. Une argile propre, semblable à une sculpture, avec des plans délibérément exagérés, donne un meilleur résultat en termes de topologie qu’un sprite stylisé ; la version stylisée est générée simultanément et sert de référence pour les couleurs.
- **Définissez le visage, obtenez un visage.** Un cadrage du buste ajoute **3,1 à 4,5 fois** plus de polygones sur la tête, et la différence est structurelle : paupières séparées, sillon frontal, cavités nasales modélisées – ce n’est pas simplement un flou plus prononcé.
- **Les jumeaux appartiennent à une maille, pas à un personnage.** Réutilisez un jumeau sur différentes mailles et la couverture se réduit de **62 % à 22,7 %**, car les bras sont projetés dans l’espace vide à côté du modèle. Générez des jumeaux à partir de la maille que vous allez texturer, à chaque fois.
- **L’identité appartient à l’invite.** Un élément canonique qui n’est pas mentionné dans l’invite apparaît par erreur et disparaîtra de la même manière : cela a été mesuré lorsque des genouillères dorées se sont avérées apparaître uniquement en raison du bruit dans un ControlNet défectueux.
- **Demandez à la géométrie, pas à un seuil.** Le remplacement d’un masque avec le contour exact obtenu par lancer de rayons a amélioré la couverture de référence de **28,4 % à 39,1 %** des texels valides – uniquement additif, sans diffusion, sans utilisation du GPU. La technique de masquage basée sur les coins et la médiane a échoué trois fois ici et est abandonnée.
- **Supprimez ce qu’aucune caméra ne peut voir, à partir de l’atlas et jamais de la maille.** 49 % des texels de l’atlas sont invisibles de l’extérieur ; en excluant ces faces, on réduit l’interpolation de 68 %. Plutôt que de supprimer, il est préférable d’exclure, ce qui rend l’échec impossible au lieu de simplement détectable.

## Qu’est-ce qui n’a pas été résolu ?

Ils sont nommés et décrits en détail, et figurent sur la page d’accueil plutôt que dans une note de bas de page. [Tous se trouvent dans le code](docs/known-defects.md).

- La bande de la lame représente 0,00 % de la référence de l’étape 1 sur les huit caméras : l’acier sur un fond gris est parfaitement aligné avec le seuil de la clé. L’union permet de récupérer 55,72 %.
- Les joints des traits ne sont pas uniformisés. Une limite de provenance présente une variation **5,5 fois** supérieure à celle d’une texture ordinaire ; la région désignée par le réalisateur présente une variation **9,5 fois** supérieure.
- La dilatation se propage entre les îles de l’atlas qui n’ont aucun lien entre elles : 74,9 % des texels dilatés tirent leur couleur d’une autre île, à une distance médiane de 0,177 sur une figure haute de 1,0.
- Chaque reconstruction effectuée sur cet itinéraire est une coquille creuse à double paroi, dont les parois ont environ deux voxels d’épaisseur. Aucun prédicat volumétrique n’est valide pour l’une ou l’autre.

## Comment ce dépôt est géré

Cette approche est tout aussi importante que le processus lui-même, et elle répond à un objectif précis : lors d’une série de dix séances précédentes, chaque participant a évalué son propre travail et rédigé des conclusions qui ont ensuite été présentées comme des faits établis lors de la séance suivante. Rien dans ce cycle ne pouvait être vérifié.

- **Définir les objectifs avant de commencer, faire un compte rendu après, et prendre une décision finale** – et la session qui conçoit une expérience n’évalue jamais ses propres résultats. Vingt expériences sont disponibles dans [les archives](docs/experiments/).
- **Les corrections sont appliquées directement, à côté de la mesure qu’elles ont invalidée**, et non pas par des suppressions discrètes. Six affirmations initiales ont été réfutées lors de la première session, et les six sont toujours accessibles à côté de ce qui les a remplacées.
- **Les échecs restent dans le dépôt avec leur raison.** [`tools/superseded/`](docs/tools.md) n’est pas une archive – chacun peut exécuter ces outils et observer qu’ils échouent de la même manière.
- **Un résultat négatif est un succès total**, il est consigné et clôturé plutôt que d’être ajusté pour atteindre une valeur cible.
- **Les tests sont associés au commit qui modifie le code** – 213 tests réussis, réalisés par deux personnes différentes, avec une intégration continue basée sur les chemins pour les 205 tests hermétiques.
- **Les données peuvent être consultées.** Un index SQLite + FTS5 est appliqué à l’ensemble des données, et il a été vérifié sur quatre ensembles de données. Il a permis de trouver un nombre incorrect dans le texte à trois endroits en comptant directement les données.

## Là où tout se trouve

| | |
|---|---|
| **[Le guide de référence](docs/handbook/index.md)** | le guide : description détaillée de l’itinéraire étape par étape, présentation des thèmes abordés et explication du système de classification. |
| **[Le dossier](docs/experiments/)** | vingt expériences : spécifications, rapport, conclusions et toutes les prédictions formulées avant la mesure. |
| **[Ce que le processus a appris](docs/findings.md)** | les résultats durables et les règles obtenues avec difficulté, en intégralité. |
| **[État de chaque outil](docs/tools.md)** | ce qui fonctionne, ce qui est obsolète et les preuves pour chacun. |
| **[Défauts connus](docs/known-defects.md)** | tout ce qui n’a pas été résolu, mesuré et localisé dans le code. |
| **[Le déroulement, tel qu’il s’est produit](docs/arc-history.md)** | l’historique chronologique, avec les corrections intactes. |
| **[CLAUDE.md](CLAUDE.md)** | comment travailler ici : les rôles, les règles et ce que chacun implique. |

## Position concernant la licence

Chaque étape s’exécute localement et est conforme aux exigences commerciales : SDXL (OpenRAIL++), MV-Adapter (open source), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Exclusions délibérées, avec la justification : **nvdiffrast** (non commercial – appliqué ici par un mécanisme de sécurité structurel, et non par une attestation), **Hunyuan3D-Paint** (licence invalide dans l’UE, au Royaume-Uni et en Corée du Sud), **MVPaint** et **TEXGen** (aucune licence) et **UltraSharp / SUPIR / StableSR** (algorithmes d’amélioration non commerciaux).

## Modèle de confiance et de menace

facet s’exécute entièrement sur votre propre machine : chaque outil est un script que vous exécutez en utilisant des chemins que vous saisissez, la question pertinente n’est donc pas « quelles sont les autorisations demandées par cette application », mais « que font ces scripts sur votre machine ». La réponse est fournie par la mesure, chaque cycle pouvant être répété ; la politique complète figure dans [SECURITY.md](SECURITY.md) :

- **Données concernées :** maillages, textures, images et fichiers JSON sur le disque local, aux chemins que vous indiquez dans la ligne de commande. De plus, `docs/index/facet.db`, qui est *dérivé* – il ne contient rien qui n’était pas déjà un fichier dans ce dépôt, et `facet_index.py build` le régénère à partir de zéro.
- **Données NON concernées :** aucune information d’identification, jamais. Rien ici ne lit, ne stocke ou ne transmet de jeton, de clé ou de mot de passe, et rien de tel n’est présent dans l’arborescence – une recherche a été effectuée pour détecter les clés préfixées par le fournisseur, les GitHub PAT, les jetons Slack, les ID de clé AWS, les blocs de clé privée, les jetons d’authentification et les affectations en ligne `api_key`/`password`, **zéro correspondance**, aucun fichier ressemblant à une information d’identification n’a été détecté.
- **Pas de télémétrie.** Aucune donnée n’est collectée ni envoyée. Il n’y a pas d’option de désactivation car il n’y a rien à désactiver.
- **Sortie réseau :** deux des trente-quatre outils ouvrent un socket – `restylize_views.py` et `texpass_brush.py` – et les deux appellent une API HTTP ComfyUI à l’adresse `--host`, **par défaut `127.0.0.1:8188`**. Rien d’autre dans `tools/` n’effectue d’appel réseau.
- **Autorisations :** utilisateur ordinaire. Pas d’élévation de privilèges, pas d’installation de service, pas d’écritures dans les paramètres système ou le registre.

Trois points critiques sont explicitement mentionnés plutôt que dissimulés, car une note de sécurité qui ne contient que des assurances n’est pas un modèle de menace : **les opérations sur les fichiers ne sont pas exécutées dans un environnement isolé** (un outil écrit à l’endroit indiqué par ses arguments) ; **des chemins locaux absolus sont intégrés dans de nombreux outils et documents** – 114 occurrences dans 26 fichiers, ce ne sont pas des secrets, mais une divulgation de la configuration d’une machine, et c’est pourquoi la plupart des outils ne fonctionneront pas sans modification ailleurs ; et **les erreurs inattendues se manifestent sous forme de traces Python**, sans barrière `--debug` ni format d’erreur structuré. Les arrêts délibérés sont des messages `ANDON:` qui contiennent la mesure qui les a déclenchés. C’est le contrat de l’instrument de recherche, et [SHIP_GATE.md](SHIP_GATE.md) indique précisément à quel moment il cesse d’être suffisant.

**État du support :** ce dépôt est développé en open source, sur une seule machine, par un seul responsable et une équipe de conseillers et d’exécutants qui se relaient. `main` est le seul état pris en charge. Il n’y a pas de canal de publication, pas de politique de rétroportage et pas de SLA – ce qu’il y a à la place, c’est le dossier : chaque affirmation est associée au code qui la produit, et [docs/experiments](docs/experiments/) contient les spécifications, le rapport et les conclusions pour chacune.

## Exigences

Blender 5.x, Python 3.11+ avec `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Une installation locale de ComfyUI est nécessaire uniquement pour le pinceau d’inpainting. Développé sur une RTX 5090 ; la capacité de VRAM est plus importante que la vitesse brute.

La suite hermétique est exécutée dans CI sur **ubuntu-latest / Python 3.12** avec des installations fixes (`.github/workflows/ci.yml`) ; le niveau d’artefacts nécessite les arbres enregistrés sous `E:\AI\training`, qui ne sont pas dans git, de sorte que CI les exclut par conception. Localement, `python -m pytest` exécute les **213** tests et `python -m pytest -m "not artifacts"` exécute les **205** tests reproduits par CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
