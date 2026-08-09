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
  Local hardware end to end · no non-commercial licence anywhere in the chain
</p>

---

Lo stile viene applicato **sull'asset**, nello spazio delle texture, e non disegnato per ogni singola visualizzazione per poi essere assemblato successivamente. Fornendo alla pipeline un modello di argilla con forme esagerate, si ottiene una mesh texturizzata il cui colore deriva da un riferimento stilizzato di *quella* stessa mesh, con tutte le aree che il riferimento non poteva vedere riempite tramite uno strumento di "inpainting" mascherato e una dilatazione consapevole della superficie.

Prende il nome dalle due componenti del problema: i poligoni e la superficie che devono rappresentare.

## Installazione

La pipeline stessa è un insieme di script locali che vengono eseguiti su percorsi specificati dall'utente; clona il repository e leggi [la guida introduttiva](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**L'indice dei record viene fornito come pacchetto**, in modo che un assistente possa interrogare la traccia delle evidenze invece di leggerla:

```bash
npx @mcptoolshop/facet          # zero-prerequisite; verified binary, no Python needed
```

Sono inclusi due comandi: `facet-mcp`, il server MCP stdio (sei strumenti, con la verifica a quattro punti come superficie di controllo), e `facet-index` (`build` / `verify` / `q` / `claims`). Esegui questi comandi all'interno di una copia del progetto; `--db` indica un indice diverso.

⚠ **`pip install facet-mcp` era difettoso in tutte le versioni rilasciate fino alla v0.3.0, ed è stato corretto nella v0.3.1.** Il pacchetto installa `facet_index` come modulo di primo livello; quindi, fino alla versione v0.3.0 inclusa, individuava la posizione del record rispetto a `<venv>/Lib` (che non contiene né il corpus né l'indice) e a `build`, `claims` e `q`, ma tutti questi tentativi fallivano se `--db` non era presente.
**Nelle versioni v0.3.0 o precedenti, utilizza il binario `npx` indicato sopra.**

A partire dalla v0.3.1, la radice viene risolta **verificando l'esistenza del record** anziché presupponendola: esegui uno qualsiasi dei due comandi all'interno di una copia del progetto e il sistema lo troverà; eseguilo da qualsiasi altra posizione e il programma terminerà con il messaggio "**`4` RIFIUTATO**", indicando sia le directory che ha tentato di utilizzare, sia i marcatori che ha cercato.
`$FACET_INDEX_DB` viene ora letto da entrambi i comandi e seleziona quale *indice* utilizzare, ma non quale *corpus*. I risultati sono stati misurati su un pacchetto creato da `main` e installato in un ambiente virtuale pulito: [E24](docs/experiments/E24-ruling.md).

*Questo blocco è stato corretto due volte. Inizialmente conteneva il testo `pipx install facet-mcp # oppure il pacchetto Python direttamente`, until v0.3.0's read-back ran a **verb** instead of `--help`.
Successivamente, affermava che il pacchetto "funziona solo per `q` e `claims`" - **ma anche `claims` non funzionava**, come dimostrato da E24 eseguendolo. Entrambe le correzioni sono presenti in [known-defects.md](docs/known-defects.md) con i relativi risultati.*

## Stato attuale

**Quattro asset accettati, appartenenti a quattro classi di soggetti diversi, senza costi aggiuntivi.** Ognuno è stato valutato dal direttore utilizzando il proprio livello di zoom, sia sul modello GLB che su fogli di dimensioni reali, e non tramite una metrica che supera una soglia.

| soggetto | classe | accettato | riferimento / pennello / dilatazione |
|---|---|---|---|
| **Character (W3)** | umanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veicolo, con struttura sottile | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | animale, membrane alari | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | oggetto di scena, quasi bidimensionale, grigio su grigio | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Le condivisioni si riferiscono a texel validi e **non sono comparabili tra soggetti diversi**: una nave nasconde gran parte di sé dalla prospettiva dell'osservatore, mentre un animale ne nasconde metà. Valuta ogni soggetto rispetto al proprio limite di copertura pre-registrato; in questo modo, i risultati rientrano nell'intervallo **86–93%**: la differenza tra le righe è dovuta alla geometria, non a una regressione. [Numeri completi con i relativi denominatori](docs/handbook/subjects.md).

**Si tratta di una pipeline, non di un generatore che produce un singolo elemento.** Se si contraddice la specifica su otto elementi specifici, il risultato sarà positivo in **8 casi su 8**: la deviazione mediana ΔE è pari a 46,3 rispetto a 6,2 sui cinque controlli mantenuti; tuttavia, l'aspetto generale rimane lo stesso. La struttura è garantita dalla mesh e dal controllo; gli attributi specifici vengono applicati tramite il prompt.

## La pipeline

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

Fase per fase, con la motivazione di ciascuna: **[la guida](docs/handbook/index.md)**.

## Cosa rende possibile il funzionamento

Sei risultati, ognuno dei quali ha richiesto un esperimento e ognuno dei quali si generalizza oltre il soggetto che lo ha prodotto. [La versione completa con i risultati](docs/findings.md).

- **Prima la forma, poi lo stile.** Gli strumenti di ricostruzione interpretano il rumore superficiale come geometria. Un modello di argilla pulito e simile a una scultura, con piani deliberatamente esagerati, produce una topologia migliore rispetto a uno sprite stilizzato; l'elemento stilizzato viene generato contemporaneamente e diventa il riferimento cromatico.
- **Definisci la forma del viso per ottenere un viso.** Un ritaglio che inquadra il busto aggiunge **da 3,1 a 4,5 volte più poligoni alla testa**, e la differenza è strutturale: palpebre separate, una fossetta sul sopracciglio, cavità delle narici modellate; non si tratta semplicemente di una sfocatura meno marcata.
- **Le copie appartengono a una mesh, non a un personaggio.** Se utilizzi una copia su più mesh, la copertura diminuisce del **62% → 22,7%**, perché le braccia si proiettano nello spazio vuoto accanto al modello. Genera sempre le copie dalla mesh che stai per texturizzare.
- **L'identità appartiene al prompt.** Un elemento canonico non menzionato nel prompt viene aggiunto accidentalmente e scomparirà allo stesso modo: questo è stato misurato quando si è scoperto che le ginocchiere dorate apparivano nell'immagine solo a causa del rumore in un ControlNet difettoso.
- **Chiedi informazioni sulla geometria, non su una soglia.** La sostituzione di una maschera chiave con l'esatta silhouette ottenuta tramite raycast ha aumentato la copertura del riferimento dal **28,4% al 39,1%** dei texel validi: questo è un aumento netto, senza diffusione né utilizzo della GPU. Il keying basato sugli angoli ha fallito tre volte in questa fase ed è stato abbandonato.
- **Elimina ciò che nessuna telecamera può vedere, dall'atlante e non dalla mesh.** Il 49% dei texel dell'atlante sono invisibili se osservati dall'esterno; l'esclusione di queste facce riduce l'interpolazione del 68%. L'esclusione anziché l'eliminazione rende il fallimento impossibile, invece che semplicemente rilevabile.

## Cosa non è ancora stato risolto

Identificato e misurato, nella pagina principale anziché in una nota a piè di pagina. [Tutti gli elementi sono elencati nel codice](docs/known-defects.md).

- **La fascia del disco utilizza lo 0,00% del riferimento della fase 1** su tutte e otto le telecamere: l'acciaio su uno sfondo grigio si posiziona esattamente sulla soglia chiave. L'unione salva il 55,72%.
- **Le giunture delle strisce non sono livellate.** Un confine di provenienza presenta una variazione della trama **5,5 volte** maggiore rispetto alla normale; la regione nominata dal direttore presenta una variazione **9,5 volte** maggiore.
- **La dilatazione si estende tra isole dell'atlante non correlate:** il 74,9% dei texel dilatati prendono il loro colore da un'altra isola, con una distanza mediana di 0,177 su una figura alta 1,0.
- **Ogni ricostruzione in questo percorso è un guscio cavo a doppia parete**, con pareti di circa due voxel. Nessun predicato volumetrico è valido su uno di essi.

## Come viene eseguito questo repository

La disciplina è tanto importante quanto la pipeline, ed esiste per un motivo: in una fase precedente sono state eseguite dieci sessioni, ciascuna delle quali ha valutato il proprio output e ha scritto conclusioni che nella sessione successiva sono state considerate fatti consolidati. Nulla in quel ciclo era verificabile.

- **Definizione prima del lavoro, relazione dopo, decisione finale:** e la sessione che progetta un esperimento non valuta mai i propri risultati. Ventitré esperimenti sono disponibili in [questa sezione](docs/experiments/).
- **Le correzioni vengono inserite al loro posto, accanto alla misurazione che le ha confutate**, e non come semplici eliminazioni. Sei affermazioni ereditate sono state falsificate nella sessione iniziale, e tutte e sei sono ancora leggibili accanto a ciò che le ha sostituite.
- **I fallimenti rimangono nel repository insieme al loro motivo.** [`tools/superseded/`](docs/tools.md) non è un archivio: chiunque può eseguire questi strumenti e osservare il loro fallimento nello stesso modo.
- **Un risultato negativo è un successo completo**, segnalato e chiuso, anziché modificato per raggiungere un valore specifico.
- **I test sono associati al commit che modifica il codice:** 684 superati da due persone, con CI basata sui percorsi per i 675 elementi ermetici.
- **La sezione è consultabile.** Un indice SQLite + FTS5 sull'intero percorso, verificato su quattro punti. Ha individuato un numero di decisioni che il testo aveva indicato in modo errato in tre siti, contando la stessa sezione.

## Dove si trova tutto

| | |
|---|---|
| **[Il manuale](docs/handbook/index.md)** | la guida: il percorso fase per fase, i soggetti, il sistema di profilazione |
| **[La sezione](docs/experiments/)** | ventitré esperimenti: definizione, relazione, decisione e ogni previsione indicata prima della misurazione |
| **[Cosa ha imparato il percorso](docs/findings.md)** | le scoperte durature e le regole ottenute con fatica, nella loro interezza |
| **[Stato di ogni strumento](docs/tools.md)** | cosa funziona, cosa è obsoleto e le prove per ciascuno |
| **[Difetti noti](docs/known-defects.md)** | tutto ciò che non è stato risolto, misurato e localizzato nel codice |
| **[Il percorso, come si è svolto](docs/arc-history.md)** | la cronologia, con le correzioni intatte |
| **[CLAUDE.md](CLAUDE.md)** | come lavorare qui: i ruoli, le regole e il costo di ciascuno |

## Posizione della licenza

Ogni fase viene eseguita localmente ed è conforme alle normative commerciali: SDXL (OpenRAIL++), MV-Adapter (open), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Escluso intenzionalmente, con la relativa motivazione: **nvdiffrast** (non commerciale: applicato qui tramite un meccanismo di sicurezza strutturale, non tramite attestazione), **Hunyuan3D-Paint** (licenza non valida nell'UE, nel Regno Unito e in Corea del Sud), **MVPaint** e **TEXGen** (nessuna licenza) e **UltraSharp / SUPIR / StableSR** (upscaler non commerciali).

## Modello di fiducia e minaccia

facet viene eseguito interamente sulla propria macchina: ogni strumento è uno script che si esegue sui percorsi digitati, quindi la domanda utile non è *quali autorizzazioni richiede questa app*, ma *cosa fanno questi script alla tua macchina*. La risposta è fornita dalla misurazione, con ogni ciclo ripetibile; la politica completa è disponibile in [SECURITY.md](SECURITY.md):

- **Dati interessati:** mesh, texture, immagini e JSON su disco locale, nei percorsi specificati nella riga di comando. Inoltre `docs/index/facet.db`, che è *derivato*: non contiene nulla che non fosse già un file in questo repository, e `facet_index.py build` lo rigenera da zero.
- **Dati NON interessati:** nessuna credenziale, mai. Nulla qui legge, memorizza o trasmette token, chiavi o password, e nessuno di essi è presente nell'albero: sono stati eseguiti controlli per individuare chiavi con prefisso del provider, GitHub PAT, token Slack, ID chiave AWS, blocchi di chiavi private, token bearer e assegnazioni inline `api_key`/`password`; **zero corrispondenze**, nessun file simile a una credenziale tracciato.
- **Nessun telemetria.** Nessuna raccolta, nessuna trasmissione. Non esiste un'opzione per disattivare perché non c'è nulla da disattivare.
- **Traffico di rete:** due degli strumenti su trentaquattro aprono un socket: `restylize_views.py` e `texpass_brush.py`, ed entrambi chiamano l'API HTTP di ComfyUI all'indirizzo `--host`, con valore predefinito `127.0.0.1:8188`. Nient'altro in `tools/` effettua una chiamata di rete.
- **Autorizzazioni:** utente normale. Nessun aumento dei privilegi, nessuna installazione del servizio, nessuna scrittura nelle impostazioni di sistema o nel registro di sistema.

Tre spigoli vivi vengono evidenziati piuttosto che negati, perché una nota di sicurezza che elenca solo delle rassicurazioni non è un modello di minaccia: **le operazioni sui file non sono eseguite in un ambiente isolato** (uno strumento scrive ovunque indichino i suoi argomenti); **i percorsi locali assoluti sono incorporati in molti strumenti e documenti** — 114 occorrenze in 26 file, non si tratta di segreti ma della divulgazione del layout di una macchina e del motivo per cui la maggior parte degli strumenti non funzionerà senza modifiche altrove; e **i fallimenti imprevisti emergono come tracce di Python nei 34 script di ricerca non pubblicati**, senza alcun filtro `--debug`. Le interruzioni deliberate sono messaggi `ANDON:` che contengono la misurazione che le ha attivate. Questo è il contratto dello strumento di ricerca e [SHIP_GATE.md](SHIP_GATE.md) registra esattamente quando smette di essere sufficiente, cosa che è successa per i due comandi in questione al punto 0.2.0: `facet-index` e `facet-mcp` restituiscono `0` ok / `1` errore utente / `2` errore di runtime — e, come indicato in [E22](docs/experiments/E22-ruling.md), **`4` RIFIUTATO** per un filtro attivato o una sezione `verify` che non funziona correttamente, il che significa che lo strumento sta funzionando e ti avvisa di non procedere invece di generare un errore di runtime. Tutti rifiutano con un messaggio di errore strutturato che indica il passaggio successivo anziché una traccia ([E21](docs/experiments/E21-cli-contract-report.md)).

**Inoltre, i filtri in questi due comandi non sono più eliminabili.** Ogni ANDON installa `raise`; un semplice `assert` è un'istruzione che `python -O` rimuove silenziosamente e 87 dei filtri di questo repository potevano essere rimossi tramite una variabile d'ambiente fino a quando E22 non li ha modificati. Misurati prima e dopo sullo stesso filtro, in quattro modalità interprete.
**E poiché [E23](docs/experiments/E23-route-gates-report.md), nemmeno i filtri sul percorso che ha prodotto le quattro risorse accettate sono eliminabili** — i suoi **57 siti su dodici strumenti**, convertiti come una semplice operazione sui file che non è mai stata eseguita da alcun test, ora rifiutano tutti sotto `-O` e `PYTHONOPTIMIZE=1`, nonché in un interprete normale.
**134 filtri nei restanti strumenti di ricerca sono ancora affermazioni** — elencati qui anziché omessi, definiti da [E22 Ruling 4](docs/experiments/E22-ruling.md) e nessuno di essi è presente in una sezione che installa: 132 sono strumenti di misurazione sotto `diagnostics/`, uno è un controllo di rendering e quello di `superseded/` non viene mai convertito, perché questi strumenti vengono mantenuti in modo che chiunque possa eseguirli e osservare il loro fallimento nello stesso modo.

**Stato del supporto:** questo repository è sviluppato in modalità open source, su un'unica piattaforma, da un unico responsabile e con una coppia di consulenti ed esecutori a rotazione. `main` è l'unico stato supportato. Non esiste un canale di rilascio, una politica di backporting o un SLA; ciò che esiste invece è la documentazione: ogni affermazione si trova accanto al codice che la produce e [docs/experiments](docs/experiments/) contiene le specifiche, il rapporto e la decisione per ciascuna di esse.

## Requisiti

Blender 5.x, Python 3.11+ con `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. È necessaria un'installazione locale di ComfyUI solo per il pennello di inpainting. Sviluppato su una RTX 5090; la quantità di VRAM disponibile è più importante della velocità pura.

Il CI esegue il sottoinsieme ermetico della suite su **ubuntu-latest / Python 3.12** con installazioni fisse (`.github/workflows/ci.yml`); lo strato degli artefatti richiede gli alberi registrati in `E:\AI\training`, che non sono presenti in git, quindi il CI li esclude intenzionalmente. Localmente, `python -m pytest` esegue tutti i **684** test e `python -m pytest -m "not artifacts"` esegue i **675** test riprodotti dal CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
