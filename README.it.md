<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.md">English</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

Lo stile viene applicato **sull'asset**, nello spazio della texture, e non viene "dipinginto" per ogni vista e poi assemblato successivamente. Fornisci alla pipeline un modello in argilla con forme esagerate e questa restituirà una mesh texturizzata il cui colore deriva da un riferimento stilizzato di *quella* mesh, con tutto ciò che il riferimento non poteva vedere riempito tramite un pennello per l'inpainting mascherato e una dilatazione consapevole della superficie.

Prende il nome dalle due metà del problema: i poligoni e la faccia che devono rappresentare.

## Installa

La pipeline stessa è un insieme di script locali che vengono eseguiti su percorsi specificati dall'utente; clona il repository e leggi [la guida introduttiva](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Due server vengono forniti come pacchetto**: l'indice dei record, in modo che un assistente possa interrogare la traccia delle prove anziché leggerla, e **a partire dalla versione 0.4.0 il server di misurazione**, in modo che due asset misurati a distanza di mesi utilizzino lo stesso flusso di codice.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` è il server MCP stdio che opera sui record (sei strumenti, con la verifica a quattro punti come superficie di controllo per l'integrità) e `facet-index` è l'indice stesso (`build` / `verify` / `q` / `claims`). Esegui uno dei due all'interno di una copia del repository; `--db` indica un indice diverso.

### Il server di misurazione: nuovo nella versione 0.4.0

`facet-measure` fornisce la **parte numerica** di un confronto e non indica mai se l'output è valido. Ogni payload contiene la versione del server, l'hash del file dello strumento e un hash della configurazione, e `measure_report` **rifiuta** di effettuare confronti tra versioni incompatibili, che è la caratteristica per cui è stato progettato l'intero sistema.

Verificato eseguendo un **comando** anziché `--help`: una mesh di controllo restituisce 786.432 facce con un inviluppo di identità completo su una macchina che non ha una copia del repository.

**Il risultato dipende da una sola cosa, ovvero dalla tua versione di Python:**

| la tua versione di Python | `[measure-full]` ti fornisce |
|---|---|
| **3.11 / 3.12** | **tutti e otto gli strumenti**: `open3d` si installa tramite PyPI |
| **3.13** | quattro strumenti: `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 è l'ultima *versione* e pubblica i pacchetti cp38–cp312 senza **sdist**, quindi sulla versione 3.13 non c'è nulla su PyPI da installare. Il pacchetto aggiuntivo lo include insieme a `python_version < "3.13"`, in modo che l'installazione **riesca** e i quattro strumenti di geometria restituiscano **`4` RIFIUTATO**, indicando ciò di cui hanno bisogno, anziché far fallire l'intera installazione.

**Per ottenere tutti gli otto strumenti su Python 3.13**, Open3D pubblica i pacchetti cp313 più recenti sul suo canale di sviluppo in continuo aggiornamento. Un URL diretto è valido sulla riga di comando; è consentito solo all'interno dei metadati del pacchetto pubblicato:

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **Su Windows e macOS, i pacchetti di sviluppo hanno il suffisso `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` al momento della scrittura) e il nome cambia quando `main` cambia; elenca gli asset nella [versione `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) e prendi quello più recente. **Questa versione è quella rispetto alla quale sono stati misurati i numeri dipendenti da open3d di questa pipeline**, ed è un limite reale di comparabilità: l'inviluppo di identità registra l'hash dello strumento, non le sue dipendenze — [E31](docs/experiments/E31-ruling.md).

*Fino alla versione 0.3.1, il pacchetto conteneva due file `.py` e nessuno degli strumenti di misurazione, quindi un server di misurazione installato non aveva nulla da eseguire. Nessuno se n'è accorto per quattro versioni perché questo repository È la copia del codice: lo strumento funzionava dove veniva compilato e non era mai stato altrove.*

⚠ **`pip install facet-mcp` era difettoso in tutte le versioni pubblicate fino alla versione 0.3.0 ed è stato corretto nella versione 0.3.1.** Il pacchetto installa `facet_index` come modulo di livello superiore, quindi fino alla versione 0.3.0 includeva, risolveva la posizione del record rispetto a `<venv>/Lib`, che non contiene né il corpus né l'indice, e `build`, `claims` e `q` fallivano tutti senza `--db`.
**Sulla versione 0.3.0 o precedente, utilizza il binario `npx` sopra.**

Dalla versione 0.3.1, la radice viene risolta **verificando l'esistenza del record** anziché presupponendolo: esegui uno dei due comandi all'interno di una copia del repository e lo troverà; eseguilo da qualsiasi altra posizione ed esso restituirà **`4` RIFIUTATO**, indicando entrambe le directory che ha provato e entrambi i marcatori che ha cercato. `$FACET_INDEX_DB` viene ora letto da entrambi i comandi e seleziona quale *indice*, non quale *corpus*. Misurato su un pacchetto compilato da `main` e installato in un ambiente virtuale pulito — [E24](docs/experiments/E24-ruling.md).

*Questo blocco è stato corretto due volte. Inizialmente conteneva `pipx install facet-mcp # o il pacchetto Python direttamente`, until v0.3.0's read-back ran a **verb** instead of `--help`.
Successivamente, affermava che il pacchetto "funziona solo per `q` e `claims`" — **`claims` non funzionava nemmeno**, cosa che E24 ha scoperto eseguendolo. Entrambe le correzioni sono presenti in [known-defects.md](docs/known-defects.md) con le relative misurazioni.*

## La situazione attuale

**Quattro asset accettati, appartenenti a quattro classi di oggetti, senza costi aggiuntivi.** Ognuno è stato valutato dal direttore con il proprio livello di zoom: sul file GLB o su fogli di dimensioni reali, e non tramite una metrica che supera una soglia.

| oggetto | classe | accettato | riferimento / pennello / dilatazione |
|---|---|---|---|
| **Character (W3)** | umanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veicolo, rigging leggero | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | animale, membrane delle ali | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | oggetto di scena, quasi bidimensionale, grigio su grigio | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Le quote sono espresse in texel validi e **non sono comparabili tra oggetti diversi**: una nave nasconde gran parte di sé dalla prospettiva a livello degli occhi e un animale ne nasconde metà. Valuta ciascuno rispetto al proprio limite di copertura pre-registrato, rispetto al quale ottengono un punteggio dell'**86–93%**: la differenza tra le righe è data dalla geometria, non da una regressione. [Numeri completi con i rispettivi denominatori](docs/handbook/subjects.md).

**Si tratta di una pipeline, non di un generatore a carattere singolo.** Contradici la specifica su otto elementi specifici e il prompt avrà successo in **8 casi su 8**: ΔE mediano pari a 46,3 rispetto a 6,2 su cinque controlli mantenuti; nel frattempo, la figura rimane la stessa. La struttura è mantenuta dalla mesh e dal controllo; gli attributi denominati sono gestiti dal prompt.

**La questione relativa al proiettore è stata chiusa il 16 agosto 2026** ([E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
Le otto immagini **compongono**: ricostruite a partire dal set di dati per ogni inquadratura, utilizzando
i pesi relativi al bordo × orientamento × visibilità; l'atlante genera il risultato desiderato dal direttore, che lo definisce *"decisamente migliore"* e poi *"ottimo"*, rispetto a un atlante già esistente la cui configurazione stava causando problemi di rendering. La sequenza di operazioni che ha portato a questo risultato è disponibile in `tools/`
(`emit_view_aovs`, `s3_composite`, `flow_estimate`, `s3_run`, `s3_sheet`,
`atlas_from_aovs`, `twin_mesh_warp`), cinque delle sette immagini sono state create da un canale esterno
le cui specifiche di calibrazione hanno dato risultati positivi **in tutti i casi**, e ogni immagine è stata verificata prima di essere utilizzata. Ciò che resta è descritto di seguito, senza nascondere nulla: una classe di poligoni utilizzati per il riempimento, attualmente in fase di analisi; una superficie mai vista prima, in attesa di una definizione precisa; e la configurazione standard, definita dal direttore come l'elemento cruciale.

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

**Il percorso tratteggiato è nuovo ed è intenzionalmente non continuo.** La prima casella del percorso riporta sempre la scritta *concept di argilla*, e fino ad ora nulla qui lo ha prodotto: ogni pezzo di argilla arrivava manualmente ed era lavorato durante il processo. Ora esiste uno strumento che trasforma un concetto in argilla, e la sua prima versione è stata testata a dimensioni reali: posa, protezioni per i polsi, medaglione per la cintura e orlo strappato sono stati tutti utilizzati; la massa della criniera no; la perdita di colore è stata misurata sull'intero fotogramma con un valore di **C\* p99.9 = 13.15**, su uno sfondo monocromatico uniforme. **Ciò che questa versione non può dimostrare è se la mesh migliora**, ed è l'unica domanda che ne determina l'utilità, quindi rimane una candidata con le sue prove registrate: **[preparazione del concept](docs/concept-prep.md)**.

## Cosa lo rende efficace

Sei risultati, ciascuno dei quali richiede un esperimento e ciascuno dei quali si generalizza oltre l'oggetto che lo ha prodotto. [La versione completa, con le misurazioni](docs/findings.md).

- **Prima la forma, poi lo stile.** Gli strumenti di ricostruzione interpretano il rumore superficiale come geometria. Un modello di argilla pulito e con piani deliberatamente esagerati produce una topologia migliore rispetto a uno sprite stilizzato; la versione stilizzata viene generata contemporaneamente e diventa il riferimento cromatico.
- **Definisci il volto, ottieni un volto.** Un ritaglio del busto aggiunge dal **3,1 al 4,5 volte più poligoni alla testa**, e la differenza è strutturale: palpebre separate, una piega sulla fronte, cavità delle narici modellate, non semplicemente una sfocatura più nitida.
- **Le copie appartengono a una mesh, non a un personaggio.** Riutilizza una copia su diverse mesh e la copertura diminuisce del **62% → 22,7%**, perché le braccia si proiettano in uno spazio vuoto accanto al modello. Genera le copie dalla mesh che stai per texturizzare, ogni volta.
- **L'identità appartiene al prompt.** Un elemento canonico non menzionato nel prompt viene aggiunto accidentalmente e scomparirà allo stesso modo: misurato quando si è scoperto che le placche dorate sulle ginocchia apparivano nell'immagine solo a causa del rumore in un ControlNet difettoso.
- **Chiedi alla geometria, non a una soglia.** La sostituzione di una maschera chiave con l'esatta silhouette ottenuta tramite raycast ha spostato la copertura di riferimento dal **28,4% al 39,1%** dei texel validi: strettamente additivo, nessuna diffusione, nessuna GPU. Il keying basato sull'angolo mediano è fallito tre volte e non viene più utilizzato.
- **Elimina ciò che nessuna telecamera può vedere, dall'atlante e mai dalla mesh.** Il 49% dei texel dell'atlante sono invisibili dall'esterno; l'esclusione di questi volti riduce l'interpolazione del 68%. L'esclusione anziché l'eliminazione rende il fallimento impossibile invece che semplicemente rilevabile.

## Cosa non è stato risolto

Indicato e misurato, nella pagina principale piuttosto che in una nota a piè di pagina. [Tutti, situati nel codice](docs/known-defects.md).

- **Alcune superfici visibili vengono mappate nello spazio dell'atlante, ma non vengono mai scritte**, e vengono renderizzate con il colore nero predefinito dell'immagine. Il motore di rendering di Blender utilizza un campionamento centrato sui texel, quindi un triangolo che non si sovrappone al centro di alcun texel rimane vuoto; i suoi sviluppatori
[hanno identificato questo meccanismo e implementato una correzione](https://projects.blender.org/blender/blender/pulls/161752)
due settimane dopo la creazione della versione in cui sono stati misurati tutti i valori qui riportati. Si tratta di una proprietà della configurazione, non di un singolo elemento: è stato misurato su un asset e risulta **non misurato sugli altri quattro**.
- **La banda del bordo occupa lo 0,00% dell'immagine di riferimento nella fase 1** in tutte le otto telecamere; l'acciaio su uno sfondo grigio si posiziona esattamente sulla soglia desiderata. L'unione dei dati consente di ottenere un risultato del 55,72%.
- **Le giunture delle texture non sono allineate.** Un confine tra diverse aree presenta una variazione **5,5 volte** maggiore rispetto alla normale; l'area definita dal direttore presenta una variazione **9,5 volte** maggiore.
- **La dilatazione si estende tra isole dell'atlante non correlate**: il 74,9% dei texel dilatati prendono il loro colore da un'altra isola, con una distanza mediana di 0,177 su una figura alta 1,0. ⚠ **Questa percentuale si riferisce ai texel dell'atlante e non indica cosa vede la telecamera**: la dilatazione rappresenta il 26,95% dell'atlante renderizzato e il **4,95% dei pixel della figura renderizzata**, con un rapporto di 0,18. Le texture sono presenti in aree ampie, mentre i difetti si trovano in aree più piccole; quindi, un texel dilatato ha un impatto limitato sullo schermo.
- **⚑ Il difetto che determina l'accettazione è causato dalla TEXTURE, non da alcun riempimento**: regioni che presentano il colore di un altro materiale, che nessuna statistica sui punti può rilevare. Misurato in tre modi diversi, utilizzando tre sessioni e tre spazi: **il 91,05% dei difetti sono legati a `reference` con un fattore di arricchimento pari a 0,99**, valore molto vicino alla media; la stessa classe nel tessuto verde presenta il **68,46% dei difetti legati a `reference`**; e su una sottile lamiera, i texel dipinti sulla superficie presentano il **18,77%** dei difetti rispetto al **5,55%** del riempimento dovuto alla dilatazione. Il riempimento utilizza correttamente il colore del vicino più prossimo che presenta una texture; tuttavia, tale vicino presenta già un difetto. La miscela stessa è una suddivisione a due bande non documentata
(`M + gaussian_blur_σ16(B − M)`) che misura **il valore peggiore tra quattro** alternative sugli stessi punti.
- **Le diverse inquadrature non sono mai indipendenti, il che limita ogni correzione della miscela.** Per ogni area con un difetto, **il 100% delle facce con due o più telecamere contribuenti si trova all'interno di un angolo di 90°** (mediana di 45°) e il 21% delle facce con difetti è visibile solo da una telecamera. Le inquadrature adiacenti, che utilizzano impostazioni quasi identiche, presentano problemi contemporaneamente; pertanto, i vantaggi ottenuti con la fotogrammetria multi-view non possono essere trasferiti direttamente qui.
- **Ogni ricostruzione in questa configurazione è un guscio cavo a doppia parete**, con pareti di circa due voxel. Nessun predicato volumetrico è valido su uno di essi.
- **Le immagini presentano differenze ai confini dei materiali non definiti, e la configurazione standard è l'elemento cruciale** (16 agosto 2026). La deformazione interna della mesh rispetto alla superficie misurata ha una mediana compresa tra **3,5 e 11,1 pixel** su tutte le otto inquadrature, rispetto alle mediane del contorno comprese tra 1,2 e 3,0; ogni area con un difetto evidenziata dal direttore (taglio della manica, mano, parte superiore dello stivale) è una giunzione di materiali che non è stata definita nel prompt di generazione (il prompt registrato contiene sei elementi; "grip", "gauntlet", "greave" e "hand" compaiono **zero** volte). La sua diagnosi è la seguente: *"Non abbiamo definito correttamente la configurazione standard."* La configurazione standard W3 e la rigenerazione basata sulla configurazione standard sono la soluzione prevista ([registro della spedizione E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
- **Dal 4,65% al 5,57% dei texel validi rappresentano superfici che nessuna telecamera con anello piatto può vedere**: non superano il test della profondità in nessuna delle inquadrature, nessuna configurazione di proiezione può renderizzarli e la pipeline esistente li ha riempiti con un colore uniforme che ha creato le aree scure. Hanno bisogno di una definizione (materiale neutro, pennello o accettazione), non di una correzione ([report E49](docs/experiments/E49-finish-and-cap-report.md)).
- **Il riempimento completo candidato renderizza poligoni colorati piatti**: si tratta dell'unica classe aperta definita dal direttore nelle schede delle immagini accettate (*"l'aspetto è ottimo, ma ci sono forme poligonali colorate"*). L'ipotesi in fase di test prevede l'utilizzo di maschere di provenienza già contrassegnate: isole isolate delle dimensioni di singoli triangoli, riempite con un colore uniforme a partire da campioni adiacenti al bordo presi dalla silhouette non erosa.

## Come viene eseguito questo repository

La disciplina è tanto importante quanto la pipeline, ed esiste per un motivo: una fase precedente ha eseguito dieci sessioni in cui ogni sessione ha valutato il proprio output e scritto conclusioni che la sessione successiva ha considerato come fatti consolidati. Nulla in quel ciclo era verificabile.

- **Definizione prima del lavoro, relazione dopo, decisione finale**: e la sessione che progetta un esperimento non valuta mai i propri risultati. Quaranta esperimenti sono presenti in [la documentazione](docs/experiments/).
- **Le correzioni vengono applicate al loro posto, accanto alla misurazione che le ha confutate**, mai come semplici eliminazioni. Solo nella sessione iniziale sono state falsificate sei affermazioni iniziali e tutte e sei sono ancora leggibili accanto a ciò che le ha sostituite.
- **I fallimenti rimangono nel repository con la relativa motivazione.** [`tools/superseded/`](docs/tools.md) non è un archivio: chiunque può eseguire questi strumenti e osservare il loro fallimento nello stesso modo.
- **Un risultato negativo è un successo completo**, segnalato e chiuso anziché ottimizzato per raggiungere un valore specifico.
- **I test sono associati al commit che modifica il codice**: 1223 risultati positivi ottenuti da due persone, con CI basata sui percorsi per i 1173 elementi ermetici.
- **La documentazione è consultabile.** Un indice SQLite + FTS5 sull'intero percorso, verificato su quattro livelli. Ha individuato un conteggio delle decisioni che il testo presentava in modo errato in tre siti, contando la documentazione stessa.

## Dove tutto è presente:

| | |
|---|---|
| **[Il manuale](docs/handbook/index.md)** | la guida: le fasi, gli argomenti e il sistema di profili. |
| **[Preparazione del concetto](docs/concept-prep.md)** | il candidato per la fase di modellazione: il suo percorso iniziale (Gate 0), il posizionamento e l'elemento della licenza che apre. |
| **[La documentazione](docs/experiments/)** | quaranta esperimenti: definizione, relazione, decisione e ogni previsione indicata prima della misurazione. |
| **[Cosa ha imparato il percorso](docs/findings.md)** | i risultati duraturi e le regole ottenute con fatica, nella loro interezza. |
| **[Stato di ogni strumento](docs/tools.md)** | cosa funziona, cosa è stato sostituito e le prove per ciascuno. |
| **[Difetti noti](docs/known-defects.md)** | tutto ciò che non è stato risolto, misurato e localizzato nel codice. |
| **[L'arco temporale, come si è svolto](docs/arc-history.md)** | la cronologia, con le correzioni intatte. |
| **[CLAUDE.md](CLAUDE.md)** | come lavorare qui: i ruoli, le regole e il costo di ciascuno. |

## Posizione della licenza

Ogni fase viene eseguita in locale e nel rispetto delle normative commerciali: SDXL (OpenRAIL++), MV-Adapter (open), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Esclusi deliberatamente, con la relativa motivazione: **nvdiffrast** (non commerciale, applicato qui tramite un meccanismo di sicurezza strutturale, non tramite attestazione), **Hunyuan3D-Paint** (licenza non valida nell'UE, nel Regno Unito e in Corea del Sud), **MVPaint** e **TEXGen** (nessuna licenza) e **UltraSharp / SUPIR / StableSR** (strumenti di upscaling non commerciali).

**Il limite dell'affermazione, indicato anziché lasciato alla scoperta.** Descrive il **percorso registrato**: le fasi nel diagramma sopra, dall'immagine al 3D. La fase candidata per la preparazione del modello a monte attualmente viene eseguita su un'API cloud chiusa i cui termini questo repository non ha verificato, quindi nessuna affermazione di licenza qui copre un elemento creato da uno dei suoi modelli. Si tratta di un aspetto aperto con un percorso definito per risolverlo: il modello locale corretto dal punto di vista della licenza è **Qwen-Image-Edit (Apache-2.0)** e **FLUX.1-Kontext [dev] è escluso per gli stessi motivi di nvdiffrast**: pesi non commerciali. Entrambi sono stati verificati rispetto al catalogo dei modelli dello studio anziché richiamati; la motivazione è disponibile in [preparazione del concetto](docs/concept-prep.md).

## Modello di fiducia e di minaccia

facet viene eseguito interamente sulla propria macchina: ogni strumento è uno script che si esegue sui percorsi digitati, quindi la domanda utile non è *quali autorizzazioni richiede questa app*, ma *cosa fanno questi script alla tua macchina*. La risposta viene fornita tramite misurazione, con ogni ciclo ripetibile; la politica completa è disponibile in [SECURITY.md](SECURITY.md):

- **Dati interessati:** mesh, texture, immagini e JSON su disco locale, nei percorsi specificati nella riga di comando. Inoltre `docs/index/facet.db`, che è *derivato*: non contiene nulla che non fosse già un file in questo repository e `facet_index.py build` lo rigenera da zero.
- **Dati NON interessati:** nessuna credenziale, mai. Nessuno di questi elementi legge, memorizza o trasmette token, chiavi o password e nessuno di essi è presente nell'albero: sono stati eseguiti controlli per le chiavi con prefisso del provider, i token GitHub PAT, i token Slack, gli ID delle chiavi AWS, i blocchi di chiavi private, i token bearer e le assegnazioni inline `api_key`/`password`, **zero corrispondenze**, nessun file simile a una credenziale tracciato.
- **Nessun telemetria.** Nessuna raccolta o trasmissione. Non è necessario disattivare nulla perché non c'è nulla da disattivare.
- **Traffico di rete:** due degli strumenti su trentasei aprono un socket: `restylize_views.py` e `texpass_brush.py`, ed entrambi chiamano un'API HTTP ComfyUI all'indirizzo `--host`, **valore predefinito `127.0.0.1:8188`**. Nessun altro elemento in `tools/` effettua una chiamata di rete.
- **Autorizzazioni:** utente normale. Nessuna elevazione, nessuna installazione del servizio, nessuna scrittura nelle impostazioni di sistema o nel registro di sistema.

Tre spigoli vivi vengono evidenziati piuttosto che negati, perché una nota di sicurezza che elenca solo garanzie non è un modello di minaccia: **le operazioni sui file non sono eseguite in un ambiente isolato** (uno strumento scrive ovunque indichino i suoi argomenti); **i percorsi locali assoluti sono incorporati in molti strumenti e documenti** — 114 occorrenze in 26 file, non segreti ma una divulgazione della struttura di una macchina e la ragione per cui la maggior parte degli strumenti non funzionerà senza modifiche altrove; e **gli errori imprevisti si manifestano come tracce di Python nei 36 script di ricerca non pubblicati**, senza un filtro `--debug`. Le interruzioni deliberate sono messaggi `ANDON:` che contengono la misurazione che le ha attivate. Questo è il contratto dello strumento di ricerca e [SHIP_GATE.md](SHIP_GATE.md) registra esattamente quando smette di essere sufficiente, cosa che per i due comandi *installa* è avvenuta alla versione 0.2.0: `facet-index` e `facet-mcp` restituiscono `0` ok / `1` errore utente / `2` errore in fase di esecuzione — e, poiché [E22](docs/experiments/E22-ruling.md), **`4` RIFIUTATO** per un filtro attivato o una sezione `verify` non funzionante, il che significa che lo strumento funziona e ti avvisa di non procedere invece di generare un errore in fase di esecuzione. Tutti rifiutano con un errore strutturato che indica il passaggio successivo anziché una traccia ([E21](docs/experiments/E21-cli-contract-report.md)).

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

Il CI esegue il sottoinsieme ermetico della suite su **ubuntu-latest / Python 3.12** con installazioni fisse (`.github/workflows/ci.yml`); il livello degli artefatti richiede gli alberi registrati in `E:\AI\training`, che non sono presenti in git, quindi il CI li esclude intenzionalmente. Localmente, `python -m pytest` esegue tutti i **1223** test e `python -m pytest -m "not artifacts"` esegue i **1173** test riprodotti dal CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
