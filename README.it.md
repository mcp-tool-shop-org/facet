<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

Lo stile viene applicato **sull'asset**, nello spazio delle texture, e non viene disegnato per ogni singola visualizzazione né assemblato successivamente. Fornendo alla pipeline un modello in argilla con forme esagerate, questa restituirà una mesh texturizzata il cui colore deriva da un riferimento stilizzato di *quella* stessa mesh, con tutte le aree che il riferimento non poteva vedere riempite tramite un pennello per l'inpainting mascherato e una dilatazione consapevole della superficie.

Prende il nome dalle due componenti del problema: i poligoni e la superficie che devono rappresentare.

## Installazione

La pipeline stessa è un insieme di script locali che vengono eseguiti su percorsi specificati dall'utente; clona il repository e leggi [la guida introduttiva](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Due server vengono forniti come pacchetto**: l'indice dei record, in modo che un assistente possa interrogare la cronologia delle prove anziché leggerla, e **a partire dalla versione 0.4.0 il server di misurazione**, in modo che due asset misurati a distanza di mesi utilizzino lo stesso flusso di codice.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` è il server MCP stdio che opera sui record (sei strumenti, con la verifica a quattro punti come superficie di controllo per l'integrità) e `facet-index` è l'indice stesso (`build` / `verify` / `q` / `claims`). Esegui uno dei due all'interno di una copia del repository; `--db` indica un indice diverso.

### Il server di misurazione: nuovo nella versione 0.4.0

`facet-measure` fornisce la **componente numerica** di un confronto e non indica mai se l'output è valido. Ogni pacchetto dati contiene la versione del server, l'hash del file dello strumento e l'hash della configurazione, e `measure_report` **rifiuta** di effettuare confronti tra versioni incompatibili, che è la caratteristica per cui è stato progettato l'intero sistema.

Verificato eseguendo un **comando** anziché `--help`: una mesh di controllo restituisce 786.432 facce con un inviluppo di identità completo su una macchina che non contiene una copia del repository.

**Il risultato dipende da un solo fattore, ovvero la versione di Python:**

| la tua versione di Python | `[measure-full]` ti fornisce |
|---|---|
| **3.11 / 3.12** | **tutti e otto gli strumenti**: `open3d` si installa tramite PyPI |
| **3.13** | quattro strumenti: `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 is the latest *release* and publishes cp38–cp312 wheels with **no sdist**,
so on 3.13 there is nothing on PyPI to install. The extra carries it behind
`python_version < "3.13"`, so the install **succeeds** there and the four geometry tools
exit **`4` REFUSED** naming what they need — rather than the whole install failing.

**Per ottenere tutti e otto gli strumenti su Python 3.13**, Open3D pubblica i pacchetti cp313 più recenti sul suo canale di sviluppo in continuo aggiornamento. Un URL diretto è accettabile nella riga di comando; è vietato solo all'interno dei metadati del pacchetto pubblicato:

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **Su Windows e macOS, i pacchetti di sviluppo hanno il suffisso `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` al momento della stesura) e il nome cambia quando `main` cambia; elenca gli asset nella [versione `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) e seleziona quello più recente. **Questa versione è quella rispetto alla quale sono stati misurati i numeri dipendenti da open3d di questa pipeline**, ed è un limite reale per la comparabilità: l'inviluppo di identità registra l'hash dello strumento, non le sue dipendenze [E31](docs/experiments/E31-ruling.md).

*Fino alla versione 0.3.1, il pacchetto conteneva due file `.py` e nessuno degli strumenti di misurazione, quindi un server di misurazione installato non aveva nulla da eseguire. Nessuno se n'è accorto per quattro versioni perché questo repository È la copia del codice: lo strumento funzionava dove veniva compilato e non era mai stato altrove.*

⚠ **`pip install facet-mcp` era difettoso in tutte le versioni pubblicate fino alla versione 0.3.0 ed è stato corretto nella versione 0.3.1.** Il pacchetto installa `facet_index` come modulo di livello superiore, quindi fino alla versione 0.3.0 includeva, risolveva la posizione del record rispetto a `<venv>/Lib`, che non contiene né il corpus né l'indice, e `build`, `claims` e `q` fallivano tutti se mancava `--db`.
**Sulla versione 0.3.0 o precedente, utilizza il binario `npx` sopra.**

A partire dalla versione 0.3.1, la posizione principale viene risolta **verificando l'esistenza del record** anziché presupponendolo: esegui uno dei due comandi all'interno di una copia del repository e lo troverà; eseguilo da qualsiasi altra posizione ed esso restituirà **`4` RIFIUTATO**, indicando entrambe le directory che ha provato e entrambi i marcatori che ha cercato. `$FACET_INDEX_DB` viene ora letto da entrambi i comandi e seleziona quale *indice*, non quale *corpus*. Misurato su un pacchetto compilato da `main` e installato in un ambiente virtuale pulito [E24](docs/experiments/E24-ruling.md).

*Questo blocco è stato corretto due volte. Inizialmente conteneva `pipx install facet-mcp # o il pacchetto Python direttamente `, until v0.3.0's read-back ran a **verb** instead of `--help`. Successivamente affermava che il pacchetto "funziona solo per `q` e `claims`" - **`claims` non funzionava nemmeno**, come scoperto da E24 eseguendolo. Entrambe le correzioni sono presenti in [known-defects.md](docs/known-defects.md) con le relative misurazioni.*

## La situazione attuale

**Quattro asset accettati, appartenenti a quattro classi di oggetti, senza costi aggiuntivi.** Ognuno è stato valutato dal direttore con il proprio livello di zoom: sul file GLB o su fogli di dimensioni reali, e non tramite una metrica che supera una soglia.

| oggetto | classe | accettato | riferimento / pennello / dilatazione |
|---|---|---|---|
| **Character (W3)** | umanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veicolo, rigging leggero | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | animale, membrane delle ali | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | oggetto di scena, quasi bidimensionale, grigio su grigio | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Le quote sono espresse in texel validi e **non sono comparabili tra oggetti diversi**: una nave nasconde gran parte di sé dalla prospettiva a livello degli occhi e un animale ne nasconde metà. Valuta ciascuno rispetto al proprio limite di copertura pre-registrato, rispetto al quale ottengono un punteggio dell'**86-93%**: la differenza tra le righe è dovuta alla geometria, non alla regressione [Numeri completi con i rispettivi denominatori](docs/handbook/subjects.md).

**Si tratta di una pipeline, non di un generatore a carattere singolo.** Contradici la specifica su otto elementi specifici e il prompt avrà successo in **8 casi su 8**: ΔE mediano pari a 46,3 rispetto a 6,2 su cinque controlli mantenuti; nel frattempo, la figura rimane la stessa. La struttura è mantenuta dalla mesh e dal controllo; gli attributi nominati sono gestiti dal prompt.

## La pipeline

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

Fase per fase, con le motivazioni di ciascuna: **[la guida](docs/handbook/index.md)**.

**Il percorso tratteggiato è nuovo ed è intenzionalmente non continuo.** La prima casella del percorso riporta sempre la scritta *concept di argilla*, e fino ad ora nulla qui lo ha prodotto: ogni pezzo di argilla arrivava manualmente ed era lavorato durante il processo. Ora esiste uno strumento che trasforma un concetto in argilla, e la sua prima versione è stata testata a dimensione reale: posa, protezioni per i polsi, medaglione per la cintura e orlo strappato sono stati tutti applicati; la massa della criniera no; la perdita di colore è stata misurata sull'intero fotogramma con un valore di **C\* p99.9 = 13.15**, su uno sfondo monocromatico uniforme. **Ciò che questa versione non può dimostrare è se la mesh migliora**, ed è l'unica domanda che ne giustifica l'utilizzo, quindi rimane una candidata con le sue prove registrate: **[preparazione del concept](docs/concept-prep.md)**.

## Cosa lo rende efficace

Sei risultati, ciascuno dei quali richiede un esperimento e ciascuno dei quali si generalizza oltre l'oggetto che lo ha prodotto. [La versione completa, con le misurazioni](docs/findings.md).

- **Prima la forma, poi lo stile.** Gli strumenti di ricostruzione interpretano il rumore superficiale come geometria. Un pezzo di argilla pulito e modellato, con piani intenzionalmente esagerati, produce una topologia migliore rispetto a uno sprite stilizzato; la versione stilizzata viene generata contemporaneamente e diventa il riferimento cromatico.
- **Definisci il volto, ottieni un volto.** Un ritaglio del busto aggiunge dal **3,1 al 4,5 volte più poligoni alla testa**, e la differenza è strutturale: palpebre separate, una piega sulla fronte, cavità delle narici modellate, non semplicemente una sfocatura più nitida.
- **Le copie appartengono a una mesh, non a un personaggio.** Riutilizza una copia su diverse mesh e la copertura diminuisce del **62% → 22,7%**, perché le braccia si proiettano in uno spazio vuoto accanto al modello. Genera le copie dalla mesh che stai per texturizzare, ogni volta.
- **L'identità appartiene al prompt.** Un elemento canonico non menzionato nel prompt viene aggiunto accidentalmente e scomparirà allo stesso modo: misurato quando si è scoperto che le placche dorate sulle ginocchia apparivano nell'immagine solo a causa del rumore in un ControlNet difettoso.
- **Chiedi alla geometria, non a una soglia.** La sostituzione di una maschera chiave con l'esatta silhouette ottenuta tramite raycast ha spostato la copertura di riferimento dal **28,4% al 39,1%** dei texel validi: strettamente additivo, nessuna diffusione, nessuna GPU. Il keying basato sull'angolo mediano è fallito tre volte e non viene più utilizzato.
- **Elimina ciò che nessuna telecamera può vedere, dall'atlante e mai dalla mesh.** Il 49% dei texel dell'atlante sono invisibili dall'esterno; l'esclusione di questi volti riduce l'interpolazione del 68%. L'esclusione, anziché l'eliminazione, rende il fallimento impossibile invece che semplicemente rilevabile.

## Cosa non è stato risolto

Indicato e misurato, nella pagina principale piuttosto che in una nota a piè di pagina. [Tutti, situati nel codice](docs/known-defects.md).

- **Alcune aree superficiali visibili vengono mappate nello spazio dell'atlante, ma non vengono mai scritte durante il baking**, e vengono renderizzate come il nero predefinito non modificato dell'immagine. Lo strumento di baking di Blender utilizza un campionamento al centro del texel, quindi un triangolo che non si sovrappone a nessun centro texel rimane vuoto: i suoi stessi sviluppatori
[hanno identificato il meccanismo e hanno implementato una correzione](https://projects.blender.org/blender/blender/pulls/161752)
due settimane dopo la build su cui sono stati misurati tutti i numeri qui presenti. È una proprietà del percorso, non di un singolo oggetto: misurato su un asset, **non misurato sugli altri quattro**.
- **La fascia della lama occupa lo 0,00% del riferimento nella fase 1** su tutte e otto le telecamere: l'acciaio su uno sfondo grigio si trova esattamente sulla soglia chiave. L'unione salva il 55,72%.
- **Le giunture delle pennellate non sono livellate.** Un confine di provenienza presenta una variazione della texture pari a **5,5 volte**; la regione che il direttore ha identificato presenta una variazione pari a **9,5 volte**.
- **La dilatazione si estende tra isole dell'atlante non correlate**: il 74,9% dei texel dilatati prendono il loro colore da un'altra isola, con una distanza mediana di 0,177 su una figura alta 1,0. ⚠ **Questa percentuale si riferisce ai texel dell'atlante e non è un'affermazione su ciò che vede una telecamera**: la dilatazione rappresenta il 26,95% dell'atlante renderizzato e il **4,95% dei pixel della figura renderizzata**, con un rapporto di 0,18. La pittura si trova in grandi mappe, i buchi in quelle piccole, quindi un texel dilatato è economico nello spazio dello schermo.
- **⚑ Il difetto che determina l'accettazione è portato dalla PITTURA, non da alcun riempimento**: regioni che presentano il colore di un altro materiale, che nessuna statistica sulle macchie può rilevare. Misurato in tre modi, in tre sessioni e in tre spazi: **91,05% `reference` trasportato con un arricchimento di 0,99**, esattamente al tasso base; la stessa classe nel verde del tessuto **68,46% `reference`**; e su una sottile lama, i texel dipinti sulla superficie **18,77%** sono contaminati rispetto al riempimento della dilatazione, che è pari al **5,55%**. Il riempimento deriva correttamente dal vicino dipinto più vicino, e quel vicino è già errato. La miscela stessa è una suddivisione a due bande non documentata
(`M + gaussian_blur_σ16(B − M)`) che misura il **peggiore tra quattro** valori alternativi sugli stessi punti.
- **Le viste non sono mai indipendenti, il che limita ogni correzione della fusione.** Per ogni gruppo di difetti, il **100% delle facce con due o più telecamere contribuenti ha tutte le telecamere all'interno di un arco di 90°** (mediana 45°) e il 21% delle facce difettose sono viste da una sola telecamera. Le viste adiacenti, sotto controlli quasi identici, falliscono insieme, quindi i guadagni multi-vista pubblicati dalla fotogrammetria non si trasferiscono qui così come sembrano.
- **Ogni ricostruzione in questo percorso è un guscio cavo a doppia parete**, con pareti di circa due voxel. Nessun predicato volumetrico è valido su uno di essi.

## Come viene eseguito questo repository

La disciplina è tanto importante quanto la pipeline, ed esiste per un motivo: una fase precedente ha eseguito dieci sessioni in cui ogni sessione ha valutato il proprio output e ha scritto conclusioni che la sessione successiva ha considerato come fatti consolidati. Nulla in quel ciclo era verificabile.

- **Definizione prima del lavoro, relazione dopo, decisione finale**: e la sessione che progetta un esperimento non valuta mai i propri risultati. Quaranta esperimenti sono disponibili in [questa sezione](docs/experiments/).
- **Le correzioni vengono applicate immediatamente, accanto alla misurazione che le ha invalidate**, e non come semplici eliminazioni. Solo nella sessione iniziale, sei affermazioni preesistenti sono state confutate, e tutte e sei sono ancora visibili accanto a ciò che le ha sostituite.
- **I fallimenti rimangono nel repository insieme alla loro motivazione.** [`tools/superseded/`](docs/tools.md) non è un archivio: chiunque può eseguire questi strumenti e osservare i loro fallimenti nello stesso modo.
- **Un risultato negativo è un successo completo**, viene segnalato e chiuso anziché essere modificato per raggiungere un valore specifico.
- **I test sono associati al commit che modifica il codice**: 1174 risultati positivi ottenuti da due persone, con CI basata sui percorsi per i 1128 elementi "ermetici".
- **La registrazione è consultabile.** Un indice SQLite + FTS5 sull'intero percorso, verificato su quattro livelli. Ha individuato un conteggio che il testo presentava in modo errato in tre siti, contando direttamente la registrazione stessa.

## Dove tutto è..

| | |
|---|---|
| **[Il manuale](docs/handbook/index.md)** | la guida: il percorso passo dopo passo, gli argomenti, il sistema di profili. |
| **[Preparazione del concetto](docs/concept-prep.md)** | il candidato "hop" per la preparazione dell'argilla: il suo percorso iniziale (Gate 0), il suo posizionamento e l'elemento di licenza che abilita. |
| **[La registrazione](docs/experiments/)** | quaranta esperimenti: definizione, relazione, decisione finale e ogni previsione dichiarata prima della misurazione. |
| **[Cosa ha imparato il percorso](docs/findings.md)** | i risultati duraturi e le regole ottenute con fatica, nella loro interezza. |
| **[Stato di ogni strumento](docs/tools.md)** | cosa funziona, cosa è stato sostituito e le prove per ciascuno. |
| **[Difetti noti](docs/known-defects.md)** | tutto ciò che non è stato risolto, misurato e localizzato nel codice. |
| **[L'arco temporale, come si è svolto](docs/arc-history.md)** | la cronologia degli eventi, con le correzioni intatte. |
| **[CLAUDE.md](CLAUDE.md)** | come lavorare qui: i ruoli, le regole e il costo di ciascuno. |

## Posizione della licenza

Ogni fase viene eseguita in locale e nel rispetto delle normative commerciali: SDXL (OpenRAIL++), MV-Adapter (open source), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Esclusi intenzionalmente, con la relativa motivazione: **nvdiffrast** (non commerciale, applicato qui tramite un meccanismo di sicurezza strutturale, non tramite attestazione), **Hunyuan3D-Paint** (licenza non valida nell'UE, nel Regno Unito e in Corea del Sud), **MVPaint** e **TEXGen** (nessuna licenza) e **UltraSharp / SUPIR / StableSR** (strumenti di upscaling non commerciali).

**I confini dell'affermazione, dichiarati anziché lasciati alla scoperta.** Descrive il **percorso registrato**: le fasi nel diagramma sopra, dall'immagine al 3D. La fase candidata per la preparazione dell'argilla a monte attualmente viene eseguita su un'API cloud chiusa i cui termini questo repository **non ha verificato**, quindi nessuna affermazione di licenza qui copre un elemento creato da una delle sue argille. Si tratta di un aspetto aperto con un percorso definito per risolverlo: il modello locale corretto dal punto di vista della licenza è **Qwen-Image-Edit (Apache-2.0)** e **FLUX.1-Kontext [dev] è escluso per gli stessi motivi di nvdiffrast**: pesi non commerciali. Entrambi sono stati verificati rispetto al catalogo dei modelli dello studio anziché richiamati; la motivazione è disponibile in [concept prep](docs/concept-prep.md).

## Modello di fiducia e di minaccia

ogni fase viene eseguita interamente sulla propria macchina: ogni strumento è uno script che si esegue su percorsi digitati, quindi la domanda utile non è *quali autorizzazioni richiede questa applicazione*, ma *cosa fanno questi script alla tua macchina*. La risposta viene fornita tramite misurazione, con ogni ciclo ripetibile; la politica completa è disponibile in [SECURITY.md](SECURITY.md):

- **Dati interessati:** mesh, texture, immagini e JSON su disco locale, nei percorsi specificati nella riga di comando. Inoltre `docs/index/facet.db`, che è *derivato*: non contiene nulla che non fosse già un file in questo repository e `facet_index.py build` lo rigenera da zero.
- **Dati NON interessati:** nessuna credenziale, mai. Nessuno di questi elementi legge, memorizza o trasmette token, chiavi o password, e nessuno è presente nell'albero: sono stati eseguiti controlli per individuare chiavi con prefisso del provider, GitHub PAT, token Slack, ID chiave AWS, blocchi di chiavi private, token bearer e assegnazioni inline `api_key`/`password`; **nessuna corrispondenza**, nessun file che assomigli a una credenziale è stato rilevato.
- **Nessun telemetria.** Nessuna raccolta o trasmissione di dati. Non esiste un'opzione per disattivare perché non c'è nulla da disattivare.
- **Traffico di rete:** due degli strumenti su trentasei aprono una connessione socket: `restylize_views.py` e `texpass_brush.py`, entrambi chiamano un'API HTTP ComfyUI all'indirizzo `--host`, **valore predefinito `127.0.0.1:8188`**. Nessun altro elemento in `tools/` effettua chiamate di rete.
- **Autorizzazioni:** utente standard. Nessuna elevazione dei privilegi, nessuna installazione del servizio, nessuna scrittura nelle impostazioni di sistema o nel registro di sistema.

Tre spigoli vivi vengono evidenziati anziché eliminati, perché una nota di sicurezza che elenca solo delle rassicurazioni non è un modello di minaccia: **le operazioni sui file non sono eseguite in un ambiente isolato** (uno strumento scrive ovunque indichino i suoi argomenti); **i percorsi locali assoluti sono incorporati in molti strumenti e documenti** — 114 occorrenze in 26 file, non si tratta di segreti ma della divulgazione del layout di una macchina e del motivo per cui la maggior parte degli strumenti non funzionerà senza modifiche altrove; e **i fallimenti imprevisti vengono visualizzati come tracce di Python nei 36 script di ricerca non pubblicati**, senza alcun filtro `--debug`. Le interruzioni deliberate sono messaggi `ANDON:` che contengono la misurazione che le ha attivate. Questo è il contratto dello strumento di ricerca e [SHIP_GATE.md](SHIP_GATE.md) registra esattamente quando smette di essere sufficiente, cosa che per i due comandi *installa*, è avvenuta alla versione 0.2.0: `facet-index` e `facet-mcp` restituiscono `0` ok / `1` errore utente / `2` errore in fase di esecuzione — e, poiché [E22](docs/experiments/E22-ruling.md), **`4` RIFIUTATO** per un filtro attivato o una sezione `verify` non funzionante, il che significa che lo strumento funziona e ti avvisa di non procedere anziché generare un errore in fase di esecuzione. Tutti rifiutano con un messaggio di errore strutturato che indica il passaggio successivo anziché una traccia ([E21](docs/experiments/E21-cli-contract-report.md)).

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

**Stato del supporto:** questo repository viene sviluppato in modo aperto, su un'unica piattaforma, da un unico responsabile e con sessioni a rotazione di consulenti ed esecutori. `main` è l'unico stato supportato. Non esiste un canale di rilascio, una politica di backporting o un SLA; ciò che esiste invece è la registrazione: ogni affermazione si trova accanto al codice che la produce e [docs/experiments](docs/experiments/) contiene le specifiche, il rapporto e la decisione per ciascuna di esse.

## Requisiti

Blender 5.x, Python 3.11+ con `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. È necessaria un'installazione locale di ComfyUI solo per il pennello di inpainting. Sviluppato su una RTX 5090; la quantità di VRAM disponibile è più importante della velocità pura.

Il CI esegue il sottoinsieme ermetico della suite su **ubuntu-latest / Python 3.12** con installazioni fisse (`.github/workflows/ci.yml`); lo strato degli artefatti richiede gli alberi registrati in `E:\AI\training`, che non sono presenti in git, quindi il CI li esclude intenzionalmente. Localmente, `python -m pytest` esegue tutti i **1174** test e `python -m pytest -m "not artifacts"` esegue i **1128** test riprodotti dal CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
