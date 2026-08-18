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

`facet-mcp` è il server MCP stdio che opera sui record (sei strumenti, con la verifica su quattro punti come superficie di controllo) e `facet-index` è l'indice stesso (`build` / `verify` / `q` / `claims`). Esegui uno dei due all'interno di una directory estratta; `--db` indica un indice diverso.

### Il server di misurazione: nuovo nella versione 0.4.0

`facet-measure` fornisce la **parte numerica** di un confronto e non indica mai se l'output è valido. Ogni payload contiene la versione del server, l'hash del file dello strumento e un hash della configurazione, e `measure_report` **rifiuta** di effettuare confronti tra versioni incompatibili, che è la caratteristica per cui è stato progettato l'intero sistema.

Verificato eseguendo un **comando** anziché `--help`: una mesh di controllo restituisce 786.432 facce con un inviluppo di identità completo su una macchina che non ha estratto il codice.

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

⚠ **Su Windows e macOS, i pacchetti di sviluppo hanno il suffisso `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` al momento della scrittura) e il nome cambia quando `main` cambia; elenca gli asset nella [versione `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) e prendi quello più recente. **Questa versione è quella rispetto alla quale sono stati misurati i numeri dipendenti da open3d di questa pipeline**, ed è un limite reale di comparabilità: l'inviluppo di identità registra l'hash dello strumento, non le sue dipendenze — [E31](docs/experiments/E31-ruling.md).

*Fino alla versione 0.3.1, il pacchetto conteneva due file `.py` e nessuno degli strumenti di misurazione, quindi un server di misurazione installato non aveva nulla da eseguire. Nessuno se n'è accorto per quattro versioni perché questo repository È la directory estratta: lo strumento funzionava dove veniva compilato e non era mai stato altrove.*

⚠ **`pip install facet-mcp` era difettoso in tutte le versioni pubblicate fino alla versione 0.3.0 ed è stato corretto nella versione 0.3.1.** Il pacchetto installa `facet_index` come modulo di primo livello, quindi fino alla versione 0.3.0 includeva, risolveva la posizione del record rispetto a `<venv>/Lib`, che non contiene né il corpus né l'indice, e `build`, `claims` e `q` senza `--db` fallivano tutti.
**Sulla versione 0.3.0 o precedente, utilizza il binario `npx` sopra.**

Dalla versione 0.3.1, la radice viene risolta **verificando l'esistenza del record** anziché presupponendolo: esegui uno dei due comandi all'interno di una directory estratta e lo troverà; eseguilo da qualsiasi altra posizione ed esce con il messaggio **`4` RIFIUTATO**, indicando entrambe le directory che ha provato e entrambi i marcatori che ha cercato. `$FACET_INDEX_DB` viene ora letto da entrambi i comandi e seleziona quale *indice*, non quale *corpus*. Misurato su un pacchetto compilato da `main` e installato in un ambiente virtuale pulito — [E24](docs/experiments/E24-ruling.md).

*Questo blocco è stato corretto due volte. Inizialmente conteneva `pipx install facet-mcp # o il pacchetto Python direttamente `, until v0.3.0's read-back ran a **verb** instead of ` --help`. Successivamente affermava che il pacchetto "funziona solo per `q` e `claims`" — **`claims` non funzionava nemmeno**, cosa scoperta da E24 eseguendolo. Entrambe le correzioni sono presenti in [known-defects.md](docs/known-defects.md) con le relative misurazioni.*

## La situazione attuale

**Quattro asset accettati, appartenenti a quattro classi di oggetti, senza costi.** Ognuno è stato valutato dal direttore in base alle proprie impostazioni di zoom (sul file GLB o su fogli a grandezza naturale), e non tramite una metrica che supera una soglia.

| oggetto | classe | accettato | riferimento / pennello / dilatazione |
|---|---|---|---|
| **Character (W3)** | umanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veicolo, rigging sottile | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | animale, membrane delle ali | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | oggetto di scena, quasi bidimensionale, grigio su grigio | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Le quote sono espresse in texel validi e **non sono comparabili tra oggetti diversi**: una nave nasconde gran parte di sé dalla prospettiva a livello degli occhi e un animale ne nasconde metà. Valuta ciascuno rispetto al proprio limite massimo pre-registrato, rispetto al quale ottengono un punteggio dell'**86–93%**: la differenza tra le righe è data dalla geometria, non da una regressione. [Numeri completi con i rispettivi denominatori](docs/handbook/subjects.md).

**Si tratta di una pipeline, non di un generatore a carattere singolo.** Contradici le specifiche su otto elementi specifici e il prompt vince **8 su 8**: la mediana ΔE è 46,3 rispetto a 6,2 su cinque controlli mantenuti; nel frattempo, la figura rimane la stessa. La struttura è mantenuta dalla mesh e dal controllo; gli attributi denominati sono gestiti dal prompt.

**La questione del proiettore è stata chiusa il 16 agosto 2026** ([E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
Le otto immagini **compongono**: ricostruite a partire dal set di dati per ogni prospettiva, utilizzando
pesi relativi al bordo × alla direzione × alla visibilità; l'atlante, una volta renderizzato, ha superato per la prima volta il test del Direttore su questa sequenza — due volte, lungo due archi — accanto a un
atlante già esistente, la cui sequenza stava causando problemi di rendering; le immagini concordano. La catena che ha permesso questo è in `tools/`
(`emit_view_aovs`, `s3_composite`, `flow_estimate`, `s3_run`, `s3_sheet`,
`atlas_from_aovs`, `twin_mesh_warp`), costruita principalmente attraverso un canale di revisione esterno
i cui elementi di calibrazione nominati hanno mantenuto **diciassette su diciassette**, tutti
verificati qui eseguendoli prima che qualsiasi elemento potesse essere considerato affidabile.

**Il canone è costituito dai dati e definisce i limiti della spesa (17 agosto 2026).** La specifica dell'identità
include diciassette elementi; il flusso di lavoro che ha generato le immagini gemelle ne include sedici; la configurazione predefinita per una nuova esecuzione ne include sei. Nulla li collega, quindi quattro sequenze
hanno corretto la composizione a valle del rendering che era errato alla fonte. Il canone è ora un
database organizzato in base alla **superficie**: un elenco di elementi non può mostrare cosa manca e un
elemento anulabile crea uno spazio vuoto nella riga; `canon_gate` viene eseguito **all'interno** di `restylize_views`
e `texpass_brush`, prima che esista la directory di output. Una generazione il cui prompt non include il canone approvato viene rifiutata e nulla viene scritto.

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

`prof_hit 5/19` è un **campione lasciato intenzionalmente incompleto**: è l'impostazione predefinita attiva che una sequenza
utilizzerebbe effettivamente, quindi la prima `--profile character.json` dovrebbe interrompersi. Riparare
la stringa eliminerebbe le prove.

**Il limite del processo è definito esplicitamente, anziché lasciato alla scoperta.** Verifica che il
prompt di input contenga le frasi del canone approvato. Non verifica parafrasi,
elementi per ogni prospettiva, bozze non approvate, soggetti senza file di superficie o se un materiale nominato è stato applicato sulla superficie corretta. Quattro soggetti hanno un file IDENTITY.md e nessun file JSON delle superfici: lasciato incompleto anziché generato senza seguire il riferimento.

## La sequenza

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

Passo dopo passo, con la motivazione per ciascuno: **[il manuale](docs/handbook/index.md)**.

**Il passaggio tratteggiato è nuovo ed è intenzionalmente non continuo.** Il primo elemento della sequenza ha sempre
visualizzato *concetto in argilla*, e fino ad ora nulla di ciò ha prodotto un risultato concreto: ogni modello in argilla è arrivato manualmente ed è stato elaborato durante il processo. Ora esiste uno strumento che converte un concetto in un modello in argilla, e la prima coppia è stata creata a dimensione reale: posa, fasce per i polsi, medaglione sulla cintura e orlo strappato sono stati tutti inclusi; la massa della criniera no; la perdita di colore è stata misurata su tutto il fotogramma con **C\* p99.9 = 13.15** con uno sfondo monocromatico uniforme. **Ciò che questa coppia non può mostrare è se la mesh risulta migliore**, che è l'unica domanda che ne determina l'approvazione, quindi rimane un candidato con le sue prove registrate:
**[preparazione del concetto](docs/concept-prep.md)**.

## Cosa lo rende efficace

Sei risultati, ciascuno dei quali ha richiesto un esperimento e ciascuno dei quali è applicabile oltre il soggetto che lo ha prodotto. [La versione completa, con le
misure](docs/findings.md).

- **Prima la forma, poi lo stile.** Gli strumenti di ricostruzione interpretano il rumore della superficie come geometria. Un modello in argilla pulito e simile a una scultura, con piani intenzionalmente esagerati, produce una topologia migliore rispetto a uno sprite stilizzato; l'immagine gemella stilizzata viene generata contemporaneamente e diventa il
riferimento per i colori.
- **Inquadra il viso, ottieni un viso.** Un ritaglio del busto aggiunge **da 3,1 a 4,5 volte** più poligoni alla
testa, e la differenza è strutturale: palpebre separate, una piega sul sopracciglio, cavità delle narici modellate; non semplicemente una sfocatura più nitida.
- **Le immagini gemelle appartengono a una mesh, non a un personaggio.** Riutilizza un'immagine gemella su diverse mesh e la copertura diminuisce del **62% → 22,7%**, perché le braccia si proiettano nello spazio vuoto accanto al modello. Genera sempre le immagini gemelle dalla mesh che stai per texturizzare.
- **L'identità appartiene al prompt.** Un elemento del canone non nominato nel prompt viene aggiunto accidentalmente e lascerà lo stesso modo: misurato quando è stato scoperto che le ginocchiere dorate apparivano nell'immagine solo a causa del rumore in un ControlNet difettoso.
- **Chiedi alla geometria, non a una soglia.** La sostituzione di una maschera chiave con l'esatta silhouette del raycast ha spostato la copertura di riferimento dal **28,4% al 39,1%** dei texel validi: strettamente additivo, nessuna diffusione, nessuna GPU. Il keying basato sull'angolo mediano ha fallito tre volte qui ed è stato dismesso.
- **Elimina ciò che nessuna telecamera può vedere, dall'atlante e mai dalla mesh.** Il 49% dei texel dell'atlante
sono invisibili dall'esterno; l'esclusione di questi elementi riduce l'interpolazione del **68%**. L'esclusione anziché l'eliminazione rende il fallimento impossibile invece che semplicemente rilevabile.

## Cosa non è stato risolto

Nominato e misurato, nella pagina iniziale anziché in una nota a piè di pagina. [Tutti, situati nel
codice](docs/known-defects.md).

- **Alcune mappe di superficie visibili corrispondono allo spazio dell'atlante, ma nessuna operazione di baking le modifica mai**, e vengono renderizzate come il nero predefinito non modificato dell'immagine. Il sistema di baking di Blender utilizza un campionamento del centro texel, quindi un triangolo che non si sovrappone al centro di alcun texel rimane vuoto: i suoi stessi sviluppatori
[hanno identificato il meccanismo e implementato una correzione](https://projects.blender.org/blender/blender/pulls/161752)
due settimane dopo la build su cui sono stati misurati tutti i valori qui presenti. Si tratta di una proprietà del percorso,
non di un singolo oggetto: misurato su un asset, **non misurato sugli altri quattro**.
- **La fascia della lama occupa lo 0,00% del riferimento dello stadio 1** in tutte e otto le telecamere: l'acciaio su uno sfondo grigio si posiziona esattamente sulla soglia chiave. L'unione recupera il 55,72%.
- **Le giunture delle texture non sono allineate.** Un confine di provenienza presenta una variazione della texture pari a **5,5 volte** rispetto alla normale; la regione identificata dal Direttore presenta una variazione pari a **9,5 volte**.
- **La dilatazione si estende tra isole dell'atlante non correlate**: il 74,9% dei texel dilatati prendono il loro colore da un'altra isola, con una distanza mediana di 0,177 su una figura alta 1,0. ⚠ **Questa percentuale si riferisce ai texel dell'atlante e non è un'affermazione su ciò che vede una telecamera**: la dilatazione rappresenta il 26,95% dell'atlante renderizzato e il **4,95% dei pixel della figura renderizzata**, con un rapporto di 0,18. Le texture si trovano in grandi mappe, i vuoti in quelle piccole, quindi un texel dilatato ha un costo contenuto nello spazio dello schermo.
- **⚑ Il difetto che determina l'accettazione è legato alla TEXTURE, non a nessun riempimento**: regioni che presentano il colore di un altro materiale, cosa che nessuna statistica sui punti può rilevare. Misurato in tre modi con tre sessioni in tre spazi diversi: **91,05% `reference`, con un arricchimento pari a 0,99**, valore molto vicino alla media; la stessa classe nel verde del tessuto presenta il **68,46% `reference`**; e su una sottile lama, i texel dipinti sulla superficie presentano il **18,77%** di contaminazione rispetto al **5,55%** del riempimento della dilatazione.
Il riempimento proviene correttamente dal vicino dipinto più prossimo, e questo vicino è già difettoso. La miscela stessa è una suddivisione a due bande non documentata
(`M + gaussian_blur_σ16(B − M)`) che misura il **peggiore dei quattro** valori alternativi sugli stessi punti.
- **Le viste non sono mai indipendenti, il che limita ogni correzione della miscela.** Per ogni gruppo di difetti, il **100% delle facce con due o più telecamere contribuenti ha tutte le telecamere all'interno di un angolo di 90°** (mediana di 45°) e il 21% delle facce difettose è visibile solo da una telecamera. Le viste adiacenti, sottoposte a controlli quasi identici, falliscono insieme, quindi i vantaggi multi-vista pubblicati dalla fotogrammetria non si trasferiscono qui in modo diretto.
- **Ogni ricostruzione su questo percorso è un guscio cavo a doppia parete**, con pareti di circa due voxel. Nessun predicato volumetrico è valido su uno di essi.
- **Le piastre sono diverse ai confini dei materiali non identificati, e il canone è l'elemento cruciale** (2026-08-16). La deformazione interna da gemello alla mesh misurata ha una mediana compresa tra **3,5 e 11,1 px** su tutte le otto viste rispetto alle mediane della silhouette comprese tra 1,2 e 3,0; ogni regione residua che il Direttore ha cerchiato (taglio della manica, mano, parte superiore dello stivale) è una giunzione di materiali che il prompt di generazione non ha mai nominato. ⚠ **CORRETTO IL 2026-08-17 e la correzione affina i risultati.** In precedenza si leggeva: "il prompt registrato contiene sei elementi", ma in realtà ne fonde due diversi. Il flusso di lavoro che ha generato i gemelli nomina **16 su 17**, mancando solo l'impugnatura; il *profilo predefinito del pennello* ne nomina sei. Entrambe le affermazioni sono vere, e la frase conteneva un errore su queste. Ciò che conta di più è che l'impugnatura, il bracciale, la protezione per la gamba e la mano compaiono **zero** volte nel prompt di 16 frasi, perché **non esiste alcun elemento relativo a essi nel canone**. Un prompt completo non può comunque nominare una mano che non è mai stata specificata. ✅ **CHIUSO IL 2026-08-17**: l'elenco delle superfici viene esaminato, compilato e **tutti i 24 elementi sono stati convalidati**, e il sistema ora rifiuta un prompt che non li copre.
- **Dal 4,65 al 5,57% dei texel validi rappresentano una superficie che nessuna telecamera a anello piatto può vedere**: questi falliscono nel test del gate di profondità in ogni vista, nessun percorso di proiezione può renderizzarli e la pipeline fornita li ha riempiti con un'inondazione cieca rispetto all'isola, creando le macchie scure. Hanno bisogno di una politica (materiale neutro, pennello o accettazione), non di una correzione ([relazione E49](docs/experiments/E49-finish-and-cap-report.md)).
- **Poligoni colorati piatti sulle schede di qualità accettabile**: l'unica classe aperta del Direttore. ⚠ **L'ipotesi sul passaggio di riempimento è FALSA (2026-08-17).** Il riempimento orfano misura *al di sotto* della sua media al difetto (0,27), le aree si trovano per il 90–99% su texel dipinti normali e lo stesso difetto è presente in un rendering creato da un atlante che precede la correzione ritenuta responsabile. Invece, l'origine è stata individuata: il gemello della vista di rendering è pulito in quel punto e una **vista diversa** possiede 97 dei 115 pixel difettosi con un angolo di 0,68 rispetto a 0,60. La macchia angolare è un **artefatto di dispersione** e il colore è una reale discrepanza tra le viste su una superficie che è già stata nominata, quindi la rigenerazione del gemello non è giustificata dal fatto che "il difetto si trova nei gemelli". Un compositore che preferisce la vista di destinazione rappresenta la correzione definita e non ha costi. *Testo sostituito, mantenuto in base alla regola delle correzioni: "isole orfane delle dimensioni di singoli triangoli, riempite con un colore uniforme da campioni adiacenti al confine presi con la silhouette non erosa".*

## Come viene eseguito questo repository

La disciplina è tanto importante quanto il processo stesso e esiste per una ragione: in precedenza, sono state eseguite dieci sessioni in cui ogni partecipante ha valutato i propri risultati e scritto delle conclusioni che la sessione successiva ha considerato come fatti consolidati. Nulla di tutto ciò era verificabile.

- **Definizione prima del lavoro, relazione dopo, decisione finale**: e la sessione che progetta un esperimento non valuta mai i propri risultati. Cinquantuno esperimenti sono presenti in [la documentazione](docs/experiments/).
- **Le correzioni vengono applicate al loro posto, accanto alla misurazione che le ha confutate**, mai come semplici eliminazioni. Solo nella sessione iniziale sono state falsificate sei affermazioni iniziali e tutte e sei sono ancora leggibili accanto a ciò che le ha sostituite.
- **I fallimenti rimangono nel repository con la relativa motivazione.** [`tools/superseded/`](docs/tools.md) non è un archivio: chiunque può eseguire questi strumenti e osservare il loro fallimento nello stesso modo.
- **Un risultato negativo è un successo completo**, segnalato e chiuso anziché ottimizzato per raggiungere un valore specifico.
- **I test sono associati al commit che modifica il codice**: 1338 superati con due persone che lavorano, con CI basata sui percorsi per i 1284 elementi ermetici.
- **La documentazione è consultabile.** Un indice SQLite + FTS5 sull'intero percorso, verificato su quattro livelli. Ha individuato un conteggio delle decisioni che il testo presentava in modo errato in tre siti, contando la documentazione stessa.

## Dove tutto è presente:

| | |
|---|---|
| **[Il manuale](docs/handbook/index.md)** | la guida: le fasi, gli argomenti e il sistema di profili. |
| **[Preparazione del concetto](docs/concept-prep.md)** | il candidato per la fase di modellazione: il suo percorso iniziale (Gate 0), il posizionamento e l'elemento della licenza che apre. |
| **[La documentazione](docs/experiments/)** | cinquantuno esperimenti: definizione, relazione, decisione e ogni previsione indicata prima della misurazione. |
| **[Cosa ha imparato il percorso](docs/findings.md)** | i risultati duraturi e le regole ottenute con fatica, nella loro interezza. |
| **[Stato di ogni strumento](docs/tools.md)** | cosa funziona, cosa è stato sostituito e le prove per ciascuno. |
| **[Difetti noti](docs/known-defects.md)** | tutto ciò che non è stato risolto, misurato e localizzato nel codice. |
| **[L'arco temporale, come si è svolto](docs/arc-history.md)** | la cronologia, con le correzioni intatte. |
| **[CLAUDE.md](CLAUDE.md)** | come lavorare qui: i ruoli, le regole e il costo di ciascuno. |

## Posizione della licenza

Ogni fase viene eseguita in locale e nel rispetto delle normative commerciali: SDXL (OpenRAIL++), MV-Adapter (open), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Esclusi deliberatamente, con la relativa motivazione: **nvdiffrast** (non commerciale, applicato qui tramite un meccanismo di sicurezza strutturale, non tramite attestazione), **Hunyuan3D-Paint** (licenza non valida nell'UE, nel Regno Unito e in Corea del Sud), **MVPaint** e **TEXGen** (nessuna licenza) e **UltraSharp / SUPIR / StableSR** (strumenti di upscaling non commerciali).

**Il limite dell'affermazione, indicato anziché lasciato alla scoperta.** Descrive il **percorso registrato**: le fasi nel diagramma sopra, dall'immagine al 3D. La fase candidata per la preparazione del modello a monte attualmente viene eseguita su un'API cloud chiusa i cui termini questo repository **non ha verificato**, quindi nessuna affermazione di licenza qui copre un elemento creato da uno dei suoi modelli. Si tratta di un aspetto aperto con un percorso definito per risolverlo: il modello locale corretto per la licenza è **Qwen-Image-Edit (Apache-2.0)** e **FLUX.1-Kontext [dev] è escluso per gli stessi motivi di nvdiffrast**: pesi non commerciali. Entrambi sono stati verificati rispetto al catalogo dei modelli dello studio anziché richiamati; la motivazione è presente in [preparazione del concetto](docs/concept-prep.md).

## Modello di fiducia e di minaccia

facet viene eseguito interamente sulla propria macchina: ogni strumento è uno script che si esegue sui percorsi digitati, quindi la domanda utile non è *quali autorizzazioni richiede questa app*, ma *cosa fanno questi script alla tua macchina*. La risposta è fornita dalla misurazione, con ogni ciclo ripetibile; la politica completa è disponibile in [SECURITY.md](SECURITY.md):

- **Dati interessati:** mesh, texture, immagini e JSON su disco locale, nei percorsi specificati nella riga di comando. Inoltre `docs/index/facet.db`, che è *derivato*: non contiene nulla che non fosse già un file in questo repository e `facet_index.py build` lo rigenera da zero.
- **Dati NON interessati:** nessuna credenziale, mai. Nulla qui legge, memorizza o trasmette token, chiavi o password e nessuno di questi elementi è presente nell'albero: è stata eseguita una scansione per le chiavi con prefisso del provider, i token GitHub PAT, i token Slack, gli ID delle chiavi AWS, i blocchi di chiavi private, i token bearer e le assegnazioni inline `api_key`/`password`, **zero corrispondenze**, nessun file simile a una credenziale tracciato.
- **Nessun telemetria.** Nessuna raccolta, nessuna trasmissione. Non esiste un'opzione per disattivare perché non c'è nulla da disattivare.
- **Traffico di rete:** due degli strumenti su trentasei aprono un socket: `restylize_views.py` e `texpass_brush.py`, ed entrambi chiamano un'API HTTP ComfyUI all'indirizzo `--host`, **valore predefinito `127.0.0.1:8188`**. Nient'altro in `tools/` effettua una chiamata di rete.
- **Autorizzazioni:** utente normale. Nessun aumento dei privilegi, nessuna installazione del servizio, nessuna scrittura nelle impostazioni di sistema o nel registro di sistema.

Tre spigoli vivi vengono evidenziati piuttosto che negati, perché una nota di sicurezza che elenca solo delle rassicurazioni non è un modello di minaccia: **le operazioni sui file non sono eseguite in un ambiente isolato** (uno strumento scrive ovunque gli indichino i suoi argomenti); **i percorsi locali assoluti sono incorporati in molti strumenti e documenti** — 114 occorrenze in 26 file, non si tratta di segreti ma della divulgazione del layout di una macchina e del motivo per cui la maggior parte degli strumenti non funzionerà senza modifiche altrove; e **i fallimenti imprevisti emergono come tracce di Python nei 36 script di ricerca non pubblicati**, senza un filtro `--debug`. Le interruzioni deliberate sono messaggi `ANDON:` che contengono la misurazione che le ha attivate. Questo è il contratto dello strumento di ricerca e [SHIP_GATE.md](SHIP_GATE.md) registra esattamente quando smette di essere sufficiente, cosa che per i due comandi *installa* è avvenuta a 0.2.0: `facet-index` e `facet-mcp` restituiscono `0` ok / `1` errore utente / `2` errore in fase di esecuzione — e, poiché [E22](docs/experiments/E22-ruling.md), **`4` RIFIUTATO** per un filtro attivato o una sezione `verify` non funzionante, il che significa che lo strumento funziona e ti avvisa di non procedere invece di generare un errore in fase di esecuzione. Tutti rifiutano con un messaggio di errore strutturato che indica il passaggio successivo anziché una traccia ([E21](docs/experiments/E21-cli-contract-report.md)).

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

Il CI esegue il sottoinsieme ermetico della suite su **ubuntu-latest / Python 3.12** con installazioni fisse (`.github/workflows/ci.yml`); il livello degli artefatti richiede gli alberi registrati in `E:\AI\training`, che non sono presenti in git, quindi il CI li esclude intenzionalmente. Localmente, `python -m pytest` esegue tutti i **1338** test e `python -m pytest -m "not artifacts"` esegue i **1284** test riprodotti dal CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
