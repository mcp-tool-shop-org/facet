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

Lo stile viene applicato **sull'asset**, nello spazio delle texture, e non viene "dipinginto" per ogni vista e poi assemblato successivamente. Fornendo alla pipeline un modello in argilla con forme esagerate, si ottiene una mesh texturizzata il cui colore deriva da un riferimento stilizzato di *quella* stessa mesh; tutto ciò che il riferimento non può vedere viene riempito tramite un pennello per l'inpainting mascherato e una dilatazione consapevole della superficie.

Prende il nome dalle due metà del problema: i poligoni e la faccia che devono rappresentare.

## Installazione

La pipeline stessa è un insieme di script locali che vengono eseguiti su percorsi specificati dall'utente; clona il repository e leggi [la guida introduttiva](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Due server vengono forniti come pacchetto**: l'indice dei record, in modo che un assistente possa interrogare la traccia delle prove anziché leggerla, e **a partire dalla versione 0.4.0 il server di misurazione**, in modo che due asset misurati a distanza di mesi utilizzino lo stesso flusso di codice.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` è il server MCP stdio che opera sui record (sei strumenti, con la verifica a quattro punti come superficie di controllo che rifiuta i dati non validi) e `facet-index` è l'indice stesso (`build` / `verify` / `q` / `claims`). Esegui uno dei due all'interno di una copia del codice; `--db` indica un indice diverso.

### Il server di misurazione: nuovo nella versione 0.4.0

`facet-measure` fornisce la **parte numerica** di un confronto e non indica mai se l'output è valido. Ogni payload contiene la versione del server, l'hash del file dello strumento e un hash della configurazione, e `measure_report` **rifiuta** di effettuare confronti tra dati incompatibili, che è la caratteristica per cui è stato progettato l'intero sistema.

Verificato eseguendo un **comando** anziché `--help`: una mesh di controllo restituisce 786.432 facce con un envelope di identità completo su una macchina che non contiene una copia del codice.

**Il risultato dipende da una sola cosa, ovvero dalla versione di Python:**

| la tua versione di Python | `[measure-full]` ti fornisce |
|---|---|
| **3.11 / 3.12** | **tutti e otto gli strumenti**: `open3d` si installa tramite PyPI |
| **3.13** | quattro strumenti: `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 is the latest *release* and publishes cp38–cp312 wheels with **no sdist**,
so on 3.13 there is nothing on PyPI to install. The extra carries it behind
`python_version < "3.13"`, so the install **succeeds** there and the four geometry tools
exit **`4` REFUSED** naming what they need — rather than the whole install failing.

**Per ottenere tutti gli otto strumenti su Python 3.13**, Open3D pubblica le versioni cp313 più recenti sul suo canale di sviluppo in continuo aggiornamento. Un URL diretto è accettabile nella riga di comando; è vietato solo all'interno dei metadati del pacchetto pubblicato:

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **Su Windows e macOS, i pacchetti di sviluppo hanno il suffisso `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` al momento della stesura) e il nome cambia quando `main` cambia; elenca gli asset nella [versione `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) e seleziona quello più recente. **Questa versione è quella rispetto alla quale sono stati misurati i numeri dipendenti da open3d della pipeline**, ed è un limite di comparabilità reale: l'envelope di identità registra l'hash dello strumento, non le sue dipendenze — [E31](docs/experiments/E31-ruling.md).

*Fino alla versione 0.3.1, il pacchetto conteneva due file `.py` e nessuno degli strumenti di misurazione, quindi un server di misurazione installato non aveva nulla da eseguire. Nessuno se n'è accorto per quattro versioni perché questo repository È la copia del codice: lo strumento funzionava dove veniva compilato e non era mai stato altrove.*

⚠ **`pip install facet-mcp` era difettoso in tutte le versioni pubblicate fino alla versione 0.3.0 ed è stato corretto nella versione 0.3.1.** Il pacchetto installa `facet_index` come modulo di livello superiore, quindi fino alla versione 0.3.0 (inclusa) risolveva la posizione del record rispetto a `<venv>/Lib`, che non contiene né il corpus né l'indice, e `build`, `claims` e `q` fallivano tutti senza `--db`.
**Sulla versione 0.3.0 o precedente, utilizza il binario `npx` sopra.**

Dalla versione 0.3.1, la radice viene risolta **verificando l'esistenza del record** anziché presupponendolo: esegui uno dei due comandi all'interno di una copia del codice e lo troverà; eseguilo da qualsiasi altra posizione ed esce con il messaggio **`4` RIFIUTATO**, indicando entrambe le directory che ha provato e entrambi i marcatori che ha cercato. `$FACET_INDEX_DB` viene ora letto da entrambi i comandi e seleziona quale *indice*, non quale *corpus*. Misurato su un pacchetto compilato da `main` e installato in un ambiente virtuale pulito — [E24](docs/experiments/E24-ruling.md).

*Questo blocco è stato corretto due volte. Inizialmente conteneva `pipx install facet-mcp # o il pacchetto Python direttamente `, until v0.3.0's read-back ran a **verb** instead of ` --help`. Successivamente affermava che il pacchetto "funziona solo per `q` e `claims`" — **`claims` non funzionava nemmeno**, cosa che E24 ha scoperto eseguendolo. Entrambe le correzioni sono presenti in [known-defects.md](docs/known-defects.md) con le relative misurazioni.*

## La situazione attuale

**Quattro asset accettati, appartenenti a quattro classi di oggetti, senza costi aggiuntivi.** Ognuno è stato valutato dal direttore con il proprio livello di zoom: sul file GLB o su fogli di dimensioni reali, e non tramite una metrica che supera una soglia.

| oggetto | classe | accettato | riferimento / pennello / dilatazione |
|---|---|---|---|
| **Character (W3)** | umanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veicolo, rigging sottile | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | animale, membrane delle ali | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | oggetto di scena, quasi bidimensionale, grigio su grigio | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Le condivisioni sono costituite da texel validi e **non sono comparabili tra oggetti diversi**: una nave nasconde gran parte di sé dalla prospettiva a livello degli occhi e un animale ne nasconde metà. Valuta ciascuno rispetto al proprio limite massimo pre-registrato, rispetto al quale ottengono un punteggio dell'**86–93%**: la differenza tra le righe è rappresentata dalla geometria, non da una regressione. [Numeri completi con i rispettivi denominatori](docs/handbook/subjects.md).

**Un quinto soggetto è a metà del ciclo e rappresenta il primo riferimento costruito, con la priorità data al riferimento stesso (2026-08-17 → 2026-08-19).** A1, "l'archivista", è stato avviato da un riferimento che contiene la sua ricetta integrata, anziché da un concetto basato su argilla, e ogni fase successiva è stata controllata in base a questo: il canone è stato approvato con **16/16 superfici** prima ancora che esistesse una mesh, una mesh è stata approvata dal direttore, una scena ha riprodotto il riferimento **pixel per pixel tre volte**, un set di otto viste gemelle con un manifesto sha256 sono stati accettati e due errori di contaminazione nominati sono stati misurati su ciascun meccanismo prima che qualsiasi cosa venisse modificata. La fase di rendering è stata approvata [2026-08-19](docs/experiments/E70-baked-look-report.md) — **in base all'identità e al set di elementi, ed è questo l'ambito completo dell'approvazione.**

**Quindi il pennello si è aperto e ora disegna solo nei fori.** Il primo tratto è stato applicato con un angolo di 90 gradi il 2026-08-19: l'invarianza ANDON ha registrato **0,014 lv con la componente calda più grande pari a 0 px** al di fuori della figura, su un totale di 472.318 px testati, e `commit` ha disegnato **3.585 texel**, riempiendo i fori **2.044.423 → 2.040.838** con l'atlas sorgente, la cui identità è stata verificata successivamente. Alla risoluzione impostata dal direttore, il triangolo pallido all'altezza del colletto e della spalla del gilet è diventato di colore viola intenso e la cucitura appare come un unico elemento. Non ha inventato un volto, non ha fatto ruotare la testa né ha dipinto un secondo gilet.

**Il risultato metodologico è più importante dell'asset.** In tutto questo processo, l'intensità del ControlNet non è mai stata modificata: ogni correzione ha **eliminato una causa** anziché applicare una forza contro di essa. Due degli errori erano difetti nelle specifiche fornite dal consulente, rilevati dai sistemi di esecuzione e da un canale di revisione esterno prima che venisse speso qualsiasi credito, ed entrambi sono indicati nel registro con la misurazione che ha portato alla loro correzione.

**Si tratta di una pipeline, non di un generatore a carattere singolo.** Contraddici le specifiche su otto elementi nominati e il prompt avrà successo in **8 casi su 8**: la deviazione mediana ΔE è pari a 46,3 rispetto a 6,2 sui cinque controlli mantenuti, mentre la figura rimane la stessa. La struttura è mantenuta dalla mesh e dal controllo; gli attributi nominati sono gestiti dal prompt.

**La questione del proiettore si è conclusa il 2026-08-16** ([E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
Le otto immagini **sono composte**: ricostruite a partire dal bundle per ciascuna vista, utilizzando pesi di bordo × orientamento × visibilità; il rendering dell'atlas ha superato la soglia di accettazione del direttore per la prima volta in questo percorso — due volte, su due cicli — rispetto a un atlas già pubblicato, il cui percorso aveva causato problemi nella resa delle immagini, e ora le immagini concordano. La catena che ha permesso ciò è contenuta in `tools/` (`emit_view_aovs`, `s3_composite`, `flow_estimate`, `s3_run`, `s3_sheet`, `atlas_from_aovs`, `twin_mesh_warp`), ed è stata realizzata principalmente attraverso un canale di revisione esterno le cui richieste di calibrazione nominate hanno avuto successo **in venti casi su venti**, e ognuna di esse è stata verificata qui eseguendola prima che qualsiasi cosa desse per scontato il risultato.

**Il canone è costituito dai dati, e determina l'utilizzo delle risorse (2026-08-17).** Le specifiche sull'identità hanno nominato diciassette elementi; il flusso di lavoro che ha generato le immagini gemelle ne ha nominati sedici; la configurazione predefinita per una nuova esecuzione ne ha nominati sei. Nessuno di essi era collegato agli altri, quindi quattro cicli hanno corretto la composizione a valle, dopo che un errore nella fonte aveva causato problemi. Il canone è ora un database indicizzato in base alla **superficie**: un elenco di elementi non può mostrare cosa manca e un elemento nullable rende un foro una riga; `canon_gate` opera **all'interno** degli strumenti che creano un risultato, prima ancora che esista la directory di output. Un risultato il cui prompt non copre il canone approvato viene rifiutato e nulla viene scritto.

**Si tratta di un router ed è configurato per essere sicuro.** Risolve un soggetto nel suo file del canone, gestisce un prompt **in entrambe le direzioni** e contiene un ambito. **Uno strumento che crea un risultato e a cui non viene fornito alcun canone non procede in modo silenzioso: lo rifiuta.** La soluzione per un soggetto che effettivamente non ne ha è supportata da dati statistici e non può essere utilizzata da un soggetto che invece ne ha: `--no-canon --subject GALLEON` procede e si identifica; `--no-canon --subject W3` viene **rifiutato**, perché W3 ha delle superfici. Questo chiude la casella di controllo per costruzione, anziché per convenzione, ed è importante perché la forma precedente — `if args.canon:` — ha permesso al driver PowerShell pubblicato di superare il controllo in silenzio.

**La seconda direzione è quella che rileva un difetto reale.** Verificare che il prompt *contenga* il canone rivela un prompt incompleto. Verificare che tutto ciò che è contenuto nel prompt *sia* parte del canone rivela una frase che nomina qualcosa che il personaggio non ha, e ce n'era uno presente nella configurazione predefinita: **`gold necklace`**, che questo repository aveva già identificato come errore nell'indicare la medaglia dorata sulla cintura, *"e l'elemento sopravvive per caso."* Un prompt completo con tale frase aggiunta ora restituisce `missing: 0` e viene comunque rifiutato, indicando la clausola.

```
canon_gate 1.0.0  census  (occupancy is not ratification)
subject      named   occupancy   ratified   prof_hit surfaces
W3              19       24/24      24/24       5/19 canon/w3.surfaces.json
GALLEON         13           -          -      11/13 NONE
DRAGON          11           -          -      10/11 NONE
LONGSWORD        5         5/5        5/5        4/5 canon/longsword.surfaces.json
E10-LAYER        1           -          -          - NONE
LOGO             0           -          -          - NONE
A1              10       16/16      16/16      10/10 canon/a1.surfaces.json
```

`prof_hit 5/19` è un **campione lasciato intenzionalmente difettoso**: si tratta della configurazione predefinita che una nuova esecuzione utilizzerebbe effettivamente, quindi il primo `--profile character.json` dovrebbe interrompere l'esecuzione. Riparare la stringa eliminerebbe le prove.

**E c'è un foglio di lavoro, perché i quattro soggetti senza canone non si muoveranno da soli.** Emette ogni superficie che il *tipo* di un soggetto implica — quindi un foro è una riga prima ancora che qualcuno lo abbia nominato — trasforma un file IDENTITY.md in un inventario, gestisce le giunture come coppie per confermare e riserva gli slot dell'ambito per ciascuna vista. È **strutturalmente incapace di riempire un elemento**, ed è questa la proprietà su cui viene testato: una frase dannosa che arriva con una superficie già assegnata non viene scritta. Generare il canone significa avere una persona che esamina un riferimento; il foglio di lavoro rende semplicemente questo processo più economico e completo.

**Il confine del portale è definito esplicitamente, non lasciato alla scoperta.** Verifica le frasi canoniche validate in entrambe le direzioni, entro un determinato ambito. Non verifica parafrasi o sinonimi: l'abbinamento semantico inserirebbe un modello all'interno di un portale, cosa che questo repository rifiuta per principio; inoltre, non verifica i singoli elementi fino a quando non viene dichiarato un ambito di visualizzazione, né se un materiale specifico è stato applicato alla superficie *corretta*. Gli slot dell'ambito esistono e le loro liste di superfici sono vuote: riempirli richiede l'intervento umano, proprio come aggiungere gli oggetti. Quattro soggetti hanno un file IDENTITY.md e nessun file JSON delle superfici: questo è stato lasciato incompiuto piuttosto che generato senza aver analizzato il riferimento.

**Viene misurato quanti elementi può contenere una richiesta (prompt), ma non raggiunge il canone.** La letteratura valuta ogni elemento aggiunto alla richiesta, con un costo in termini di presenza degli elementi stessi, entro un intervallo molto inferiore al nostro; quindi, è stato chiesto se le immagini già pagate potessero risolvere la questione. **Non possono farlo, e il motivo è strutturale:** nessun elemento nel corpus mantiene la sua frase costante mentre il numero circostante varia *e* può essere assente. Ciò che forniscono è un limite unilaterale, con cinque richieste per una singola telecamera con controllo, maschera e seme identici: su una scala di elementi da **10 a 17**, l'eliminazione non rimuove nulla di ciò che era presente a 10, mentre una modifica dell'identità allo *zero* ha spostato l'intero intervallo di calibrazione. **Il canone di W3 richiede 19, ma il corpus non lo raggiunge mai** ([E55](docs/experiments/E55-density-vs-identity-report.md)). Lo studio stampa i tre numeri che vengono combinati: 24 superfici per richiesta, 25 controlli richiesti, 19 elementi univoci; quindi, un conteggio della copertura non viene mai confrontato con una misurazione del numero di elementi.

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

Passo dopo passo, con la motivazione per ciascuno: **[il manuale](docs/handbook/index.md)**.

**Il salto tratteggiato è nuovo ed è intenzionalmente non continuo.** La prima casella del percorso riporta sempre *concetto in argilla*, e fino ad ora nulla di ciò ha portato a un risultato concreto: ogni elemento in argilla arrivava manualmente ed era elaborato durante il processo. Ora esiste uno strumento che trasforma un concetto in argilla, e la sua prima coppia è stata analizzata a grandezza naturale: posa, fasce per i polsi, medaglione della cintura e orlo strappato sono stati tutti inclusi; la massa della criniera no; la perdita di colore è stata misurata sull'intero fotogramma con **C\* p99.9 = 13.15** su uno sfondo monocromatico uniforme. **Ciò che questa coppia non può mostrare è se la mesh migliora**, ed è l'unica domanda che ne promuove l'utilizzo; quindi, rimane un candidato con le sue prove registrate: **[preparazione del concetto](docs/concept-prep.md)**.

## Cosa lo rende efficace

Sei risultati, ciascuno dei quali ha richiesto un esperimento e ciascuno dei quali si generalizza oltre il soggetto che l'ha prodotto. [La versione completa, con le misurazioni](docs/findings.md).

- **Prima la forma, poi lo stile.** I ricostruttori interpretano il rumore della superficie come geometria. Un elemento in argilla pulito e simile a una scultura, con piani deliberatamente esagerati, produce una topologia migliore rispetto a uno sprite stilizzato; l'elemento gemello stilizzato viene generato contemporaneamente e diventa il riferimento di colore.
- **Inquadra il viso, ottieni un viso.** Un ritaglio del busto aggiunge **3,1–4,5 volte** più poligoni alla testa, e la differenza è strutturale: palpebre separate, una piega sul sopracciglio, cavità delle narici modellate; non semplicemente una sfocatura meno marcata.
- **I gemelli appartengono a una mesh, non a un personaggio.** Riutilizza un elemento gemello su diverse mesh e la copertura si riduce del **62% → 22,7%**, perché le braccia si proiettano nello spazio vuoto accanto al modello. Genera elementi gemelli dalla mesh che stai per texturizzare, ogni volta.
- **L'identità appartiene alla richiesta (prompt).** Un elemento canonico non nominato nella richiesta arriva per caso e se ne andrà allo stesso modo: questo è stato misurato quando si è scoperto che le ginocchiere dorate raggiungevano l'immagine solo attraverso il rumore in un ControlNet difettoso.
- **Chiedi alla geometria, non a una soglia.** La sostituzione di una maschera chiave con l'esatta silhouette del raycast ha spostato la copertura di riferimento dal **28,4% al 39,1%** dei texel validi: strettamente additivo, nessuna diffusione, nessuna GPU. Il keying angolare-mediano è fallito tre volte qui ed è stato abbandonato.
- **Elimina ciò che nessuna telecamera può vedere, dall'atlante e mai dalla mesh.** Il 49% dei texel dell'atlante sono invisibili dall'esterno; l'esclusione di questi volti riduce l'interpolazione del **68%**. L'esclusione piuttosto che l'eliminazione rende il fallimento impossibile anziché semplicemente rilevabile.

## Cosa non è stato risolto

Nominato e misurato, nella pagina iniziale piuttosto che in una nota a piè di pagina. [Tutti, localizzati nel codice](docs/known-defects.md).

- **Alcune mappe di superficie visibili corrispondono allo spazio dell'atlante che nessun processo di baking registra**, e vengono renderizzate come il nero predefinito non modificato dell'immagine. Il sistema di baking di Blender utilizza un campionamento del centro texel, quindi un triangolo che non sovrappone alcun centro texel rimane vuoto: i suoi stessi sviluppatori
[hanno identificato il meccanismo e implementato una correzione](https://projects.blender.org/blender/blender/pulls/161752)
due settimane dopo la build su cui sono stati misurati tutti i valori qui presenti. Si tratta di una proprietà del percorso,
non di un singolo oggetto: misurato su un asset, **non misurato sugli altri quattro**.
- **La fascia della lama occupa lo 0,00% del riferimento dello stadio 1** su tutte e otto le telecamere: l'acciaio su uno sfondo grigio si posiziona esattamente sulla soglia dell'immagine di riferimento. L'unione risolve il 55,72%.
- **Le giunture delle texture non sono allineate.** Un confine di provenienza presenta una variazione della texture pari a **5,5 volte** rispetto alla normale; la regione identificata dal direttore presenta una variazione pari a **9,5 volte**.
- **La dilatazione si estende tra le isole dell'atlante non correlate**: il 74,9% dei texel dilatati trae il proprio colore da un'altra isola, con una distanza mediana di 0,177 su una figura alta 1,0. ⚠ **Questa percentuale si riferisce ai texel dell'atlante e non è un'affermazione su ciò che vede una telecamera**: la dilatazione rappresenta il 26,95% dell'atlante renderizzato e il **4,95% dei pixel della figura renderizzata**, con un rapporto di 0,18. Le texture si trovano in grandi mappe, i fori in quelle piccole, quindi un texel dilatato ha un costo contenuto nello spazio dello schermo.
- **⚑ Il difetto che determina l'accettazione è legato alla TEXTURE, non a nessun riempimento**: regioni che presentano il colore di un altro materiale, che nessuna statistica sui punti può rilevare. Misurato in tre modi con tre sessioni in tre spazi: **91,05% `reference`, con un aumento del 0,99**, perfettamente in linea con la frequenza di base; la stessa classe nel verde tessuto **68,46% `reference`**; e su una sottile lama, i texel dipinti sulla superficie **18,77%** rispetto al 5,55% del riempimento della dilatazione.
Il riempimento deriva correttamente dal vicino dipinto più prossimo, e questo vicino è già errato. La miscela stessa è una suddivisione a due bande non documentata
(`M + gaussian_blur_σ16(B − M)`) che misura il **peggiore tra quattro** valori alternativi sugli stessi punti.
- **⚑ Una superficie dipinta presenta delle bande ed è la scoperta sulla proprietà che porta all'accettazione dell'asset.** La superficie gemella di A1 è una singola tonalità continua; il baking è suddiviso in strisce verticali di diverse sfumature di pesca. `project_twins` è **"chi vince prende tutto"**: una telecamera vince ogni texel senza ombra di dubbio in base al peso della prospettiva, alla proprietà piuttosto che alla media, e la superficie è visibile dalla vista frontale e dai due quarti a 45°, che **presentano discrepanze nel valore del colore pari a R 13,0 / G 13,9 / B 18,3** sull'anello accettato. Ovunque due mappe UV sulla superficie siano di proprietà di telecamere diverse, la discrepanza si manifesta come un netto gradino, quindi **le bande sono i confini delle isole, non sporcizia**, né appartengono alla classe dei fori grigi. **Lo strumento strutturalmente non può correggerlo**: `commit` scrive solo nei texel del foro e i texel stilizzati sono congelati. Sono state identificate due soluzioni, ma nessuna è stata implementata: lasciare che la vista frontale possieda l'intera banda della testa o consentire a una miscela di giunture di **riscrivere la texture**, cosa che nessuno degli stadi in questo percorso può fare attualmente.
La media ponderata è già accumulata nello strumento e l'atlante miscelato esiste già sul disco; nessuno lo ha mostrato al direttore. **Questo era presente nella scheda da cui il baking è stato approvato** e l'approvazione copriva l'identità e l'insieme degli elementi: un difetto evidente su un artefatto accettato non è una contraddizione, ma la registrazione non deve indicare che l'approvazione copra una proprietà che nessuno ha valutato.
- **Le viste non sono mai indipendenti, il che limita ogni correzione della miscela.** Per ogni gruppo di difetti, il **100% delle superfici con due o più telecamere contribuenti si trova all'interno di un angolo di 90°** (mediana 45°) e il 21% delle superfici difettose è visibile solo da una telecamera. Le viste adiacenti sotto controlli quasi identici falliscono insieme, quindi i vantaggi multi-vista pubblicati dalla fotogrammetria non si trasferiscono qui in modo diretto.
- **Ogni ricostruzione in questo percorso è un guscio cavo a doppia parete**, con pareti di circa due voxel. Nessun predicato volumetrico è valido su uno di essi.
- **Le superfici presentano discrepanze sui confini dei materiali non identificati, e il canone è l'elemento cruciale** (2026-08-16). La deformazione dell'interno rispetto alla mesh misurata ha una mediana compresa tra **3,5 e 11,1 pixel** su tutte le otto viste rispetto alle mediane della silhouette comprese tra 1,2 e 3,0; ogni regione che il direttore ha evidenziato (taglio della manica, mano, parte superiore dello stivale) è una giuntura di materiali che l'istruzione non ha mai nominato. ⚠ **CORRETTO IL 2026-08-17 e la correzione rafforza la scoperta.**
In precedenza si leggeva: "l'istruzione registrata contiene sei elementi", ma in realtà ne unisce due diversi. Il flusso di lavoro che ha generato le superfici gemelle nomina **16 su 17**, mancando solo l'impugnatura; il *profilo predefinito del pennello* ne nomina sei. Entrambe le affermazioni sono vere e la frase conteneva un errore. Ciò che conta, ed è più importante: l'impugnatura, il bracciale, la protezione per la gamba e la mano compaiono **zero** volte nelle 16 frasi dell'istruzione, perché **non esiste alcun elemento relativo a essi nel canone**. Un'istruzione completa non può comunque nominare una mano che non è mai stata specificata.
✅ **CHIUSO IL 2026-08-17**: l'elenco delle superfici viene esaminato, completato e **tutti i 24 elementi sono stati convalidati** e il sistema ora rifiuta un'istruzione che non li copre.
- **Dal 4,65 al 5,57% dei texel validi rappresentano una superficie che nessuna telecamera a vista piatta può vedere**: questi falliscono il controllo della profondità in ogni vista, nessun percorso di proiezione può dipingerli e la pipeline fornita li ha riempiti con un'inondazione cieca rispetto all'isola, creando le macchie scure. Hanno bisogno di una politica (materiale neutro, pennello o accettazione), non di una correzione ([relazione E49](docs/experiments/E49-finish-and-cap-report.md)).
- **Poligoni colorati piatti sulle schede del livello accettato**: l'unica classe aperta del direttore. ⚠ **L'ipotesi sul passaggio di riempimento è FALSA (2026-08-17).** Il riempimento orfano misura *inferiore* alla sua frequenza di base nel difetto (0,27), le aree si trovano per il 90-99% su texel dipinti normali e lo stesso difetto è presente in un rendering creato da un atlante che precede la correzione ritenuta responsabile. Invece, l'origine è stata individuata: la superficie gemella della vista di rendering è pulita lì e una **vista diversa** possiede 97 dei 115 pixel difettosi con un angolo di visuale pari a 0,68 rispetto a 0,60. La macchia angolare è un **artefatto di dispersione** e il colore è una reale discrepanza tra le viste su una superficie che è già stata nominata, quindi la rigenerazione della superficie gemella non è giustificata dall'affermazione "il difetto si trova nelle superfici gemelle".
⚠ **E anche la correzione proposta in questa pagina è FALSA (2026-08-17).** In precedenza si leggeva: *"un compositore che preferisce la vista di destinazione è la correzione definita e non ha costi"*. Il compositore esisteva già ed era già l'impostazione predefinita; misurato rispetto al classificatore piatto sulle immagini statiche di un esecuzione registrata, la priorità alla vista di destinazione **aumenta** il conteggio nella vista di destinazione (38 → 40) e lo aumenta notevolmente in altre due viste (23 → 64, 36 → 110), diventando *più* coerente. Il meccanismo: **la forma è la proprietà, il colore non lo è.** L'oliva è la texture della vista 6 di una superficie che la vista 6 sta dipingendo correttamente, quindi nella vista di destinazione 6, dove la priorità alla vista di destinazione significa *preferire la vista 6*, la politica massimizza esattamente la texture di cui è composto il difetto. **Una politica sulla proprietà non può correggere una discrepanza tra i colori delle viste su una superficie correttamente attribuita**, il che elimina l'intera famiglia piuttosto che solo un ramo ([E52](docs/experiments/E52-target-first-flats-ruling.md)). Ciò che resta è una questione di texture e ha un costo in termini di generazione. *Testo sostituito, mantenuto in base alla regola delle correzioni: "isole orfane delle dimensioni di singoli triangoli, riempite con colori piatti da campioni adiacenti ai confini della superficie gemella presi con la silhouette non erosa".*

## Come viene eseguito questo repository

La disciplina è tanto importante quanto il processo stesso e esiste per un motivo: una fase precedente ha previsto dieci sessioni in cui ogni partecipante valutava i propri risultati e scriveva delle conclusioni che, nella sessione successiva, venivano considerate come fatti consolidati. Nulla in questo ciclo era verificabile.

- **Definizione prima del lavoro, relazione dopo, decisione finale** — e la sessione che progetta un esperimento non valuta mai i propri risultati. Sono disponibili settantadue esperimenti in [questa sezione](docs/experiments/).
- **Le correzioni vengono inserite al loro posto, accanto alla misurazione che le ha confutate**, e non come semplici eliminazioni. Solo nella sessione iniziale sono state falsificate sei affermazioni iniziali, e tutte e sei sono ancora leggibili accanto a ciò che le ha sostituite.
- **I fallimenti rimangono nel repository insieme alle loro motivazioni.** [`tools/superseded/`](docs/tools.md) non è un archivio: chiunque può eseguire questi strumenti e osservare i loro fallimenti nello stesso modo.
- **Un risultato negativo è un successo completo**, viene segnalato e chiuso anziché essere modificato per raggiungere un determinato valore.
- **I test sono associati al commit che modifica il codice** — 1346 superati con la partecipazione di due persone, con CI basata sui percorsi per i 1289 elementi ermetici.
- **La sezione è consultabile.** È disponibile un indice SQLite + FTS5 sull'intero percorso, verificato su quattro livelli. Ha individuato una serie di risultati che il testo aveva indicato in modo errato in tre punti, contando direttamente la sezione stessa.

## Dove si trova tutto

| | |
|---|---|
| **[Il manuale](docs/handbook/index.md)** | la guida: le fasi del percorso, gli argomenti e il sistema di profili |
| **[Preparazione del concetto](docs/concept-prep.md)** | il candidato per la fase di modellazione: il suo percorso iniziale (Gate 0), il suo posizionamento e l'elemento della licenza che abilita |
| **[La sezione](docs/experiments/)** | settantadue esperimenti: definizione, relazione, decisione e ogni previsione indicata prima della misurazione |
| **[Cosa ha imparato il percorso](docs/findings.md)** | i risultati duraturi e le regole ottenute con fatica, nella loro interezza |
| **[Stato di ogni strumento](docs/tools.md)** | cosa funziona, cosa è stato sostituito e le prove per ciascuno |
| **[Difetti noti](docs/known-defects.md)** | tutto ciò che non è stato risolto, misurato e localizzato nel codice |
| **[Il percorso, come si è svolto](docs/arc-history.md)** | la cronologia, con le correzioni intatte |
| **[CLAUDE.md](CLAUDE.md)** | come lavorare qui: i ruoli, le regole e il costo di ciascuno |

## Posizione della licenza

Ogni fase viene eseguita in locale e nel rispetto delle normative commerciali: SDXL (OpenRAIL++), MV-Adapter (open), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Esclusi deliberatamente, con la relativa motivazione: **nvdiffrast** (non commerciale — applicato qui tramite un meccanismo di sicurezza strutturale, e non tramite attestazione), **Hunyuan3D-Paint** (licenza non valida nell'UE, nel Regno Unito e in Corea del Sud), **MVPaint** e **TEXGen** (nessuna licenza) e **UltraSharp / SUPIR / StableSR** (strumenti di upscaling non commerciali).

**Il limite dell'affermazione, indicato esplicitamente anziché lasciato alla scoperta.** Descrive il **percorso registrato**: le fasi nel diagramma sopra, dall'immagine al 3D. La fase candidata per la preparazione del modello a monte attualmente viene eseguita su un'API cloud chiusa i cui termini questo repository **non ha verificato**, quindi nessuna affermazione di licenza qui copre un elemento creato da uno dei suoi modelli. Si tratta di un aspetto aperto con un percorso definito per risolverlo: il modello locale corretto dal punto di vista della licenza è **Qwen-Image-Edit (Apache-2.0)** e **FLUX.1-Kontext [dev] è escluso per gli stessi motivi di nvdiffrast** — pesi non commerciali. Entrambi sono stati verificati rispetto al catalogo dei modelli dello studio anziché richiamati; la motivazione è disponibile in [preparazione del concetto](docs/concept-prep.md).

## Modello di fiducia e di minaccia

facet viene eseguito interamente sulla propria macchina: ogni strumento è uno script che si esegue su percorsi digitati, quindi la domanda utile non è *quali autorizzazioni richiede questa app*, ma *cosa fanno questi script alla tua macchina*. La risposta viene fornita tramite misurazione, con ogni ciclo ripetibile; la politica completa è disponibile in [SECURITY.md](SECURITY.md):

- **Dati interessati:** mesh, texture, immagini e JSON su disco locale, nei percorsi specificati nella riga di comando. Inoltre `docs/index/facet.db`, che è *derivato*: non contiene nulla che non fosse già un file in questo repository e `facet_index.py build` lo rigenera da zero.
- **Dati NON interessati:** nessuna credenziale, mai. Nulla qui legge, memorizza o trasmette token, chiavi o password, e nessuno di questi elementi è presente nell'albero: è stata eseguita una scansione per individuare chiavi con prefisso del provider, GitHub PAT, token Slack, ID chiave AWS, blocchi di chiavi private, token bearer e assegnazioni inline `api_key`/`password`, **zero corrispondenze**, nessun file simile a una credenziale tracciato.
- **Nessun telemetria.** Nessuna raccolta o trasmissione di dati. Non è necessario disattivare nulla perché non c'è nulla da disattivare.
- **Traffico di rete:** due strumenti aprono un socket: `restylize_views.py` e `texpass_brush.py`, ed entrambi chiamano un'API HTTP ComfyUI all'indirizzo `--host`, **valore predefinito `127.0.0.1:8188`**. Nient'altro in `tools/` effettua una chiamata di rete.
- **Autorizzazioni:** utente normale. Nessun aumento dei privilegi, nessuna installazione del servizio, nessuna scrittura nelle impostazioni di sistema o nel registro di sistema.

Tre spigoli vivi vengono evidenziati anziché eliminati, perché una nota sulla sicurezza che elenca solo delle rassicurazioni non è un modello di minaccia: **le operazioni sui file non sono eseguite in un ambiente isolato** (uno strumento scrive ovunque lo indichino i suoi argomenti); **i percorsi locali assoluti sono incorporati in molti strumenti e documenti** — 114 occorrenze in 26 file, non si tratta di segreti ma della divulgazione del layout di una macchina e del motivo per cui la maggior parte degli strumenti non funzionerà senza modifiche altrove; e **i fallimenti imprevisti vengono visualizzati come tracce di Python negli script di ricerca non pubblicati**, senza alcun filtro `--debug`. Le interruzioni deliberate sono messaggi `ANDON:` che contengono la misurazione che le ha attivate. Questo è il contratto dello strumento di ricerca, e [SHIP_GATE.md](SHIP_GATE.md) registra esattamente quando smette di essere sufficiente — cosa che per i due comandi, nella loro versione *installata*, è avvenuta alla 0.2.0: `facet-index` e `facet-mcp` restituiscono `0` ok / `1` errore utente / `2` errore in fase di esecuzione — e, poiché [E22](docs/experiments/E22-ruling.md), **`4` RIFIUTATO** per un filtro attivato o una sezione `verify` che non funziona, il che significa che lo strumento sta funzionando e ti avvisa di non procedere anziché generare un errore in fase di esecuzione. Tutti rifiutano con un messaggio di errore strutturato che indica il passaggio successivo anziché una traccia ([E21](docs/experiments/E21-cli-contract-report.md)).

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

**Stato del supporto:** questo repository viene sviluppato in modo aperto, su un'unica piattaforma, da un unico responsabile e con sessioni a rotazione di consulenti ed esecutori. `main` è l'unico stato supportato. Non esiste un canale di rilascio, una politica di backporting o un SLA; al suo posto c'è la registrazione: ogni affermazione si trova accanto al codice che la produce e [docs/experiments](docs/experiments/) contiene le specifiche, il rapporto e la decisione per ciascuna di esse.

## Requisiti

Blender 5.x, Python 3.11+ con `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. È necessaria un'installazione locale di ComfyUI solo per il pennello di inpainting. Sviluppato su una RTX 5090; la quantità di VRAM disponibile è più importante della velocità pura.

Il CI esegue il sottoinsieme ermetico della suite su **ubuntu-latest / Python 3.12** con installazioni fisse (`.github/workflows/ci.yml`); il livello degli artefatti richiede gli alberi registrati in `E:\AI\training`, che non sono presenti in git, quindi il CI li esclude intenzionalmente. Localmente, `python -m pytest` esegue tutti i **1346** test e `python -m pytest -m "not artifacts"` esegue i **1289** test riprodotti dal CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
