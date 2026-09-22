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

Lo stile viene applicato **sull'asset**, nello spazio delle texture, e non viene applicato per ogni vista e poi assemblato successivamente. Fornisci alla pipeline un modello in argilla con forme esagerate e questa restituirà una mesh con texture, il cui colore deriva da un riferimento stilizzato di *quella* mesh, con tutto ciò che il riferimento non poteva vedere riempito da un pennello di inpainting mascherato e una dilatazione consapevole della superficie.

Prende il nome da entrambe le metà del problema: i poligoni e la superficie che devono rappresentare.

## Installa

La pipeline stessa è un insieme di script locali che vengono eseguiti su percorsi che si specificano: clona il repository e leggi [la guida introduttiva](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Due server vengono forniti come pacchetto**: l'indice dei record, in modo che un assistente possa interrogare la traccia delle prove invece di leggerla, e **a partire dalla versione 0.4.0, il server di misurazione**, in modo che due asset misurati a distanza di mesi utilizzino un unico percorso di codice.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` è il server MCP stdio che opera sui record (sei strumenti, con la verifica a quattro punti come superficie di controllo che rifiuta i dati non validi) e `facet-index` è l'indice stesso (`build` / `verify` / `q` / `claims`). Esegui uno dei due all'interno di una copia del codice; `--db` indica un indice diverso.

### Il server di misurazione: nuovo nella versione 0.4.0

`facet-measure` fornisce la **parte numerica** di un confronto e non indica mai se l'output è valido. Ogni payload contiene la versione del server, l'hash del file dello strumento e un hash di configurazione, e `measure_report` **rifiuta** di effettuare confronti in caso di discrepanze, che è la proprietà per cui è stato progettato l'intero sistema.

Verificato eseguendo un **comando** anziché `--help`: una mesh di controllo restituisce 786.432 facce con un envelope di identità completo su una macchina che non ha una copia del codice.

**Il risultato dipende da una sola cosa: la versione di Python.**

| La tua versione di Python | `[measure-full]` ti fornisce |
|---|---|
| **3.11 / 3.12** | **tutti e otto gli strumenti**: `open3d` si installa da PyPI |
| **3.13** | quattro strumenti: `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 è l'ultima *versione* e pubblica i pacchetti cp38–cp312 senza **sdist**, quindi sulla versione 3.13 non c'è nulla su PyPI da installare. Il pacchetto aggiuntivo lo include e lo rende disponibile tramite `python_version < "3.13"`, quindi l'installazione **ha successo** e i quattro strumenti di geometria restituiscono **`4` RIFIUTATO**, indicando ciò di cui hanno bisogno, anziché far fallire l'intera installazione.

**Per ottenere tutti e otto gli strumenti su Python 3.13**, Open3D pubblica i pacchetti cp313 più recenti sul suo canale di sviluppo in continuo aggiornamento. Un URL diretto è valido sulla riga di comando; è solo vietato all'interno dei metadati del pacchetto pubblicato:

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **Su Windows e macOS, i pacchetti di sviluppo hanno il suffisso `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` al momento della scrittura) e il nome cambia quando `main` cambia: elenca gli asset nella [versione `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) e prendi quello più recente. **Questa versione è quella rispetto alla quale sono stati misurati i numeri dipendenti da open3d di questa pipeline**, ed è un vero limite di comparabilità: l'envelope di identità registra l'hash dello strumento, non le sue dipendenze: [E31](docs/experiments/E31-ruling.md).

*Fino alla versione 0.3.1, il pacchetto conteneva due file `.py` e nessuno degli strumenti di misurazione, quindi un server di misurazione installato non aveva nulla da eseguire. Nessuno se n'è accorto per quattro versioni perché questo repository È la copia del codice: lo strumento funzionava dove veniva compilato e non era mai stato altrove.*

⚠ **`pip install facet-mcp` era difettoso in tutte le versioni pubblicate fino alla versione 0.3.0 ed è stato corretto nella versione 0.3.1.** Il pacchetto installa `facet_index` come modulo di livello superiore, quindi fino alla versione 0.3.0, risolveva la posizione del record rispetto a `<venv>/Lib`, che non contiene né il corpus né l'indice, e `build`, `claims` e `q` senza `--db` fallivano tutti.
**Sulla versione 0.3.0 o precedente, utilizza il binario `npx` sopra.**

Dalla versione 0.3.1, la radice viene risolta **verificando la presenza del record** anziché presupponendola: esegui uno dei due comandi all'interno di una copia del codice e lo troverà; eseguilo da qualsiasi altra posizione e restituirà **`4` RIFIUTATO**, indicando entrambe le directory che ha provato e entrambi i marcatori che ha cercato. `$FACET_INDEX_DB` viene ora letto da entrambi i comandi e seleziona quale *indice*, non quale *corpus*. Misurato su un pacchetto compilato da `main` e installato in un ambiente virtuale pulito: [E24](docs/experiments/E24-ruling.md).

*Questo blocco è stato corretto due volte. Inizialmente leggeva `pipx install facet-mcp # o il pacchetto Python direttamente `, until v0.3.0's read-back ran a **verb** instead of ` --help`.
Poi affermava che il pacchetto "funziona solo per `q` e `claims`" - **`claims` non funzionava nemmeno**, cosa che E24 ha scoperto eseguendolo. Entrambe le correzioni sono presenti in [known-defects.md](docs/known-defects.md) con le relative misurazioni.*

## La situazione attuale

**Quattro asset accettati, appartenenti a quattro classi di oggetti, con un punteggio di zero.** Ognuno è stato valutato dal direttore con il proprio livello di zoom: sul file GLB o su fogli di dimensioni reali, e non tramite una metrica che supera una soglia.

| oggetto | classe | accettato | riferimento / pennello / dilatazione |
|---|---|---|---|
| **Character (W3)** | umanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veicolo, rigging sottile | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bestia, membrane delle ali | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | oggetto di scena, quasi bidimensionale, grigio su grigio | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Le condivisioni sono costituite da texel validi e **non sono comparabili tra oggetti diversi**: una nave nasconde la maggior parte di sé dalla prospettiva a livello degli occhi e un animale ne nasconde metà. Valuta ciascuno rispetto al proprio limite di copertura pre-registrato, rispetto al quale ottengono un punteggio dell'**86-93%**: la differenza tra le righe è la geometria, non la regressione. [Numeri completi, con i rispettivi denominatori](docs/handbook/subjects.md).

**Un quinto soggetto è a metà del ciclo e rappresenta il primo riferimento costruito
(2026-08-17 → 2026-08-19).** A1, "l'archivista", è stato avviato da un riferimento che contiene
la sua ricetta incorporata, anziché da un concetto basato su argilla, e ogni fase successiva è
stata vincolata a tale riferimento: il canone è stato approvato su **16/16 superfici** prima
che esistesse una mesh, una mesh è stata approvata dal direttore, una scena ha riprodotto il
riferimento **pixel per pixel, tre volte**, un set di otto viste con un manifesto sha256 è
stato accettato e sono stati rilevati due errori di contaminazione, ciascuno dei quali è stato
misurato su un meccanismo prima che venisse apportata qualsiasi modifica. La fase di rendering
è stata approvata [2026-08-19](docs/experiments/E70-baked-look-report.md) — **sulla base
dell'identità e dell'insieme di elementi, e questo è l'ambito completo di tale approvazione.**

**Quindi, il pennello si è aperto e disegna solo all'interno dei fori.** Il primo tratto è stato
applicato con un angolo di 90 gradi il 2026-08-19: l'invarianza ANDON ha restituito **0,014 lv
con la componente calda più grande di 0 px** al di fuori della figura, su 472.318 px testati,
e `commit` ha disegnato **3.585 texel**, riempiendo i fori **2.044.423 → 2.040.838**, con l'atlante
di origine verificato nuovamente byte per byte in seguito. All'ingrandimento del direttore, il
triangolo pallido sul colletto del gilet si è trasformato in un colore viola intenso e la cucitura
appare come un unico elemento. Non ha inventato un volto, non ha ruotato la testa né ha
dipinto un secondo gilet.

**Il risultato metodologico è più importante dell'asset.** In tutto questo processo, l'intensità
di ControlNet non è mai stata modificata: ogni correzione ha **eliminato una causa** anziché
esercitare una forza su di essa. Due degli errori erano difetti nelle specifiche fornite dal
consulente, rilevati dai sistemi di esecuzione e da un canale di revisione esterno prima che
venisse speso un credito, ed entrambi sono indicati nel registro con la misurazione che li ha
invalidati.

**Si tratta di una pipeline, non di un generatore di un singolo elemento.** Contraddici le
specifiche su otto elementi nominati e il prompt vince **8 su 8** — la deviazione mediana ΔE è
di 46,3 rispetto a 6,2 su cinque controlli mantenuti — mentre la figura rimane la stessa
persona. La struttura è mantenuta dalla mesh e dal controllo; gli attributi nominati sono
legati al prompt.

**La questione del proiettore è stata risolta il 2026-08-16** ([E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
Le otto immagini **compongono**: ricostruite a partire dal bundle per ogni vista, utilizzando
pesi di bordo × orientamento × visibilità, i rendering dell'atlante hanno superato per la
prima volta la soglia di accettazione del direttore in questo percorso — due volte, in due
fasi — accanto a un atlante pubblicato il cui percorso stava distruggendo l'immagine, ma le
immagini concordano. La catena che ha permesso questo è in `tools/` (`emit_view_aovs`, `s3_composite`, `flow_estimate`, `s3_run`, `s3_sheet`, `atlas_from_aovs`, `twin_mesh_warp`),
costruita in gran parte attraverso un canale di revisione esterno, le cui richieste di calibrazione
indicate sono state mantenute **venti su venti**, ognuna delle quali è stata verificata qui
eseguendola prima che qualsiasi cosa desse per scontato il risultato.

**Il canone è un insieme di dati e determina l'utilizzo delle risorse (2026-08-17).** Le
specifiche sull'identità hanno indicato diciassette elementi; il flusso di lavoro che ha generato
le immagini gemelle ha indicato sedici; le impostazioni predefinite del profilo, che sarebbero
state utilizzate in una nuova esecuzione, hanno indicato sei. Nessuno di questi elementi era
collegato, quindi quattro fasi hanno corretto la composizione a valle di un'immagine che era
errata nella fonte. Il canone è ora un database indicizzato per **superficie** — un elenco di
elementi non può mostrare cosa manca e un elemento nullable rende un foro una riga — e `canon_gate`
funziona **all'interno** degli strumenti che creano un'immagine, prima che esista la directory
di output. Un'immagine il cui prompt non copre il canone approvato viene rifiutata e non viene
scritto nulla.

**Si tratta di un router ed è configurato per il fallimento sicuro.** Risolve un soggetto nel suo
file di canone, copre un prompt in **entrambe** le direzioni e contiene un ambito. **Uno
strumento che crea un'immagine e a cui non viene fornito alcun canone non procede in modo
silenzioso: lo rifiuta.** La soluzione per un soggetto che non ne ha affatto è supportata da
dati statistici e non può essere utilizzata da un soggetto che ne ha: `--no-canon --subject GALLEON` procede e si
annuncia; `--no-canon --subject W3` viene **rifiutato**, perché W3 ha delle superfici. Questo chiude la casella di
controllo per costruzione, anziché per convenzione, ed è importante perché la forma precedente
— `if args.canon:` — ha permesso al driver PowerShell pubblicato di superare il controllo in silenzio.

**La seconda direzione è quella che rileva un difetto reale.** Verificare che il prompt *contenga*
il canone individua un prompt debole. Verificare che tutto nel prompt *sia* canone individua
una frase che nomina qualcosa che il personaggio non ha — e ce n'era una nell'impostazione
predefinita: **`gold necklace`**, che questo repository aveva già identificato come un errore nella
denominazione del medaglione della cintura dorata, *"e l'elemento sopravvive per caso."* Un
prompt che copre con quella frase aggiunta ora restituisce `missing: 0` e viene comunque rifiutato,
indicando la clausola.

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

`prof_hit 5/19` è un **campione lasciato intenzionalmente difettoso**: è l'impostazione predefinita che
un'esecuzione utilizzerebbe effettivamente, quindi il primo `--profile character.json` dovrebbe interrompersi.
Riparare la stringa eliminerebbe le prove.

**E c'è un foglio di calcolo, perché i quattro soggetti che non hanno un canone non si
muoveranno da soli.** Emette ogni superficie che il *tipo* di un soggetto implica — quindi un
foro è una riga prima che qualcuno lo abbia nominato — trasforma un file IDENTITY.md in un
inventario, gestisce le giunture come coppie per confermare e riserva gli slot di ambito per
ogni vista. È **strutturalmente incapace di riempire un elemento**, ed è questa la proprietà
che viene testata: una frase tossica che arriva con una superficie già assegnata non viene
scritta. Generare un canone è un essere umano che segue un riferimento; il foglio di calcolo
rende semplicemente il processo più economico e completo.

**Il confine del modello è definito esplicitamente, piuttosto che lasciato alla scoperta.** Verifica le frasi canoniche approvate in entrambe le direzioni, entro un determinato ambito. Non verifica parafrasi o sinonimi, poiché la corrispondenza semantica inserirebbe un modello all'interno di un confine, cosa che questo repository rifiuta in linea di principio, né verifica i singoli elementi fino a quando non viene dichiarato un ambito di visualizzazione, né se un materiale specifico è stato applicato alla superficie *corretta*. Gli slot di ambito esistono e le loro liste di superfici sono vuote: riempirli richiede l'intervento umano, proprio come riempire gli spazi con gli oggetti. Quattro soggetti hanno un file IDENTITY.md e nessun file JSON delle superfici, lasciati incompiuti piuttosto che generati senza aver esaminato il riferimento.

**Viene misurato il numero di elementi che un prompt può contenere, e questo numero non raggiunge il valore canonico.** La letteratura valuta ogni elemento aggiunto a un prompt, con un costo che influisce sulla possibilità che gli elementi vengano effettivamente visualizzati, in un intervallo molto inferiore al nostro, quindi un utente di Opus ha chiesto se le immagini già pagate potessero risolvere il problema. **Non possono, e il motivo è strutturale:** nessun elemento nel corpus mantiene la sua frase costante mentre il numero di elementi circostanti varia *e* può essere assente. Ciò che forniscono è un limite unilaterale, con cinque prompt in una singola fotocamera con controllo, maschera e seme identici: su una scala di elementi da **10 a 17**, la rimozione di elementi non ha prodotto **nulla** di diverso rispetto a quando c'erano 10 elementi, mentre una modifica dell'identità a *zero* elementi ha spostato l'intero intervallo di calibrazione. **Il canone di W3 richiede 19 elementi, ma il corpus non lo raggiunge mai** ([E55](docs/experiments/E55-density-vs-identity-report.md)). Lo studio stampa i tre numeri che vengono combinati: 24 superfici di prompt, 25 controlli richiesti, 19 elementi univoci, quindi un conteggio della copertura non viene mai confrontato con una misurazione del numero di elementi.

**Un sesto soggetto è stato coinvolto per rispondere a una domanda diversa e ha fornito un risultato negativo (2026-09-22).** È stato ricostruito un modello di guardia per `ai-rpg-stage` per testare cosa succede *dopo* l'applicazione della vernice (pose e oggetti di scena), e la ricostruzione avviene correttamente, ma poi **fallisce l'auto-rigging.** Quattro possibili cause sono state eliminate tramite misurazione, piuttosto che tramite argomentazione: input non texturizzato, numero di componenti, topologia della mesh e la posa. **Il discriminatore non è stato identificato** e [`canon/BASE-FIGURE.md`](canon/BASE-FIGURE.md) contiene la tabella di ciò che è stato provato, pur rifiutandosi di indicare una causa, perché l'unica causa che questo repository ha identificato, la separazione tra braccio e torso, è stata smentita nello stesso lasso di tempo da una posa A reale che ha fallito con una separazione *maggiore* rispetto a una posa che ha avuto successo.

**Il risultato è un vincolo di dimensione e due confini.** Ogni ricostruzione che segue questo percorso viene normalizzata a **1,002 sul suo asse più lungo**, misurata su quattro risorse non correlate, con tre decimali, quindi una mesh di oggetti di scena non ha una vera scala e uno schermo protettivo caricato così com'è è una porta di 1,8 m. La dimensione reale di un oggetto di scena viene ora dichiarata una sola volta in millimetri, memorizzata accanto al file e verificata anziché considerata come un dato certo (`tools/prop_scale.py`, unità di scena **1,0 = 1,8 m**). Un oggetto di scena che *tocca* una figura in un singolo vertice non viene mantenuto, quindi il confine di contatto segnala una distanza minima **e un'area di contatto** (`tools/verify/prop_contact.py`): la risorsa che ha innescato questo controllo ha toccato in 0,00072 punti su 97, su un totale di 624.510, e chiaramente non era in presa. E il risultato di un auto-rig viene ora letto anziché presupposto: `tools/verify/rig_report.py` indica le giunture, confronta la mesh come un *insieme* piuttosto che come un conteggio e indica se lo skinning è presente.

**Una mano con sei dita ha raggiunto un foglio accettabile superando quattro confini che non potevano "vedere" le mani.** Il direttore l'ha trovata semplicemente guardando. La clausola 7 del canone (cinque dita per mano) esiste perché la clausola 2 l'ha resa necessaria, e ora le mani sono un elemento di accettazione durante lo zoom, piuttosto che qualcosa di cui le metriche tacevano.

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

**Il salto tratteggiato è nuovo ed è intenzionalmente non continuo.** La prima casella del percorso ha sempre indicato *concetto in argilla*, e fino ad ora nulla di ciò ha prodotto un modello reale: ogni modello in argilla è arrivato manualmente ed è stato elaborato durante il processo. Ora esiste uno strumento che trasforma un concetto in un modello in argilla e la prima coppia è stata elaborata a dimensione reale: posa, fasce da polso, medaglione sulla cintura e orlo strappato sono stati inclusi; la massa della criniera no; la perdita di colore è stata misurata sull'intero fotogramma con **C\* p99.9 = 13.15** con uno sfondo monocromatico uniforme. **Ciò che questa coppia non può mostrare è se la mesh risultante è migliore**, che è l'unica domanda che la promuoverebbe, quindi rimane un candidato con le sue prove registrate: **[preparazione del concetto](docs/concept-prep.md)**.

## Cosa lo rende efficace

Sei risultati, ciascuno dei quali ha richiesto un esperimento e ciascuno dei quali si generalizza oltre il soggetto che lo ha prodotto. [La versione completa, con le misurazioni](docs/findings.md).

- **Prima la forma, poi lo stile.** I ricostruttori interpretano il rumore superficiale come geometria. Un modello di argilla pulito, simile a una scultura, con piani deliberatamente esagerati, produce una topologia migliore rispetto a uno sprite stilizzato; la copia stilizzata viene generata contemporaneamente e diventa il riferimento cromatico.
- **Definisci il volto, ottieni un volto.** Un ritaglio che mostra solo il busto aggiunge il **310–450%** di poligoni alla testa e la differenza è strutturale: palpebre separate, un'arcata sopraccigliare, cavità nasali modellate, e non semplicemente una sfocatura più accentuata.
- **Le copie appartengono a una mesh, non a un personaggio.** Riutilizza una copia su diverse mesh e la copertura si riduce del **62% → 22,7%**, perché le braccia si proiettano nello spazio vuoto accanto al modello. Genera le copie dalla mesh su cui stai per applicare le texture, ogni volta.
- **L'identità appartiene al prompt.** Un elemento canonico non menzionato nel prompt viene aggiunto per caso e scomparirà allo stesso modo: questo è stato misurato quando le ginocchiere dorate si sono rivelate visibili nell'immagine solo a causa del rumore in un ControlNet difettoso.
- **Chiedi alla geometria, non a una soglia.** Sostituire una maschera basata su chiave con la silhouette esatta ottenuta tramite raycasting ha spostato la copertura di riferimento del **28,4% → 39,1%** di texel validi: in modo strettamente additivo, senza diffusione, senza GPU. Il keying basato sulla mediana degli angoli ha fallito **quattro** volte qui ed è stato abbandonato: al suo posto, una sfumatura dipinta, un rendering di argilla in scala di grigi, uno sfondo di studio illuminato di un modello di diffusione e un riferimento di diffusione i cui angoli coprono L\* 48,1–81,1. ⚠ La forma è ancora presente in un prodotto, `tools/verify/gate_mesh.py`, che campiona un singolo angolo: è indicata esplicitamente invece di essere gestita in modo silenzioso.
- **Elimina ciò che nessuna telecamera può vedere, dall'atlante e mai dalla mesh.** Il 49% dei texel dell'atlante non è visibile dall'esterno; escludere questi elementi riduce l'interpolazione del 68%. Escludere invece di eliminare rende il fallimento impossibile anziché semplicemente rilevabile.

## Cosa non è stato risolto

Indicato e misurato, nella pagina principale anziché in una nota a piè di pagina. [Tutti, presenti nel codice](docs/known-defects.md).

- **Alcune mappe di superficie visibili corrispondono allo spazio dell'atlante, ma nessuna delle operazioni di baking le modifica**, e vengono renderizzate come il nero predefinito non modificato dell'immagine. Il sistema di baking di Blender utilizza il campionamento del centro del texel, quindi un triangolo che non si sovrappone al centro di alcun texel rimane vuoto; i suoi stessi sviluppatori
[hanno identificato il meccanismo e implementato una correzione](https://projects.blender.org/blender/blender/pulls/161752)
due settimane dopo la build su cui sono stati effettuati tutti i test. Si tratta di una proprietà del percorso,
non di un singolo oggetto: testato su un asset, **non testato sugli altri quattro**.
- **La fascia della lama occupa lo 0,00% del riferimento della fase 1** su tutte e otto le telecamere: l'acciaio su uno sfondo grigio si posiziona esattamente sulla soglia della chiave. L'unione risolve il 55,72%.
- **Le giunture delle texture non sono allineate.** Un confine di provenienza presenta una variazione di texture **5,5 volte** maggiore rispetto alla variazione ordinaria; la regione identificata dal direttore presenta una variazione **9,5 volte** maggiore.
- **La dilatazione si estende tra le isole dell'atlante non correlate:** il 74,9% dei texel dilatati prendono il loro
colore da un'altra isola, con una distanza mediana di 0,177 su una figura alta 1,0. ⚠ **Questa percentuale si riferisce ai texel dell'atlante e non è un'affermazione su ciò che una telecamera vede**: la dilatazione rappresenta il 26,95% dell'atlante renderizzato e il **4,95% dei pixel renderizzati della figura**, con un rapporto di 0,18. Le texture si trovano su aree ampie, i vuoti su aree piccole, quindi un texel dilatato ha un costo contenuto in termini di spazio sullo schermo.
- **⚑ Il difetto che determina l'accettabilità è legato alla TEXTURE, non a nessun riempimento:** regioni che presentano il colore di un altro materiale, che nessuna statistica sui punti può rilevare. Misurato in tre modi, in tre sessioni e in tre spazi: **91,05% `reference`, con un aumento del 0,99**, perfettamente in linea con il valore di base; la stessa classe nel verde del tessuto **68,46% `reference`**; e su una sottile lama, i texel dipinti sulla superficie **18,77%** rispetto al 5,55% del riempimento di dilatazione.
Il riempimento proviene correttamente dal vicino dipinto più vicino, e questo vicino è già
errato. La miscela stessa è una suddivisione a due bande non documentata
(`M + gaussian_blur_σ16(B − M)`) che misura il **peggiore dei quattro** valori possibili sugli stessi
punti.
- **⚑ Una superficie dipinta presenta delle bande e questo è il criterio di proprietà di cui sopra che si applica a un asset accettabile.** La superficie gemella di A1 è un'unica area continua; la texture è suddivisa in strisce verticali di diverse tonalità di pesca. `project_twins` è **"chi vince prende tutto"**: una telecamera vince ogni texel in modo definitivo in base al peso della superficie, alla proprietà piuttosto che alla media, e la superficie è visibile dalla vista frontale e dalle due viste a 45°, che **presentano una discrepanza nel valore del colore di R 13,0 / G 13,9 / B 18,3** sull'anello accettabile. Ovunque due mappe UV sulla superficie siano di proprietà di telecamere diverse, la discrepanza si manifesta come un netto gradino, quindi **le bande sono i confini delle isole, non sporcizia** e nemmeno la classe del "buco grigio". **Lo strumento non può correggerlo strutturalmente**: `commit` scrive solo sui texel del buco e i texel con texture sono bloccati. Sono state identificate due soluzioni, ma nessuna è stata implementata: lasciare che la vista frontale possieda l'intera banda della testa, oppure consentire a una miscela di giunture di **riscrivere la texture del colore**, cosa che nessuna fase di questo percorso può fare attualmente.
La media ponderata è già stata calcolata nello strumento e l'atlante miscelato esiste già
sul disco; nessuno l'ha ancora mostrato al direttore. **Questo era presente nella scheda da cui è stata approvata la texture** e l'approvazione copriva l'identità e l'insieme degli elementi: un difetto evidente su un artefatto accettabile non è una contraddizione, ma la registrazione non deve indicare che l'approvazione copra una proprietà che nessuno ha valutato.
- **Le viste non sono mai indipendenti, il che limita ogni correzione della miscela.** Per ogni gruppo di difetti, il **100% delle superfici con due o più telecamere che contribuiscono si trova all'interno di un angolo di 90°** (mediana 45°) e il 21% delle superfici difettose è visibile solo da una telecamera. Le viste adiacenti con controlli quasi identici falliscono insieme, quindi i vantaggi multi-vista pubblicati dalla fotogrammetria non si trasferiscono qui in modo diretto.
- **Ogni ricostruzione in questo percorso è un guscio cavo a doppia parete**, con pareti di circa due voxel. Nessun predicato volumetrico è valido su uno di essi.
- **Le superfici presentano discrepanze sui confini dei materiali non identificati e il punto di riferimento è cruciale** (16-08-2026). La deformazione dell'interno rispetto alla mesh è stata misurata in **3,5–11,1 px (mediana)** su tutte e otto le viste rispetto alle mediane della silhouette di 1,2–3,0; ogni regione che il direttore ha evidenziato (taglio della manica, mano, parte superiore dello stivale) è una giuntura di materiali che il prompt di generazione non ha mai nominato. ⚠ **CORRETTO il 17-08-2026 e la correzione rafforza la scoperta.** In precedenza si leggeva: "il prompt registrato contiene sei elementi", ma in realtà ne fonde due diversi. Il flusso di lavoro che ha generato le superfici gemelle ne nomina **16 su 17**, mancando solo la presa; il *profilo predefinito del pennello* ne nomina sei. Entrambe le affermazioni sono vere e la frase conteneva un'affermazione falsa. Ciò che conta di più è che la presa, il bracciale, la ginocchiera e la mano compaiono **zero** volte nel prompt di 16 frasi, perché **non esiste alcun elemento per essi nel punto di riferimento**. Un prompt completo non può comunque nominare una mano che non è mai stata specificata.
✅ **CHIUSO il 17-08-2026**: l'elenco delle superfici è stato esaminato, completato e **24/24 elementi sono stati convalidati** e il sistema ora rifiuta un prompt che non li copre.
- **Dal 4,65 al 5,57% dei texel validi sono superfici che nessuna telecamera con anello piatto può vedere:** non superano il controllo della profondità in nessuna vista, nessuna traiettoria di proiezione può renderizzarli e la pipeline fornita li ha riempiti con un'inondazione cieca rispetto all'isola, creando le macchie scure. Hanno bisogno di una politica (materiale neutro, pennello o accettazione), non di una correzione ([relazione E49](docs/experiments/E49-finish-and-cap-report.md)).
- **Poligoni colorati piatti sulle schede di qualità accettabile:** l'unica classe aperta del direttore.
⚠ **L'ipotesi del passaggio di riempimento è FALSIFICATA (17-08-2026).** Il riempimento orfano è inferiore al proprio valore di base nel difetto (0,27x), le aree si trovano per il 90–99% su texel dipinti normali e lo stesso difetto è presente in un rendering creato da un atlante che precede la correzione ritenuta responsabile. Invece, è stato individuato nella sua origine: la superficie gemella della vista di rendering è pulita e una **vista diversa** possiede 97 dei 115 pixel difettosi con un angolo di 0,68 rispetto a 0,60. La macchia angolare è un **artefatto di dispersione** e il colore è una reale discrepanza tra le viste su una superficie che è già stata identificata, quindi la rigenerazione della superficie gemella non è giustificata dal fatto che "il difetto si trova nelle superfici gemelle".
⚠ **E anche la correzione proposta in questa pagina è FALSIFICATA (17-08-2026).** Si leggeva: *"un compositore che preferisce la vista di destinazione è la correzione più efficace e non ha costi"*. Il compositore esisteva già ed era già l'impostazione predefinita; misurato rispetto al classificatore piatto sulle immagini di un'esecuzione registrata, la priorità alla vista di destinazione **aumenta** il conteggio nella vista di destinazione (38 → 40) e lo aumenta notevolmente in altre due (23 → 64, 36 → 110), diventando *più* coerente. Il meccanismo: **la forma è la proprietà, il colore non lo è.** L'oliva è la texture della vista 6 di una superficie che la vista 6 sta dipingendo correttamente, quindi nella vista di destinazione 6, dove la priorità alla vista di destinazione significa *dare la priorità alla vista 6*, la politica massimizza esattamente la texture di cui è composto il difetto. **Una politica di proprietà non può correggere una discrepanza di colore tra le viste su una superficie correttamente attribuita**, il che elimina l'intera famiglia piuttosto che solo un ramo ([E52](docs/experiments/E52-target-first-flats-ruling.md)). Ciò che resta è una questione di texture e ha un costo di generazione. *Testo sostituito, conservato in base alla regola delle correzioni: "isole orfane delle dimensioni di singoli triangoli, riempite in modo piatto da campioni adiacenti presi con la silhouette non erosa".*

- **Una ricostruzione che non eseguirà il rigging automatico, senza un discriminatore noto.** Uno dei sei soggetti viene ricostruito correttamente e il rigging automatico fallisce. Input senza texture, numero di componenti, topologia della mesh e la posa vengono eliminati ciascuno tramite misurazione, e la causa per cui questo repository *ha* indicato è stata falsificata nella stessa ora, quindi la tabella rimane senza. L'impostazione di un rig che esiste ha un limite misurato piuttosto che una correzione: circa 20 gradi di rotazione del braccio rimangono stabili, circa 110 gradi danneggiano le spalle e il collegamento rigido della piastra [non lo ripara](docs/tools.md); tutti e tre i tentativi di riparazione sono stati misurati e tutti e tre sono falliti.
- **Nessun elemento di scena è stato montato e accettato.** Il contratto di dimensione e il controllo di contatto esistono e vengono testati su mesh sintetiche a una distanza nota. Nulla è stato ancora posizionato in una mano e valutato durante lo zoom del Direttore, e fino a quando ciò non accadrà, il controllo sarà uno strumento privo di punti di riferimento su un asset reale.

## Come funziona questo repository

La disciplina è tanto importante quanto il processo, ed esiste per un motivo: un ciclo precedente ha eseguito dieci sessioni in cui ciascuna ha valutato il proprio output e ha scritto conclusioni che la sessione successiva ha considerato come fatti stabiliti. Nulla in quel ciclo era verificabile.

- **Definizione prima del lavoro, relazione dopo, valutazione finale** e la sessione che progetta un esperimento non valuta mai i propri risultati. Settantatré esperimenti sono presenti in [la documentazione](docs/experiments/).
- **Le correzioni vengono applicate al loro posto, accanto alla misurazione che le ha confutate**, mai come semplici eliminazioni. Sei affermazioni ereditate sono state falsificate nella sessione iniziale, e tutte e sei sono ancora leggibili accanto a ciò che le ha sostituite.
- **I fallimenti rimangono nel repository con la loro motivazione.** [`tools/superseded/`](docs/tools.md) non è un archivio: chiunque può eseguire questi strumenti e osservare il loro fallimento nello stesso modo.
- **Un risultato negativo è un successo completo**, segnalato e chiuso piuttosto che modificato per raggiungere un valore specifico.
- **I test sono collegati al commit che tocca il codice** — 1376 superati da due persone, con CI basato sui percorsi per i 1319 elementi ermetici.
- **La documentazione è consultabile.** Un indice SQLite + FTS5 sull'intero percorso, verificato su quattro elementi. Ha trovato un numero di valutazioni che il testo aveva indicato in modo errato in tre punti, contando la documentazione stessa.

## Dove si trova tutto

| | |
|---|---|
| **[Il manuale](docs/handbook/index.md)** | la guida: la sequenza delle fasi, i soggetti, il sistema di profili |
| **[Elementi di scena e rig](docs/handbook/props-and-rigs.md)** | la fase successiva alla verniciatura: il soggetto che non eseguirà il rigging automatico e i due contratti che rendono un elemento di scena un elemento di scena |
| **[Preparazione del concetto](docs/concept-prep.md)** | il candidato per la modellazione in argilla: il suo percorso iniziale, il suo posizionamento e l'elemento di licenza che apre |
| **[La documentazione](docs/experiments/)** | settantatré esperimenti: definizione, relazione, valutazione e ogni previsione indicata prima della misurazione |
| **[Cosa ha imparato il processo](docs/findings.md)** | i risultati duraturi e le regole ottenute con fatica, nella loro interezza |
| **[Stato di ogni strumento](docs/tools.md)** | cosa funziona, cosa è obsoleto e le prove per ciascuno |
| **[Difetti noti](docs/known-defects.md)** | tutto ciò che non è stato risolto, misurato e localizzato nel codice |
| **[Il ciclo, come è avvenuto](docs/arc-history.md)** | la cronologia, con le correzioni intatte |
| **[CLAUDE.md](CLAUDE.md)** | come lavorare qui: i ruoli, le regole e il costo di ciascuno |

## Posizione della licenza

Ogni fase viene eseguita localmente e in modo commercialmente corretto: SDXL (OpenRAIL++), MV-Adapter (open), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Deliberatamente escluso, con la motivazione: **nvdiffrast** (non commerciale, applicato qui da un meccanismo di sicurezza strutturale, non tramite attestazione), **Hunyuan3D-Paint** (licenza non valida nell'UE, nel Regno Unito e in Corea del Sud), **MVPaint** e **TEXGen** (nessuna licenza) e **UltraSharp / SUPIR / StableSR** (upscaler non commerciali).

**Il limite dell'affermazione, indicato piuttosto che lasciato alla scoperta.** Descrive il **processo registrato**: le fasi nel diagramma sopra, dall'immagine al 3D. La fase di preparazione del modello in argilla a monte attualmente viene eseguita su un'API cloud chiusa i cui termini questo repository **non ha verificato**, quindi nessuna affermazione di licenza qui copre un asset creato da uno dei suoi modelli in argilla. Questo è un elemento aperto con un percorso definito per risolverlo: il modello locale corretto per la licenza è **Qwen-Image-Edit (Apache-2.0)** e **FLUX.1-Kontext [dev] è escluso per le stesse ragioni di nvdiffrast**: pesi non commerciali. Entrambi sono stati verificati rispetto al catalogo dei modelli dello studio piuttosto che richiamati; la motivazione è in [preparazione del concetto](docs/concept-prep.md).

## Modello di fiducia e di minaccia

facet viene eseguito interamente sulla tua macchina: ogni strumento è uno script che esegui su percorsi che digiti, quindi la domanda utile non è *quali autorizzazioni richiede questa app* ma *cosa fanno questi script alla tua macchina*. Risposta fornita tramite misurazione, con ogni ciclo eseguibile di nuovo; la politica completa è in [SECURITY.md](SECURITY.md):

- **Dati interessati:** mesh, texture, immagini e file JSON sul disco locale, nei percorsi specificati nella riga di comando. Inoltre, `docs/index/facet.db`, che è *derivato*: non contiene nulla che non fosse già un file in questo repository e `facet_index.py build` lo rigenera da zero.
- **Dati NON interessati:** nessuna credenziale, mai. Nessun elemento legge, memorizza o trasmette token, chiavi o password, e nessuno di questi è presente nell'albero: è stata effettuata una scansione per chiavi con prefisso del provider, GitHub PAT, token Slack, ID chiave AWS, blocchi di chiavi private, token bearer e assegnazioni inline `api_key`/`password`, **nessuna corrispondenza**, nessun file che assomigli a una credenziale è stato rilevato.
- **Nessun telemetria.** Nessun dato raccolto, nessun dato inviato. Non è prevista alcuna opzione di esclusione perché non c'è nulla da cui escludere.
- **Traffico di rete in uscita:** due strumenti aprono un socket: `restylize_views.py` e `texpass_brush.py`, ed entrambi chiamano un'API HTTP di ComfyUI all'indirizzo `--host`, **valore predefinito `127.0.0.1:8188`**. Nessun altro elemento in `tools/` effettua chiamate di rete.
- **Autorizzazioni:** utente standard. Nessun aumento di privilegi, nessuna installazione di servizio, nessuna scrittura nelle impostazioni di sistema o nel registro di sistema.

Vengono evidenziati tre aspetti importanti, piuttosto che negati, perché una nota di sicurezza che elenca solo garanzie non è un modello di minaccia: **le operazioni sui file non sono eseguite in un ambiente isolato** (uno strumento scrive ovunque indichino i suoi argomenti); **i percorsi locali assoluti sono incorporati in molti strumenti e documenti**: 114 occorrenze in 26 file, non si tratta di segreti, ma di una divulgazione della struttura di una macchina e del motivo per cui la maggior parte degli strumenti non funzionerà senza modifiche altrove; e **i fallimenti imprevisti si manifestano come tracce di Python negli script di ricerca non pubblicati**, senza alcun filtro `--debug`. Le interruzioni deliberate sono messaggi `ANDON:` che contengono la misurazione che le ha attivate. Questo è il contratto dello strumento di ricerca e [SHIP_GATE.md](SHIP_GATE.md) registra esattamente quando smette di essere sufficiente, il che, per le due fasi di comando che lo installano, è a 0.2.0: `facet-index` e `facet-mcp` restituiscono `0` ok / `1` errore utente / `2` errore di runtime e, come indicato in [E22](docs/experiments/E22-ruling.md), **`4` RIFIUTATO** per un filtro attivato o una fase `verify` non riuscita, il che significa che lo strumento funziona e ti avvisa di non procedere, piuttosto che generare un errore di runtime. Tutti questi elementi rifiutano con un errore strutturato che indica il passaggio successivo, anziché una traccia ([E21](docs/experiments/E21-cli-contract-report.md)).

**E i filtri in queste due fasi non sono più eliminabili.** Ogni elemento ANDON in ciò che installa `raise`; un semplice `assert` è un'istruzione che `python -O` rimuove silenziosamente e 87 dei filtri di questo repository potevano essere rimossi tramite una variabile d'ambiente fino a quando E22 non li ha convertiti. Misurato prima e dopo sullo stesso filtro, in quattro modalità interprete.
**E, come indicato in [E23](docs/experiments/E23-route-gates-report.md), nemmeno i filtri sul percorso che ha prodotto le quattro risorse accettate lo sono**: i suoi **57 siti in dodici strumenti** sono stati convertiti in una semplice operazione sui file che non è mai stata eseguita prima, e ora ognuno di essi rifiuta anche sotto `-O` e `PYTHONOPTIMIZE=1`, oltre che sotto un interprete normale.
**E, come indicato in [E25](docs/experiments/E25-ruling.md), la classe è chiusa.** I suoi **133 siti in 43 file**: gli strumenti di misurazione che hanno prodotto le prove per le quattro risorse accettate sopra, vengono convertiti nello stesso modo, portando il totale di `raise` a **278**.
Esattamente **un** elemento ANDON `assert` rimane in qualsiasi posizione sotto `tools/`: `superseded/texpass_thin_mask.py`, che **non viene mai** convertito, perché questi strumenti sono mantenuti in modo che chiunque possa eseguirli e osservare il loro fallimento nello stesso modo. Questo resto è fissato **per nome** nella suite di test, in modo che una scansione futura non possa eliminarlo senza modificare il test intenzionalmente.

**Stato del supporto:** questo repository viene sviluppato in modo aperto, su un'unica piattaforma, da un unico responsabile e da una coppia di sessioni di consulenza ed esecuzione a rotazione. `main` è l'unico stato supportato. Non esiste un canale di rilascio, una politica di backporting o un SLA: ciò che esiste è la registrazione: ogni affermazione è affiancata dal codice che la produce e [docs/experiments](docs/experiments/) contiene le specifiche, il rapporto e la decisione per ciascuna di esse.

## Requisiti

Blender 5.x, Python 3.11+ con `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. È necessaria un'installazione locale di ComfyUI solo per il pennello di inpainting. Sviluppato su un RTX 5090; la quantità di VRAM disponibile è più importante della velocità pura.

**Due interpreti e la divisione è intenzionale.** La suite, gli strumenti MCP serviti e ogni misurazione vengono eseguiti nell'ambiente che contiene i pin CI (3.12). La fase di ricostruzione viene eseguita in un secondo interprete fissato a **3.10**, perché le ruote TRELLIS di cui ha bisogno sono compilate per esso. Uno strumento che non riesce a importare di solito viene richiesto dall'altro.

CI esegue il sottoinsieme ermetico della suite su **ubuntu-latest / Python 3.12** con installazioni fissate (`.github/workflows/ci.yml`); la fase degli artefatti richiede gli alberi registrati in `E:\AI\training`, che non sono in git, quindi CI li esclude intenzionalmente. Localmente, `python -m pytest` esegue tutti i **1376** test e `python -m pytest -m "not artifacts"` esegue i **1319** test riprodotti da CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
