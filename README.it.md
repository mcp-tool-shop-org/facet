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

Lo stile viene applicato **sull'asset**, nello spazio delle texture, e non viene disegnato per ogni vista e poi assemblato in seguito. Fornisci alla pipeline un modello di argilla con forme esagerate e questa restituirà una mesh texturizzata il cui colore deriva da un riferimento stilizzato di *quella* mesh, con tutto ciò che il riferimento non poteva vedere riempito tramite un pennello per l'inpainting mascherato e una dilatazione consapevole della superficie.

Prende il nome dalle due metà del problema: i poligoni e la superficie che devono rappresentare.

## Installa

La pipeline stessa è un insieme di script locali che vengono eseguiti su percorsi specificati dall'utente; clona il repository e leggi [la guida introduttiva](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Due server vengono forniti come pacchetto**: l'indice dei record, in modo che un assistente possa interrogare la traccia delle prove invece di leggerla, e **a partire dalla versione 0.4.0 il server di misurazione**, in modo che due asset misurati a distanza di mesi utilizzino lo stesso flusso di codice.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` è il server MCP stdio che opera sui record (sei strumenti, con la verifica a quattro punti come superficie di controllo che rifiuta i dati non validi) e `facet-index` è l'indice stesso (`build` / `verify` / `q` / `claims`). Esegui uno dei due all'interno di una copia del repository; `--db` indica un indice diverso.

### Il server di misurazione: nuovo nella versione 0.4.0

`facet-measure` fornisce la **parte numerica** di un confronto e non indica mai se l'output è valido. Ogni payload contiene la versione del server, l'hash del file dello strumento e un hash della configurazione, e `measure_report` **rifiuta** di effettuare confronti tra dati incompatibili, che è la caratteristica per cui è stato progettato l'intero sistema.

Verificato eseguendo un **comando** anziché `--help`: una mesh di controllo restituisce 786.432 facce con un inviluppo di identità completo su una macchina che non ha una copia del repository.

**Il risultato dipende da una sola cosa, ovvero dalla tua versione di Python:**

| la tua versione di Python | `[measure-full]` ti fornisce |
|---|---|
| **3.11 / 3.12** | **tutti e otto gli strumenti**: `open3d` si installa tramite PyPI |
| **3.13** | quattro strumenti: `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 is the latest *release* and publishes cp38–cp312 wheels with **no sdist**,
so on 3.13 there is nothing on PyPI to install. The extra carries it behind
`python_version < "3.13"`, so the install **succeeds** there and the four geometry tools
exit **`4` REFUSED** naming what they need — rather than the whole install failing.

**Per ottenere tutti e otto gli strumenti su Python 3.13**, Open3D pubblica i pacchetti cp313 più recenti sul suo canale di sviluppo in continuo aggiornamento. Un URL diretto è valido sulla riga di comando; è consentito solo all'interno dei metadati del pacchetto pubblicato:

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **Su Windows e macOS, i pacchetti di sviluppo hanno il suffisso `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` al momento della scrittura) e il nome cambia quando `main` cambia; elenca gli asset nella [versione `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) e seleziona quello più recente. **Questa versione è quella rispetto alla quale sono stati misurati i numeri dipendenti da open3d di questa pipeline**, ed è un limite reale di comparabilità: l'inviluppo di identità registra l'hash dello strumento, non le sue dipendenze — [E31](docs/experiments/E31-ruling.md).

*Fino alla versione 0.3.1, il pacchetto conteneva due file `.py` e nessuno degli strumenti di misurazione, quindi un server di misurazione installato non aveva nulla da eseguire. Nessuno se n'è accorto per quattro versioni perché questo repository È la copia del codice: lo strumento funzionava dove veniva compilato e non era mai stato altrove.*

⚠ **`pip install facet-mcp` era difettoso in tutte le versioni pubblicate fino alla versione 0.3.0 ed è stato corretto nella versione 0.3.1.** Il pacchetto installa `facet_index` come modulo di primo livello, quindi fino alla versione 0.3.0 includeva, risolveva la posizione del record rispetto a `<venv>/Lib`, che non contiene né il corpus né l'indice, e `build`, `claims` e `q` senza `--db` fallivano tutti.
**Sulla versione 0.3.0 o precedente, utilizza il binario `npx` sopra.**

Dalla versione 0.3.1, la posizione principale viene risolta **verificando l'esistenza del record** anziché presupponendolo: esegui uno dei due comandi all'interno di una copia del repository e lo troverà; eseguilo da qualsiasi altra posizione ed esce con il messaggio **`4` RIFIUTATO**, indicando entrambe le directory che ha provato e entrambi i marcatori che ha cercato. `$FACET_INDEX_DB` viene ora letto da entrambi i comandi e seleziona quale *indice*, non quale *corpus*. Misurato su un pacchetto compilato da `main` e installato in un ambiente virtuale pulito — [E24](docs/experiments/E24-ruling.md).

*Questo blocco è stato corretto due volte. Inizialmente conteneva il testo `pipx install facet-mcp # oppure il pacchetto Python direttamente `, until v0.3.0's read-back ran a **verb** instead of ` --help`. Successivamente affermava che il pacchetto "funziona solo per `q` e `claims`" — **`claims` non funzionava nemmeno**, cosa scoperta eseguendolo in E24. Entrambe le correzioni sono presenti in [known-defects.md](docs/known-defects.md) con le relative misurazioni.*

## La situazione attuale

**Quattro asset accettati, appartenenti a quattro classi di oggetti, senza costi aggiuntivi.** Ognuno è stato valutato dal direttore con il proprio livello di zoom, sul file GLB o su fogli di dimensioni reali, e non tramite una metrica che supera una soglia.

| oggetto | classe | accettato | riferimento / pennello / dilatazione |
|---|---|---|---|
| **Character (W3)** | umanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veicolo, rigging leggero | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | animale, membrane delle ali | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | oggetto di scena, quasi bidimensionale, grigio su grigio | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Le quote sono espresse in texel validi e **non sono comparabili tra oggetti diversi**: una nave nasconde gran parte di sé dalla prospettiva a livello degli occhi e un animale ne nasconde metà. Valuta ciascuno rispetto al proprio limite di copertura pre-registrato, rispetto al quale ottengono un punteggio dell'**86–93%**: la differenza tra le righe è data dalla geometria, non da una regressione. [Numeri completi con i rispettivi denominatori](docs/handbook/subjects.md).

**Si tratta di una pipeline, non di un generatore a carattere singolo.** Contraddici la specifica su otto elementi specifici e il prompt avrà successo in **8 casi su 8**: ΔE mediano pari a 46,3 rispetto a 6,2 su cinque controlli mantenuti; nel frattempo, la figura rimane la stessa. La struttura è mantenuta dalla mesh e dal controllo; gli attributi nominati sono gestiti dal prompt.

**La questione del proiettore è stata chiusa il 16 agosto 2026** ([E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
Le otto immagini **compongono**: ricostruite dal set di dati per ogni inquadratura, utilizzando
pesi di bordo × orientamento × visibilità; l'atlante ha superato la soglia di accettazione del direttore per la prima volta su questo percorso — due volte, lungo due archi — accanto a un
atlante già esistente il cui percorso stava causando problemi alle immagini, e queste concordano. La catena che lo ha fatto è in `tools/`
(`emit_view_aovs`, `s3_composite`, `flow_estimate`, `s3_run`, `s3_sheet`,
`atlas_from_aovs`, `twin_mesh_warp`), costruita principalmente attraverso un canale di revisione esterno
i cui elementi di calibrazione nominati hanno mantenuto una corrispondenza **venti su venti**, ognuno
verificato qui eseguendolo prima che qualsiasi elemento confermi la build.

**Il canone è costituito dai dati e definisce i limiti della spesa (17 agosto 2026).** La specifica dell'identità
ha nominato diciassette elementi; il flusso di lavoro che ha generato le immagini gemelle ne ha nominati sedici; la configurazione predefinita, per una nuova esecuzione, ne ha nominati sei. Nulla li collegava, quindi quattro archi
hanno corretto la composizione a valle dell'immagine che era errata all'origine. Il canone è ora un
database indicizzato su **superficie**: un elenco di elementi non può mostrare cosa manca e un
elemento nullable crea uno spazio vuoto in una riga; `canon_gate` viene eseguito **all'interno** degli strumenti che
creano una generazione, prima che esista la directory di output. Una generazione il cui prompt non copre il canone approvato viene rifiutata e nulla viene scritto.

**È un router ed è configurato per chiudersi in caso di errore.** Risolve un soggetto nel suo file del canone, copre
un prompt in **entrambe** le direzioni e gestisce un ambito. Uno **strumento che crea una generazione e a cui non viene fornito alcun canone non procede senza problemi: lo rifiuta.** La soluzione per un soggetto che effettivamente non ne ha è supportata da dati statistici e non può essere utilizzata da un soggetto che invece ne ha:
`--no-canon --subject GALLEON` procede e si presenta; `--no-canon --subject W3` viene
**rifiutato**, perché W3 ha delle superfici. Questo chiude la casella di controllo per costruzione, piuttosto che per convenzione, ed è importante perché la forma precedente — `if args.canon:` — permetteva al driver PowerShell esistente di superare il controllo senza problemi.

**La seconda direzione è quella che individua un difetto reale.** Verificare che il prompt *contenga* il canone rivela un prompt incompleto. Verificare che tutto nel prompt *sia* canone
rivela una frase che nomina qualcosa che il personaggio non ha, e ce n'era uno presente nell'impostazione predefinita: **`gold necklace`**, che questo repository aveva già identificato come errore nella denominazione della medaglia dorata, *"e l'elemento sopravvive per caso."* Un prompt completo con tale frase aggiunta ora restituisce `missing: 0` e viene comunque rifiutato, nominando la clausola.

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

`prof_hit 5/19` è un **campione lasciato intenzionalmente difettoso**: è l'impostazione predefinita che una generazione
effettivamente utilizzerebbe, quindi il primo `--profile character.json` dovrebbe interrompersi. Riparare
la stringa eliminerebbe le prove.

**E c'è un foglio di calcolo, perché i quattro soggetti senza canone non si muoveranno da soli.** Emette ogni superficie che il *tipo* di un soggetto implica — quindi uno spazio vuoto è una riga prima che qualcuno lo abbia nominato — trasforma un file IDENTITY.md in un inventario, gestisce le giunture a coppie per confermare e riserva gli slot dell'ambito per ogni inquadratura. È **strutturalmente incapace di riempire un elemento**, ed è questa la proprietà che viene testata: una frase "velenosa" che arriva con una superficie già assegnata non viene scritta. Generare il canone significa avere una persona che esamina un riferimento; il foglio di calcolo rende semplicemente l'operazione più semplice e completa.

**Il confine del controllo, dichiarato piuttosto che lasciato alla scoperta.** Verifica le frasi del canone approvato in entrambe le direzioni, all'interno di un ambito. Non verifica parafrasi o sinonimi — la corrispondenza semantica metterebbe un modello all'interno del controllo, cosa che questo repository rifiuta per principio — né gli elementi per ogni inquadratura finché non viene dichiarato un ambito di visualizzazione, né se un materiale nominato è finito sulla *superficie* corretta. Gli slot dell'ambito esistono e i loro elenchi di superfici sono vuoti: riempirli è un'operazione umana, come riempire gli elementi. Quattro soggetti hanno un file IDENTITY.md e nessun file JSON delle superfici — lasciato incompleto piuttosto che generato senza esaminare il riferimento.

**Quanti elementi può contenere un prompt viene misurato, e non raggiunge il canone.** La letteratura valuta ogni elemento di prompt aggiunto in termini di impatto sulla presenza degli elementi, su una scala ben inferiore alla nostra, quindi un posto su Opus ha chiesto se le immagini per cui si era già pagato potessero risolvere la questione. **Non possono, ed è per motivi strutturali:** nessun elemento nel corpus mantiene la sua frase costante mentre il numero intorno ad esso varia *e* può essere assente. Ciò che forniscono è un limite unilaterale, da cinque prompt con una telecamera con controllo, maschera e seme identici: su una scala di **10 → 17**, la rimozione non elimina nulla di ciò che era presente a 10, mentre una modifica dell'identità allo *zero* elementi ha spostato l'intero intervallo di calibrazione. **Il canone di W3 richiede 19 elementi e il corpus non lo raggiunge mai** ([E55](docs/experiments/E55-density-vs-identity-report.md)). Lo studio stampa i tre numeri che vengono combinati: 24 superfici del prompt, 25 controlli richiesti, 19 elementi univoci — quindi un conteggio della copertura non viene mai confrontato con una misurazione del numero di elementi.

## Il percorso

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

Fase per fase, con la motivazione per ciascuna: **[il manuale](docs/handbook/index.md)**.

**Il passaggio tratteggiato è nuovo ed è intenzionalmente non solido.** La prima casella del percorso ha sempre indicato *concetto in argilla*, e fino ad ora nulla di ciò che c'era lo creava: ogni elemento in argilla arrivava a mano ed era sottoposto a hashing durante il processo. Ora esiste uno strumento concetto→argilla e la sua prima coppia è stata esaminata a grandezza naturale: posa, fasce da polso, medaglia della cintura e orlo strappato sono stati inclusi; la massa della criniera no; la perdita di colore misurata sull'intera immagine è **C\* p99.9 = 13.15** con uno sfondo cromatico uniforme. **Ciò che questa coppia non può mostrare è se la mesh migliora**, che è l'unica domanda che ne promuove l'utilizzo, quindi rimane un candidato con le sue prove registrate: **[preparazione del concetto](docs/concept-prep.md)**.

## Cosa lo fa funzionare

Sei risultati, ciascuno dei quali richiede un esperimento e ciascuno dei quali può essere generalizzato al di là del soggetto che lo ha prodotto. [La versione completa, con le misurazioni](docs/findings.md).

- **Prima la forma, poi lo stile.** I ricostruttori interpretano il rumore superficiale come geometria. Un modello in argilla pulito e simile a una scultura, con piani deliberatamente esagerati, produce una topologia migliore rispetto a uno sprite stilizzato; la copia stilizzata viene generata contemporaneamente e diventa il riferimento cromatico.
- **Definisci il volto, ottieni un volto.** Un ritaglio che mostra solo il busto aggiunge dal **3,1 al 4,5 volte** più poligoni alla testa e la differenza è strutturale: palpebre separate, una ruga sulla fronte, cavità nasali modellate, non semplicemente una sfocatura più accentuata.
- **Le copie appartengono a una mesh, non a un personaggio.** Riutilizza una copia su diverse mesh e la copertura diminuisce del **62% → 22,7%**, perché le braccia si proiettano nello spazio vuoto accanto al modello. Genera le copie dalla mesh che stai per texturizzare, ogni volta.
- **L'identità appartiene al prompt.** Un elemento canonico non menzionato nel prompt appare accidentalmente e scompare allo stesso modo: questo è stato misurato quando si è scoperto che le ginocchiere dorate apparivano nell'immagine solo a causa del rumore in un ControlNet difettoso.
- **Chiedi alla geometria, non a una soglia.** Sostituire una maschera con il profilo esatto ottenuto tramite raycasting ha spostato la copertura di riferimento dal **28,4% al 39,1%** di texel validi: in modo strettamente additivo, senza diffusione e senza l'utilizzo della GPU. Il keying basato sulla mediana degli angoli è fallito tre volte qui ed è stato abbandonato.
- **Elimina ciò che nessuna telecamera può vedere, dall'atlante e mai dalla mesh.** Il 49% dei texel dell'atlante non sono visibili dall'esterno; escludere queste facce riduce l'interpolazione del 68%. Escludere invece di eliminare rende il fallimento impossibile anziché semplicemente rilevabile.

## Cosa non è stato risolto

Identificato e misurato, nella pagina principale piuttosto che in una nota a piè di pagina. [Tutti, situati nel codice](docs/known-defects.md).

- **Alcune mappe di superficie visibili corrispondono allo spazio dell'atlante che nessun processo di baking scrive mai**, e vengono renderizzate come il nero predefinito non modificato dell'immagine. Il sistema di baking di Blender utilizza un campionamento del centro texel, quindi un triangolo che non si sovrappone a nessun centro texel rimane vuoto; i suoi stessi sviluppatori
[hanno identificato il meccanismo e implementato una correzione](https://projects.blender.org/blender/blender/pulls/161752)
due settimane dopo la build su cui sono stati misurati tutti i valori qui presenti. Si tratta di una proprietà del percorso, non di un singolo oggetto: misurato su un asset, **non misurato sugli altri quattro**.
- **La fascia della lama occupa lo 0,00% del riferimento dello stadio 1** su tutte e otto le telecamere; l'acciaio su uno sfondo grigio si posiziona esattamente sulla soglia dell'immagine. L'unione recupera il 55,72%.
- **Le giunture delle texture non sono allineate.** Un confine di provenienza presenta una variazione della texture **5,5 volte** maggiore rispetto alla normale; la regione identificata dal Direttore presenta una variazione **9,5 volte** maggiore.
- **La dilatazione si estende tra isole dell'atlante non correlate**: il 74,9% dei texel dilatati trae il proprio colore da un'altra isola, con una distanza mediana di 0,177 su una figura alta 1,0. ⚠ **Questa percentuale si riferisce ai texel dell'atlante e non è un'affermazione su ciò che vede una telecamera**: la dilatazione rappresenta il 26,95% dell'atlante renderizzato e il **4,95% dei pixel della figura renderizzata**, con un rapporto di 0,18. Le texture sono presenti in grandi mappe, i vuoti in quelle piccole, quindi un texel dilatato ha un costo contenuto nello spazio dello schermo.
- **⚑ Il difetto che determina l'accettabilità è legato alla TEXTURE, non a nessun tipo di riempimento**: regioni che presentano il colore di un altro materiale, cosa che nessuna statistica sui punti può rilevare. Misurato in tre modi con tre sessioni in tre spazi: **91,05% `reference`, con un arricchimento di 0,99**, valore molto vicino alla media; la stessa classe nel verde del tessuto presenta il **68,46% `reference`**; e su una sottile lama, i texel dipinti sulla superficie presentano il **18,77%** di contaminazione rispetto al **5,55%** del riempimento della dilatazione. Il riempimento deriva correttamente dal vicino dipinto più prossimo, e questo vicino è già errato. La miscela stessa è una suddivisione a due bande non documentata (`M + gaussian_blur_σ16(B − M)`) che misura il **peggiore dei quattro** valori alternativi sugli stessi punti.
- **Le viste non sono mai indipendenti, il che limita ogni correzione della miscela.** Per ogni gruppo di difetti, il **100% delle facce con due o più telecamere contribuenti ha tutte le telecamere all'interno di un arco di 90°** (mediana di 45°) e il 21% delle facce difettose è visibile solo da una telecamera. Le viste adiacenti, sottoposte a controlli quasi identici, falliscono insieme, quindi i vantaggi multi-vista pubblicati dalla fotogrammetria non si trasferiscono qui in modo diretto.
- **Ogni ricostruzione su questo percorso è un guscio cavo a doppia parete**, con pareti di circa due voxel. Nessun predicato volumetrico è valido su uno di essi.
- **Le piastre sono diverse ai confini dei materiali non identificati, e il punto cruciale è quello** (16-08-2026). La deformazione interna della mesh rispetto alla superficie misurata ha una mediana di **3,5–11,1 px** su tutte le otto viste, rispetto alle mediane del contorno di 1,2–3,0; ogni regione residua che il Direttore ha cerchiato (taglio della manica, mano, parte superiore dello stivale) è una giunzione di materiali che il prompt di generazione non ha mai nominato. ⚠ **CORRETTO IL 17-08-2026 e la correzione affina i risultati.** In precedenza si leggeva: "il prompt registrato contiene sei elementi", ma in realtà ne fonde due diversi. Il flusso di lavoro che ha generato le copie nomina **16 su 17**, mancando solo l'impugnatura; il *profilo predefinito del pennello* ne nomina sei. Entrambe le affermazioni sono vere, e la frase conteneva un errore. Ciò che conta di più è che l'impugnatura, il bracciale, la protezione per la gamba e la mano compaiono **zero** volte nel prompt di 16 frasi, perché **non esiste alcun elemento relativo a essi nel canone**. Un prompt completo non può comunque nominare una mano che non è mai stata specificata. ✅ **CHIUSO IL 17-08-2026**: l'elenco delle superfici viene esaminato, riempito e **tutti i 24 elementi sono stati convalidati**, e il sistema ora rifiuta un prompt che non lo copre.
- **Dal 4,65 al 5,57% dei texel validi rappresentano una superficie che nessuna telecamera a anello piatto può vedere**: questi falliscono nel test del gate di profondità in ogni vista, nessun percorso di proiezione può renderizzarli e la pipeline fornita li ha riempiti con un'inondazione cieca rispetto all'isola, creando le macchie scure. Hanno bisogno di una politica (materiale neutro, pennello o accettazione), non di una correzione ([relazione E49](docs/experiments/E49-finish-and-cap-report.md)).
- **Poligoni colorati piatti sulle schede della qualità accettabile**: l'unica classe aperta del Direttore. ⚠ **L'ipotesi sul passaggio di riempimento è FALSA (17-08-2026).** Il riempimento orfano presenta un valore *inferiore* alla sua media di base nel difetto (0,27), le aree si trovano per il 90–99% su texel dipinti normali e lo stesso difetto è presente in una renderizzazione creata da un atlante che precede la correzione ritenuta responsabile. Invece, l'origine è stata individuata: la copia della vista di renderizzazione è pulita in quel punto e una **vista diversa** possiede 97 dei 115 pixel difettosi con un angolo di 0,68 rispetto a 0,60. La macchia angolare è un **artefatto di dispersione** e il colore è una reale discrepanza tra le viste su una superficie che è già stata nominata, quindi la rigenerazione della copia non è giustificata dall'affermazione "il difetto si trova nelle copie".
⚠ **E anche la correzione proposta in questa pagina è FALSA (17-08-2026).** In precedenza si leggeva: *"un compositore che preferisce la vista di destinazione rappresenta la correzione e non ha costi."* Il compositore esisteva già ed era già l'impostazione predefinita; misurato rispetto al classificatore piatto su immagini statiche provenienti da un'esecuzione registrata, la priorità alla vista di destinazione **aumenta** il conteggio nella vista di destinazione (38 → 40) e lo aumenta notevolmente in altre due viste (23 → 64, 36 → 110), diventando *più* coerente. Il meccanismo: **la forma è proprietà, il colore non lo è.** L'oliva è la texture della vista 6 di una superficie che la vista 6 sta dipingendo correttamente, quindi nella vista di destinazione 6 (dove la priorità alla vista di destinazione significa *preferire la vista 6*), la politica massimizza esattamente la texture di cui è composto il difetto. **Una politica di proprietà non può correggere una discrepanza tra i colori delle viste su una superficie correttamente attribuita**, il che porta all'abbandono dell'intera famiglia anziché solo di un ramo ([E52](docs/experiments/E52-target-first-flats-ruling.md)). Ciò che resta è una questione di texture e ha un costo in termini di generazione. *Testo precedente, mantenuto in base alla regola delle correzioni: "isole orfane delle dimensioni di singoli triangoli, riempite con colori piatti da campioni adiacenti presi con il contorno non eroso."*

## Come viene eseguito questo repository?

La disciplina è tanto un prodotto quanto lo è la pipeline, ed esiste per una ragione: una fase precedente ha previsto dieci sessioni in cui ogni partecipante valutava il proprio lavoro e scriveva delle conclusioni che venivano lette nella sessione successiva come fatti accertati. Nulla in questo ciclo era verificabile.

- **Definizione prima del lavoro, relazione dopo, decisione finale** — e la sessione che progetta un esperimento non valuta mai i propri risultati. Cinquantasei esperimenti sono disponibili in [questa sezione](docs/experiments/).
- **Le correzioni vengono inserite al loro posto, accanto alla misurazione che le ha confutate**, e non come semplici eliminazioni. Solo nella sessione iniziale sono state falsificate sei affermazioni preesistenti, e tutte e sei sono ancora leggibili accanto a ciò che le ha sostituite.
- **I fallimenti rimangono nel repository insieme alle loro motivazioni.** [`tools/superseded/`](docs/tools.md) non è un archivio: chiunque può eseguire questi strumenti e osservare i loro fallimenti nello stesso modo.
- **Un risultato negativo è un successo completo**, viene segnalato e chiuso anziché essere modificato per raggiungere un valore specifico.
- **I test sono associati al commit che modifica il codice** — 1338 superati da due persone, con CI basata sui percorsi per i 1284 elementi "ermetici".
- **La registrazione è consultabile.** Un indice SQLite + FTS5 sull'intero percorso, verificato su quattro livelli. Ha individuato un numero di decisioni che il testo presentava in modo errato in tre siti, contando la stessa registrazione.

## Dove tutto è..

| | |
|---|---|
| **[Il manuale](docs/handbook/index.md)** | la guida: le fasi del percorso, gli argomenti, il sistema di profili. |
| **[Preparazione del concetto](docs/concept-prep.md)** | il candidato "hop" di modellazione: la sua fase 0, il suo posizionamento e l'elemento della licenza che abilita. |
| **[La registrazione](docs/experiments/)** | cinquantasei esperimenti: definizione, relazione, decisione e ogni previsione dichiarata prima della misurazione. |
| **[Cosa ha imparato il percorso](docs/findings.md)** | le scoperte durature e le regole ottenute con fatica, nella loro interezza. |
| **[Stato di ogni strumento](docs/tools.md)** | cosa funziona, cosa è obsoleto e le prove per ciascuno. |
| **[Difetti noti](docs/known-defects.md)** | tutto ciò che non è stato risolto, misurato e localizzato nel codice. |
| **[Il percorso, come si è svolto](docs/arc-history.md)** | la cronologia, con le correzioni intatte. |
| **[CLAUDE.md](CLAUDE.md)** | come lavorare qui: i ruoli, le regole e il costo di ciascuno. |

## Posizione della licenza

Ogni fase viene eseguita in locale e nel rispetto delle normative commerciali: SDXL (OpenRAIL++), MV-Adapter (open), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Esclusi deliberatamente, con la relativa motivazione: **nvdiffrast** (non commerciale — applicato qui tramite un meccanismo di sicurezza strutturale, non tramite attestazione), **Hunyuan3D-Paint** (licenza non valida nell'UE, nel Regno Unito e in Corea del Sud), **MVPaint** e **TEXGen** (nessuna licenza) e **UltraSharp / SUPIR / StableSR** (upscaler non commerciali).

**Il limite dell'affermazione, dichiarato anziché lasciato alla scoperta.** Descrive il **percorso registrato**: le fasi nel diagramma sopra, dall'immagine al 3D. La fase di preparazione del modello candidata a monte attualmente viene eseguita su un'API cloud chiusa i cui termini questo repository **non ha verificato**, quindi nessuna affermazione sulla licenza qui copre un elemento creato da uno dei suoi modelli. Si tratta di un aspetto aperto con un percorso definito per risolverlo: il modello locale corretto dal punto di vista della licenza è **Qwen-Image-Edit (Apache-2.0)**, e **FLUX.1-Kontext [dev] è escluso per le stesse ragioni di nvdiffrast** — pesi non commerciali. Entrambi sono stati verificati rispetto al catalogo dei modelli dello studio anziché richiamati; la motivazione è disponibile in [preparazione del concetto](docs/concept-prep.md).

## Modello di fiducia e di minaccia

facet viene eseguito interamente sulla propria macchina: ogni strumento è uno script che si esegue su percorsi digitati, quindi la domanda utile non è *quali autorizzazioni richiede questa app*, ma *cosa fanno questi script alla tua macchina*. La risposta viene fornita tramite misurazione, con ogni ciclo ripetibile; la politica completa è disponibile in [SECURITY.md](SECURITY.md):

- **Dati interessati:** mesh, texture, immagini e JSON su disco locale, nei percorsi specificati nella riga di comando. Inoltre `docs/index/facet.db`, che è *derivato*: non contiene nulla che non fosse già un file in questo repository, e `facet_index.py build` lo rigenera da zero.
- **Dati NON interessati:** nessuna credenziale, mai. Nulla qui legge, memorizza o trasmette un token, una chiave o una password, e nessuno di questi è presente nell'albero: è stata eseguita una scansione per individuare chiavi con prefisso del provider, GitHub PAT, token Slack, ID chiave AWS, blocchi di chiavi private, token bearer e assegnazioni inline `api_key`/`password`, **zero corrispondenze**, nessun file simile a una credenziale tracciato.
- **Nessun telemetria.** Nessuna raccolta, nessuna trasmissione. Non esiste un'opzione per disattivare perché non c'è nulla da disattivare.
- **Traffico di rete:** due strumenti aprono un socket: `restylize_views.py` e `texpass_brush.py`, ed entrambi chiamano un'API HTTP ComfyUI all'indirizzo `--host`, **valore predefinito `127.0.0.1:8188`**. Nient'altro in `tools/` effettua una chiamata di rete.
- **Autorizzazioni:** utente ordinario. Nessuna elevazione, nessuna installazione del servizio, nessuna scrittura nelle impostazioni di sistema o nel registro di sistema.

Tre spigoli vivi vengono evidenziati anziché eliminati, perché una nota sulla sicurezza che elenca solo delle rassicurazioni non è un modello di minaccia: **le operazioni sui file non sono eseguite in un ambiente isolato** (uno strumento scrive ovunque lo indichino i suoi argomenti); **i percorsi locali assoluti sono incorporati in molti strumenti e documenti** — 114 occorrenze in 26 file, non si tratta di segreti ma della divulgazione del layout di una macchina e del motivo per cui la maggior parte degli strumenti non funzionerà senza modifiche altrove; e **i fallimenti imprevisti vengono visualizzati come tracce di Python negli script di ricerca non pubblicati**, senza alcun filtro `--debug`. Le interruzioni deliberate sono messaggi `ANDON:` che contengono la misurazione che le ha attivate. Questo è il contratto dello strumento di ricerca, e [SHIP_GATE.md](SHIP_GATE.md) registra esattamente quando smette di essere sufficiente — cosa che per i due comandi, nella loro versione *installs*, è avvenuta alla 0.2.0: `facet-index` e `facet-mcp` restituiscono `0` ok / `1` errore utente / `2` errore in fase di esecuzione — e, poiché [E22](docs/experiments/E22-ruling.md), **`4` RIFIUTATO** per un filtro attivato o una sezione `verify` che non funziona, il che significa che lo strumento sta funzionando e ti avvisa di non procedere anziché generare un errore in fase di esecuzione. Tutti rifiutano con un messaggio di errore strutturato che indica il passaggio successivo anziché una traccia ([E21](docs/experiments/E21-cli-contract-report.md)).

**Inoltre, i filtri in questi due comandi non sono più eliminabili.** Ogni ANDON installa `raise`; un semplice `assert` è un'istruzione che `python -O` rimuove silenziosamente e 87 dei filtri di questo repository potevano essere rimossi tramite una variabile d'ambiente fino a quando E22 non li ha modificati. Misurati prima e dopo sullo stesso filtro, in quattro modalità interprete.
**E poiché [E23](docs/experiments/E23-route-gates-report.md), nemmeno i filtri sul percorso che hanno prodotto le quattro risorse accettate sono eliminabili** — i suoi **57 siti su dodici strumenti**, convertiti come una semplice operazione sui file che non è mai stata eseguita in precedenza, ora rifiutano tutti sotto `-O` e `PYTHONOPTIMIZE=1`, nonché con un interprete normale.
**E poiché [E25](docs/experiments/E25-ruling.md), la classe è chiusa.** I suoi **133 siti su 43 file** — gli strumenti di misurazione che hanno prodotto le prove per le quattro risorse accettate sopra — si convertono nello stesso modo, portando il totale a `raise` a **278**.
Esattamente **un** semplice ANDON `assert` rimane ovunque sotto `tools/`: `superseded/texpass_thin_mask.py`, che **non viene mai convertito**, perché questi strumenti sono mantenuti in modo tale che chiunque possa eseguirli e osservare il loro fallimento nello stesso modo. Questo resto è fissato **per nome** nella suite di test, quindi una scansione futura non può eliminarlo senza modificare intenzionalmente il test.

**Stato del supporto:** questo repository viene sviluppato in modalità aperta, su un'unica piattaforma, da un unico responsabile e con sessioni a rotazione di consulenti ed esecutori. `main` è l'unico stato supportato. Non esiste un canale di rilascio, una politica di backporting o un SLA; ciò che esiste invece è la registrazione: ogni affermazione si trova accanto al codice che la produce e [docs/experiments](docs/experiments/) contiene le specifiche, il rapporto e la decisione per ciascuna di esse.

## Requisiti

Blender 5.x, Python 3.11+ con `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. È necessaria un'installazione locale di ComfyUI solo per il pennello di inpainting. Sviluppato su una RTX 5090; la quantità di VRAM disponibile è più importante della velocità pura.

Il CI esegue il sottoinsieme ermetico della suite su **ubuntu-latest / Python 3.12** con installazioni fisse (`.github/workflows/ci.yml`); il livello degli artefatti richiede gli alberi registrati in `E:\AI\training`, che non sono presenti in git, quindi il CI li esclude intenzionalmente. Localmente, `python -m pytest` esegue tutti i **1338** test e `python -m pytest -m "not artifacts"` esegue i **1284** test riprodotti dal CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
