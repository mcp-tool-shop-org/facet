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

Lo stile viene applicato **sull'asset**, nello spazio delle texture, e non viene "dipinginto" per ogni vista e poi assemblato successivamente. Fornisci alla pipeline un modello in argilla con forme esagerate e questa restituirà una mesh texturizzata il cui colore deriva da un riferimento stilizzato di *quella* mesh, con tutto ciò che il riferimento non poteva vedere riempito tramite un pennello per l'inpainting mascherato e una dilatazione consapevole della superficie.

Prende il nome dalle due metà del problema: i poligoni e la faccia che devono rappresentare.

## Installa

La pipeline stessa è un insieme di script locali che vengono eseguiti su percorsi specificati dall'utente; clona il repository e leggi [la guida introduttiva](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Due server vengono forniti come pacchetto**: l'indice dei record, in modo che un assistente possa interrogare la traccia delle prove anziché leggerla, e **a partire dalla versione 0.4.0 il server di misurazione**, in modo che due asset misurati a distanza di mesi utilizzino lo stesso flusso di codice.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` è il server MCP stdio che opera sui record (sei strumenti, con la verifica a quattro punti come superficie di controllo che rifiuta i dati non validi) e `facet-index` è l'indice stesso (`build` / `verify` / `q` / `claims`). Esegui uno dei due all'interno di una copia del repository; `--db` indica un indice diverso.

### Il server di misurazione: nuovo nella versione 0.4.0

`facet-measure` fornisce la **parte numerica** di un confronto e non indica mai se l'output è valido. Ogni payload contiene la versione del server, l'hash del file dello strumento e un hash della configurazione, e `measure_report` **rifiuta** di effettuare confronti tra dati incompatibili, che è la caratteristica per cui è stato progettato l'intero sistema.

Verificato eseguendo un **comando** anziché `--help`: una mesh di controllo restituisce 786.432 facce con un envelope di identità completo su una macchina che non ha una copia del repository.

**Il risultato dipende da una sola cosa, ovvero dalla tua versione di Python:**

| la tua versione di Python | `[measure-full]` ti fornisce |
|---|---|
| **3.11 / 3.12** | **tutti e otto gli strumenti**: `open3d` si installa tramite PyPI |
| **3.13** | quattro strumenti: `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 is the latest *release* and publishes cp38–cp312 wheels with **no sdist**,
so on 3.13 there is nothing on PyPI to install. The extra carries it behind
`python_version < "3.13"`, so the install **succeeds** there and the four geometry tools
exit **`4` REFUSED** naming what they need — rather than the whole install failing.

**Per ottenere tutti gli otto strumenti su Python 3.13**, Open3D pubblica i pacchetti cp313 più recenti sul suo canale di sviluppo in continuo aggiornamento. Un URL diretto è valido sulla riga di comando; è consentito solo all'interno dei metadati del pacchetto pubblicato:

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **Su Windows e macOS, i pacchetti di sviluppo hanno il suffisso `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` al momento della scrittura) e il nome cambia quando `main` cambia; elenca gli asset nella [versione `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) e prendi quello più recente. **Questa versione è quella rispetto alla quale sono stati misurati i numeri dipendenti da open3d di questa pipeline**, ed è un limite reale di comparabilità: l'envelope di identità registra l'hash dello strumento, non le sue dipendenze — [E31](docs/experiments/E31-ruling.md).

*Fino alla versione 0.3.1, il pacchetto conteneva due file `.py` e nessuno degli strumenti di misurazione, quindi un server di misurazione installato non aveva nulla da eseguire. Nessuno se n'è accorto per quattro versioni perché questo repository È la copia del codice: lo strumento funzionava dove veniva compilato e non era mai stato altrove.*

⚠ **`pip install facet-mcp` era difettoso in tutte le versioni pubblicate fino alla versione 0.3.0 ed è stato corretto nella versione 0.3.1.** Il pacchetto installa `facet_index` come modulo di livello superiore, quindi fino alla versione 0.3.0 includeva, risolveva la posizione del record rispetto a `<venv>/Lib`, che non contiene né il corpus né l'indice, e `build`, `claims` e `q` fallivano tutti senza `--db`.
**Sulla versione 0.3.0 o precedente, utilizza il binario `npx` sopra.**

Dalla versione 0.3.1, la radice viene risolta **verificando l'esistenza del record** anziché presupponendolo: esegui uno dei due comandi all'interno di una copia del repository e lo troverà; eseguilo da qualsiasi altra posizione ed esso restituirà **`4` RIFIUTATO**, indicando entrambe le directory che ha provato e entrambi i marcatori che ha cercato. `$FACET_INDEX_DB` viene ora letto da entrambi i comandi e seleziona quale *indice*, non quale *corpus*. Misurato su un pacchetto compilato da `main` e installato in un ambiente virtuale pulito — [E24](docs/experiments/E24-ruling.md).

*Questo blocco è stato corretto due volte. Inizialmente conteneva `pipx install facet-mcp # o il pacchetto Python direttamente `, until v0.3.0's read-back ran a **verb** instead of ` --help`. Successivamente affermava che il pacchetto "funziona solo per `q` e `claims`" — **`claims` non funzionava nemmeno**, cosa che E24 ha scoperto eseguendolo. Entrambe le correzioni sono presenti in [known-defects.md](docs/known-defects.md) con le relative misurazioni.*

## La situazione attuale

**Quattro asset accettati, appartenenti a quattro classi di oggetti, senza costi.** Ognuno è stato valutato dal direttore in base alle proprie impostazioni di zoom (sul file GLB o su fogli di dimensioni reali), e non tramite una metrica che supera una soglia.

| oggetto | classe | accettato | riferimento / pennello / dilatazione |
|---|---|---|---|
| **Character (W3)** | umanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veicolo, rigging sottile | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | animale, membrane delle ali | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | oggetto di scena, quasi bidimensionale, grigio su grigio | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Le quote sono espresse in texel validi e **non sono comparabili tra oggetti diversi**: una nave nasconde gran parte di sé dalla prospettiva a livello degli occhi e un animale ne nasconde metà. Valuta ciascun oggetto rispetto al proprio limite di copertura pre-registrato, rispetto al quale ottengono un punteggio dell'**86–93%**: la differenza tra le righe è data dalla geometria, non da una regressione. [Numeri completi con i rispettivi denominatori](docs/handbook/subjects.md).

**Si tratta di una pipeline, non di un generatore a carattere singolo.** Contradici le specifiche su otto elementi specifici e il prompt avrà successo in **8 casi su 8**: la deviazione mediana ΔE è pari a 46,3 rispetto a 6,2 su cinque controlli mantenuti, mentre la figura rimane la stessa. La struttura è mantenuta dalla mesh e dal controllo; gli attributi nominati vengono gestiti dal prompt.

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

**Il percorso tratteggiato è una novità ed è intenzionalmente non continuo.** La prima sezione del percorso riportava sempre la dicitura *modello in argilla*, e fino ad ora nulla di tutto ciò era stato realizzato: ogni modello in argilla veniva portato a mano ed elaborato durante il processo. Ora esiste uno strumento che consente di passare dal concetto al modello in argilla, e la prima coppia è stata realizzata a grandezza naturale: posa, fasce per i polsi, medaglione per la cintura e orlo strappato sono stati tutti riprodotti; la criniera no; la perdita di colore è stata misurata sull’intero fotogramma con un valore di **C\* p99.9 = 13.15** su uno sfondo monocromatico uniforme. **Ciò che questa coppia non può dimostrare è se la trama si rivela migliore**, ed è questa l’unica domanda che ne giustifica l’utilizzo, quindi rimane una possibilità con le prove registrate: **[preparazione del modello](docs/concept-prep.md)**.

## Cosa lo rende efficace?

Sono stati ottenuti sei risultati, ciascuno dei quali è stato il frutto di un esperimento e che, nel complesso, hanno una portata più ampia rispetto all’ambito specifico in cui sono stati prodotti. [La versione completa, con le misurazioni](docs/findings.md).

- **Prima la forma, poi lo stile.** I programmi di ricostruzione interpretano il rumore superficiale come geometria. Un modello in argilla pulito e simile a una scultura, con piani volutamente esagerati, produce una topologia migliore rispetto a uno sprite stilizzato; la copia stilizzata viene generata contemporaneamente e diventa il riferimento cromatico.
- **Definisci i contorni del viso, ottieni un volto.** Un ritaglio che inquadra il busto aggiunge dal **3,1 al 4,5 volte più poligoni** alla testa e la differenza è strutturale: palpebre separate, una piega sul sopracciglio, cavità nasali modellate, non semplicemente una sfocatura più accentuata.
- **Le copie appartengono a una mesh, non a un personaggio.** Riutilizza una copia su diverse mesh e la copertura si riduce del **62% → 22,7%**, perché le braccia si proiettano nello spazio vuoto accanto al modello. Genera sempre le copie dalla mesh che stai per texturizzare.
- **L'identità appartiene alla richiesta.** Un elemento canonico non menzionato nella richiesta appare casualmente e scompare allo stesso modo: questo è stato misurato quando delle ginocchiere dorate sono apparse nell'immagine solo a causa del rumore in un ControlNet difettoso.
- **Chiedi informazioni alla geometria, non a una soglia.** Sostituire una maschera con il profilo esatto ottenuto tramite raycasting ha spostato la copertura di riferimento dal **28,4% al 39,1%** dei texel validi: in modo strettamente additivo, senza diffusione e senza l'utilizzo della GPU. Il metodo di keying basato sulla mediana degli angoli è fallito tre volte qui ed è stato abbandonato.
- **Elimina ciò che nessuna telecamera può vedere, dall'atlante e mai dalla mesh.** Il 49% dei texel dell'atlante non è visibile dall'esterno; escludendo queste facce, l'interpolazione si riduce del 68%. Escludere invece di eliminare rende il fallimento impossibile anziché semplicemente rilevabile.

## Cosa resta da risolvere?

Elencati e descritti nella pagina principale, anziché in una nota a piè di pagina. [Tutti sono elencati nel codice](docs/known-defects.md).

- **La fascia della lama rappresenta lo 0,00% del riferimento nella fase 1** su tutte e otto le telecamere: l’acciaio su uno sfondo grigio si allinea perfettamente con la soglia di riferimento. L’unione consente di recuperare il 55,72%.
- **Le giunture delle pennellate non sono state livellate.** Un confine di provenienza presenta una variazione **5,5 volte** superiore rispetto alla normale tessitura; l’area indicata dal regista mostra una variazione **9,5 volte** superiore.
- **La dilatazione si estende tra isole dell’atlante non correlate:** il 74,9% dei texel dilatati assume il colore da un’altra isola, con una distanza mediana di 0,177 su una figura alta 1,0.
- **Ogni ricostruzione in questo percorso è un guscio vuoto a doppia parete**, con pareti di circa due voxel. Nessun predicato volumetrico è valido per uno di essi.

## Come viene gestito questo repository

La disciplina è tanto importante quanto il processo che la sostiene e ha una sua ragion d’essere: in un ciclo precedente, sono state svolte dieci sessioni durante le quali ogni partecipante ha valutato i propri risultati e redatto delle conclusioni che, nella sessione successiva, sono state considerate come fatti accertati. Nulla di tutto ciò poteva essere verificato.

- **Si definiscono le specifiche prima dell'esecuzione, si redige un rapporto al termine e si stabilisce la conclusione alla fine**; inoltre, la sessione in cui viene progettato un esperimento non valuta mai i propri risultati. Trentuno esperimenti sono disponibili [nel registro](docs/experiments/).
- **Le correzioni vengono applicate direttamente, accanto alla misurazione che le ha confutate**, e non come semplici eliminazioni silenziose. Solo nella sessione iniziale, sei affermazioni preesistenti sono state smentite e tutte e sei sono ancora visibili accanto a ciò che le ha sostituite.
- **I risultati negativi rimangono nel repository insieme alla motivazione.** [`tools/superseded/`](docs/tools.md) non è un archivio: chiunque può eseguire questi strumenti e osservare il loro fallimento nello stesso modo.
- **Un risultato negativo è un successo completo**, viene segnalato e chiuso, anziché essere modificato per raggiungere un determinato valore.
- **I test vengono eseguiti insieme alla modifica del codice**; 917 test hanno avuto esito positivo grazie al lavoro di due persone, con una pipeline CI basata su percorsi per i 877 test più importanti.
- **Il registro è consultabile.** È stato creato un indice SQLite + FTS5 sull'intero percorso dei dati e verificato su quattro sistemi. Questo ha permesso di individuare un errore nel conteggio delle conclusioni, che era presente in tre sezioni del testo, analizzando direttamente il registro stesso.

## Dove si trova tutto

| | |
|---|---|
| **[Il manuale](docs/handbook/index.md)** | la guida: il percorso suddiviso per tappe, gli argomenti trattati, il sistema di classificazione. |
| **[Preparazione del progetto](docs/concept-prep.md)** | il candidato Clay Hop: il suo percorso «Gate 0», la sua posizione e l’elemento speciale che sblocca. |
| **[La documentazione sugli esperimenti](docs/experiments/)** | trentuno esperimenti: descrizione, relazione, valutazione e ogni previsione formulata prima della misurazione. |
| **[Cosa è emerso dall’analisi del percorso]** (docs/findings.md) | i risultati duraturi e le regole ottenute con grande impegno, nella loro interezza. |
| **[Stato di ogni strumento](docs/tools.md)** | cosa funziona, cosa è diventato obsoleto e quali sono le prove a sostegno di ciascuna affermazione. |
| **[Difetti noti](docs/known-defects.md)** | tutto ciò che non è stato risolto, quantificato e localizzato nel codice. |
| **[La storia dell’arco](docs/arc-history.md)** | la storia in ordine cronologico, con le correzioni apportate |
| **[CLAUDE.md]** | come lavorare qui: le mansioni, le regole e i costi di ciascuna posizione. |

## Stato della licenza

Ogni fase viene eseguita a livello locale e garantisce la massima qualità: SDXL (OpenRAIL++), MV-Adapter (open), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Esclusi intenzionalmente, con la seguente motivazione: **nvdiffrast** (non commerciale — applicato qui tramite un meccanismo di sicurezza strutturale, non tramite attestazione), **Hunyuan3D-Paint** (licenza non valida nell'UE, nel Regno Unito e in Corea del Sud), **MVPaint** e **TEXGen** (nessuna licenza), e **UltraSharp / SUPIR / StableSR** (upscaler non commerciali).

**I limiti dell'affermazione sono definiti esplicitamente, anziché lasciati alla scoperta.** Descrive il **percorso registrato**, ovvero le fasi presenti nello schema precedente, a partire dalla conversione da immagine a 3D. La fase di preparazione del modello 3D, che precede questo percorso, viene attualmente eseguita su un'API cloud chiusa i cui termini non sono stati verificati in questo repository, pertanto nessuna affermazione sulla licenza si applica a un elemento creato utilizzando uno dei suoi modelli. Si tratta di un aspetto aperto con un percorso definito per risolverlo: il modello locale corretto dal punto di vista della licenza è **Qwen-Image-Edit (Apache-2.0)** e **FLUX.1-Kontext [dev] è escluso per gli stessi motivi di nvdiffrast** — pesi non commerciali. Entrambi sono stati verificati rispetto al catalogo dei modelli dello studio, anziché essere stati semplicemente richiamati; la motivazione è disponibile in [concept prep](docs/concept-prep.md).

## Modello di fiducia e di minaccia

facet viene eseguito interamente sulla propria macchina: ogni strumento è uno script che si esegue su percorsi specificati dall'utente, quindi la domanda utile non è *quali autorizzazioni richiede questa applicazione*, ma *cosa fanno questi script alla tua macchina*. La risposta è fornita tramite misurazione, con ogni ciclo eseguibile ripetutamente; la politica completa è disponibile in [SECURITY.md](SECURITY.md):

- **Dati interessati:** mesh, texture, immagini e file JSON su disco locale, nei percorsi specificati dalla riga di comando. Inoltre `docs/index/facet.db`, che è *derivato*: non contiene nulla che non fosse già un file presente in questo repository e `facet_index.py build` lo rigenera da zero.
- **Dati NON interessati:** nessuna credenziale, mai. Nessuno strumento legge, memorizza o trasmette token, chiavi o password, e nessuno di questi elementi è presente nell'albero dei file; è stata eseguita una scansione per individuare chiavi con prefisso del provider, GitHub PAT, token Slack, ID chiave AWS, blocchi di chiavi private, token bearer e assegnazioni inline `api_key`/`password`, **nessuna corrispondenza trovata**, nessun file contenente credenziali.
- **Nessun telemetria.** Nessun dato viene raccolto o inviato. Non è necessario disattivare la raccolta dati perché non c'è nulla da disattivare.
- **Traffico di rete:** due dei trentaquattro strumenti aprono una connessione socket: `restylize_views.py` e `texpass_brush.py`, entrambi chiamano un'API HTTP ComfyUI all'indirizzo `--host`, **valore predefinito `127.0.0.1:8188`**. Nessun altro strumento in `tools/` effettua chiamate di rete.
- **Autorizzazioni:** utente standard. Nessuna elevazione dei privilegi, nessuna installazione di servizi, nessuna scrittura nelle impostazioni di sistema o nel registro di sistema.

Tre aspetti critici vengono esplicitati anziché lasciati impliciti, perché una nota sulla sicurezza che elenca solo elementi rassicuranti non è un modello di minaccia: **le operazioni sui file non sono eseguite in un ambiente isolato** (uno strumento scrive ovunque indichino i suoi argomenti); **i percorsi locali assoluti sono incorporati in molti strumenti e nella documentazione** — 114 occorrenze in 26 file, non si tratta di segreti ma della divulgazione del layout di una macchina specifica, ed è il motivo per cui la maggior parte degli strumenti non funzionerà senza modifiche su altre macchine; e **i guasti imprevisti vengono visualizzati come tracce di errore Python nei 34 script di ricerca non pubblicati**, senza alcun filtro `--debug`. Le interruzioni intenzionali sono messaggi `ANDON:` che contengono la misurazione che le ha attivate. Questo è il contratto dello strumento di ricerca e [SHIP_GATE.md](SHIP_GATE.md) registra esattamente quando smette di essere sufficiente, cosa che è successa per i due comandi con cui facet *installa* gli strumenti alla versione 0.2.0: `facet-index` e `facet-mcp` restituiscono `0` (esito positivo) / `1` (errore utente) / `2` (errore di runtime); e, come indicato in [E22](docs/experiments/E22-ruling.md), **`4` RIFIUTATO** per un filtro attivato o una fase fallita `verify`, il che significa che lo strumento funziona e ti avvisa di non procedere anziché generare un errore di runtime. Tutti gli strumenti rifiutano l'esecuzione con un messaggio di errore strutturato che indica la fase successiva anziché visualizzare una traccia di errore ([E21](docs/experiments/E21-cli-contract-report.md)).

**I filtri in questi due comandi non possono più essere eliminati.** Ogni meccanismo ANDON in facet installa `raise`; un semplice `assert` è una dichiarazione che `python -O` rimuove silenziosamente e 87 dei filtri di questo repository potevano essere rimossi tramite una variabile d'ambiente fino a quando E22 non li ha convertiti. Misurato prima e dopo sullo stesso filtro, in quattro modalità interprete.
**E da [E23](docs/experiments/E23-route-gates-report.md), nemmeno i filtri sul percorso che ha prodotto i quattro elementi accettati sono più eliminabili** — i suoi **57 punti su dodici strumenti**, convertiti come una semplice operazione sui file che non erano mai stati eseguiti in precedenza, ognuno dei quali ora rifiuta l'esecuzione anche con `-O` e `PYTHONOPTIMIZE=1` oltre che con un interprete standard.
**E da [E25](docs/experiments/E25-ruling.md), la classe è chiusa.** I suoi **133 punti su 43 file** — gli strumenti di misurazione che hanno prodotto le prove per i quattro elementi accettati sopra — vengono convertiti nello stesso modo, portando il totale a `raise` a **278**.
Esattamente **un** meccanismo ANDON semplice `assert` rimane in qualsiasi punto sotto `tools/`: `superseded/texpass_thin_mask.py`, che **non viene mai** convertito, perché questi strumenti sono mantenuti in modo tale che chiunque possa eseguirli e osservare il loro fallimento nello stesso modo. Questo elemento rimanente è fissato **per nome** nella suite di test, quindi un ciclo futuro non può eliminarlo senza modificare intenzionalmente il test.

**Stato del supporto:** questo repository viene sviluppato in modo aperto, su una singola macchina, da un unico responsabile e con sessioni a rotazione di consulenti ed esecutori. `main` è l'unico stato supportato. Non esiste un canale di rilascio, una politica di backport o un SLA; ciò che esiste è la registrazione: ogni affermazione si trova accanto al codice che la produce e [docs/experiments](docs/experiments/) contiene le specifiche, il rapporto e la decisione per ciascuna di esse.

## Requisiti

Blender 5.x, Python 3.11+ con `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. È necessaria un'installazione locale di ComfyUI solo per il pennello di inpainting. Sviluppato su una RTX 5090; la quantità di VRAM disponibile è più importante della velocità pura.

CI esegue il sottoinsieme ermetico della suite su **ubuntu-latest / Python 3.12** con installazioni bloccate (`.github/workflows/ci.yml`); la fase di creazione degli artefatti richiede le strutture registrate in `E:\AI\training`, che non sono presenti in Git, quindi CI le esclude intenzionalmente. Localmente, `python -m pytest` esegue tutti i **917** test e `python -m pytest -m "not artifacts"` esegue gli **877** test riprodotti da CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
