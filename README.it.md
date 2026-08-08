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

Lo stile viene applicato **sull'asset**, nello spazio della texture, e non dipinto per ogni vista e poi assemblato successivamente. Fornisci alla pipeline un modello di argilla con forme esagerate e questa restituirà una mesh texturizzata il cui colore deriva da un riferimento stilizzato di *quella* mesh, con tutto ciò che il riferimento non poteva vedere riempito tramite uno strumento di ritocco mascherato e una dilatazione consapevole della superficie.

Prende il nome dalle due metà del problema: i poligoni e la superficie che devono rappresentare.

## Installazione

La pipeline stessa è un insieme di script locali che vengono eseguiti su percorsi specificati dall'utente: clona il repository e leggi [la guida introduttiva](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**L'indice dei record viene fornito come pacchetto**, in modo che un assistente possa interrogare la traccia delle prove invece di leggerla:

```bash
npx @mcptoolshop/facet          # zero-prerequisite; verified binary, no Python needed
pipx install facet-mcp          # or the Python package directly
```

Sono inclusi due comandi: `facet-mcp`, il server MCP stdio (sei strumenti, con la verifica a quattro punti come superficie di controllo), e `facet-index` (`build` / `verify` / `q` / `claims`). Punta uno qualsiasi su un indice utilizzando `--db` o `$FACET_INDEX_DB`.

## Situazione attuale

**Quattro asset accettati, appartenenti a quattro classi di soggetti, senza costi aggiuntivi.** Ognuno è stato valutato dal Direttore con il proprio livello di zoom: sul file GLB o su fogli a grandezza naturale, e non in base a una metrica che supera una soglia.

| soggetto | classe | accettato | riferimento / pennello / dilatazione |
|---|---|---|---|
| **Character (W3)** | umanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veicolo, struttura leggera | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bestia, membrane alari | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | oggetto di scena, quasi bidimensionale, grigio su grigio | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Le condivisioni si basano su texel validi e **non sono confrontabili tra i diversi soggetti**: una nave nasconde gran parte di sé dalla prospettiva a livello degli occhi e un animale ne nasconde metà. Valuta ciascuno rispetto al proprio limite di copertura pre-registrato, rispetto al quale raggiungono l'**86–93%**: la differenza tra le righe è la geometria, non una regressione. [Numeri completi, con i rispettivi denominatori](docs/handbook/subjects.md).

**È una pipeline, non un generatore di un singolo elemento.** Contraddici le specifiche su otto elementi specifici e l'output rispetterà la richiesta in **8 casi su 8**: la deviazione mediana ΔE è di 46,3 rispetto a 6,2 su cinque controlli mantenuti; la figura rimane comunque la stessa. La struttura è garantita dalla mesh e dal controllo; gli attributi specificati influenzano l'output.

## La pipeline

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

Fase per fase, con le motivazioni per ciascuna: **[la guida](docs/handbook/index.md)**.

## Cosa la rende efficace

Sei risultati, ognuno dei quali ha richiesto un esperimento e ognuno dei quali si generalizza oltre il soggetto che lo ha prodotto. [La versione estesa, con le misurazioni](docs/findings.md).

- **Prima la forma, poi lo stile.** Gli strumenti di ricostruzione interpretano il rumore superficiale come geometria. Un modello di argilla pulito e simile a una scultura, con piani deliberatamente esagerati, produce una topologia migliore rispetto a uno sprite stilizzato; l'elemento stilizzato viene generato contemporaneamente e diventa il riferimento cromatico.
- **Definisci la superficie del volto per ottenere un volto.** Un ritaglio che inquadra il busto aggiunge **da 3,1 a 4,5 volte più poligoni alla testa**, e la differenza è strutturale: palpebre separate, una piega sul sopracciglio, cavità delle narici modellate, e non semplicemente una sfocatura più nitida.
- **Le copie appartengono a una mesh, non a un personaggio.** Riutilizza una copia su diverse mesh e la copertura diminuisce del **62% → 22,7%**, perché le braccia si proiettano nello spazio vuoto accanto al modello. Genera sempre le copie dalla mesh che stai per texturizzare.
- **L'identità appartiene alla richiesta.** Un elemento canonico non specificato nella richiesta viene aggiunto accidentalmente e scomparirà allo stesso modo: questo è stato misurato quando si è scoperto che le placche dorate sulle ginocchia apparivano nell'immagine solo a causa del rumore in un ControlNet difettoso.
- **Chiedi informazioni sulla geometria, non su una soglia.** La sostituzione di una maschera chiave con l'esatta silhouette ottenuta tramite raycast ha aumentato la copertura del riferimento dal **28,4% al 39,1%** dei texel validi: questo avviene in modo strettamente additivo, senza diffusione e senza utilizzo della GPU. Il keying basato sugli angoli è fallito tre volte in questa fase ed è stato abbandonato.
- **Elimina ciò che nessuna telecamera può vedere, dall'atlante e non dalla mesh.** Il 49% dei texel dell'atlante sono invisibili dall'esterno; l'esclusione di queste facce riduce l'interpolazione del 68%. L'esclusione anziché l'eliminazione rende il fallimento impossibile invece che semplicemente rilevabile.

## Cosa non è ancora stato risolto

Specificato e misurato, nella pagina iniziale piuttosto che in una nota a piè di pagina. [Tutti gli elementi, presenti nel codice](docs/known-defects.md).

- **La fascia della lama occupa lo 0,00% del riferimento nella fase 1** su tutte e otto le telecamere: l'acciaio su uno sfondo grigio si trova esattamente sulla soglia del keying. L'unione salva il 55,72%.
- **Le giunture delle texture non sono uniformi.** Un confine di provenienza presenta una variazione della texture pari a **5,5 volte** rispetto alla normale; la regione specificata dal Direttore presenta una variazione pari a **9,5 volte**.
- **La dilatazione si estende tra le isole dell'atlante non correlate:** il 74,9% dei texel dilatati prendono il loro colore da un'altra isola, con una distanza mediana di 0,177 su una figura alta 1,0.
- **Ogni ricostruzione in questa pipeline è un guscio cavo a doppia parete**, con pareti di circa due voxel. Nessun predicato volumetrico è valido su uno di essi.

## Come viene eseguito questo repository

La disciplina è tanto importante quanto la pipeline stessa, ed esiste per un motivo: una fase precedente ha previsto dieci sessioni in cui ogni output veniva valutato e le conclusioni venivano scritte per essere lette nella sessione successiva come fatti consolidati. Nulla in quel ciclo era verificabile.

- **Definizione prima del lavoro, relazione dopo, decisione finale:** e la sessione che progetta un esperimento non valuta mai i propri risultati. Venti esperimenti sono disponibili in [questa sezione](docs/experiments/).
- **Le correzioni vengono applicate immediatamente, accanto alla misurazione che le ha invalidate**, e non come semplici eliminazioni silenziose. Solo nella sessione iniziale, sei affermazioni preesistenti sono state confutate, e tutte e sei sono ancora visibili accanto a ciò che le ha sostituite.
- **I fallimenti rimangono nel repository insieme alla loro motivazione.** [`tools/superseded/`](docs/tools.md) non è un archivio: chiunque può eseguire questi strumenti e osservare i loro fallimenti nello stesso modo.
- **Un risultato negativo è un successo completo**, viene segnalato e chiuso, anziché essere modificato per raggiungere un valore specifico.
- **I test vengono eseguiti insieme al commit che modifica il codice:** 218 superati con due persone che li eseguono, con CI basata sui percorsi per i 210 elementi "ermetici".
- **La cronologia è consultabile.** Un indice SQLite + FTS5 sull'intera sequenza, verificato su quattro sistemi. Ha individuato un conteggio di decisioni che il testo presentava in modo errato in tre punti, contando direttamente la cronologia stessa.

## Dove tutto è..

| | |
|---|---|
| **[Il manuale](docs/handbook/index.md)** | la guida: le fasi, gli argomenti e il sistema di profili. |
| **[La cronologia](docs/experiments/)** | venti esperimenti: definizione, relazione, decisione e ogni previsione formulata prima della misurazione. |
| **[Cosa ha imparato il percorso](docs/findings.md)** | le scoperte durature e le regole ottenute con fatica, nella loro interezza. |
| **[Stato di ogni strumento](docs/tools.md)** | cosa funziona, cosa è stato sostituito e le prove per ciascuno. |
| **[Difetti noti](docs/known-defects.md)** | tutto ciò che non è stato risolto, misurato e localizzato nel codice. |
| **[L'evoluzione, come è avvenuta](docs/arc-history.md)** | la cronologia, con le correzioni intatte. |
| **[CLAUDE.md](CLAUDE.md)** | come lavorare qui: i ruoli, le regole e il costo di ciascuno. |

## Condizioni di licenza

Ogni fase viene eseguita localmente e in modo conforme alle normative commerciali: SDXL (OpenRAIL++), MV-Adapter (open), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Esclusioni deliberate, con la relativa motivazione: **nvdiffrast** (non commerciale, applicata qui tramite un meccanismo di sicurezza strutturale, non tramite attestazione), **Hunyuan3D-Paint** (licenza non valida nell'UE, nel Regno Unito e in Corea del Sud), **MVPaint** e **TEXGen** (nessuna licenza) e **UltraSharp / SUPIR / StableSR** (upscaler non commerciali).

## Modello di fiducia e minacce

facet viene eseguito interamente sulla propria macchina: ogni strumento è uno script che si esegue sui percorsi digitati, quindi la domanda utile non è *quali autorizzazioni richiede questa applicazione*, ma *cosa fanno questi script alla tua macchina*. La risposta viene fornita tramite misurazione, con ogni ciclo ripetibile; la politica completa è disponibile in [SECURITY.md](SECURITY.md):

- **Dati interessati:** mesh, texture, immagini e JSON su disco locale, nei percorsi specificati nella riga di comando. Inoltre `docs/index/facet.db`, che sono *derivati*: non contengono nulla che non fosse già un file in questo repository, e `facet_index.py build` li rigenera da zero.
- **Dati NON interessati:** nessuna credenziale, mai. Nessuno strumento legge, memorizza o trasmette token, chiavi o password, e nessuno di questi elementi è presente nell'albero: sono stati eseguiti controlli per individuare chiavi con prefisso del provider, GitHub PAT, token Slack, ID chiave AWS, blocchi di chiavi private, token bearer e assegnazioni inline `api_key`/`password`; **zero corrispondenze**, nessun file che assomigli a una credenziale è stato rilevato.
- **Nessun telemetria.** Nessuna raccolta o trasmissione di dati. Non c'è alcuna opzione per disattivare la telemetria perché non c'è nulla da disattivare.
- **Traffico di rete:** due degli strumenti, su un totale di trentaquattro, aprono una connessione socket: `restylize_views.py` e `texpass_brush.py`, entrambi chiamano l'API HTTP di ComfyUI all'indirizzo `--host`, con valore predefinito `127.0.0.1:8188`. Nessun altro strumento in `tools/` effettua chiamate di rete.
- **Autorizzazioni:** utente standard. Nessuna elevazione dei privilegi, nessuna installazione di servizi, nessuna scrittura nelle impostazioni di sistema o nel registro di sistema.

Tre aspetti critici vengono evidenziati anziché nascosti, perché una nota sulla sicurezza che elenca solo rassicurazioni non è un modello di minacce: **le operazioni sui file non sono eseguite in un ambiente isolato** (uno strumento scrive ovunque gli indichino i suoi argomenti); **molti strumenti e documenti contengono percorsi locali assoluti**, 114 occorrenze in 26 file, non si tratta di segreti ma della divulgazione del layout di una macchina, ed è il motivo per cui la maggior parte degli strumenti non funzionerà senza modifiche su un altro sistema; e **i fallimenti imprevisti vengono visualizzati come tracce di errore di Python**, senza alcun filtro `--debug` e senza una struttura di errore definita. Le interruzioni deliberate sono messaggi `ANDON:` che contengono la misurazione che le ha attivate. Questo è il contratto dello strumento di ricerca, e [SHIP_GATE.md](SHIP_GATE.md) registra esattamente quando smette di essere sufficiente.

**Stato del supporto:** questo repository viene sviluppato in modo aperto, su un unico sistema, da un singolo responsabile e da una coppia di sessioni di consulenza ed esecuzione a rotazione. `main` è l'unico stato supportato. Non esiste un canale di rilascio, una politica di backporting o un SLA: ciò che esiste è la cronologia: ogni affermazione si trova accanto al codice che la produce, e [docs/experiments](docs/experiments/) contiene le specifiche, la relazione e la decisione per ciascuna di esse.

## Requisiti

Blender 5.x, Python 3.11+ con `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. È necessaria un'installazione locale di ComfyUI solo per il pennello di inpainting. Sviluppato su un RTX 5090; la quantità di VRAM disponibile è più importante della velocità pura.

Il CI esegue il sottoinsieme "ermetico" della suite su **ubuntu-latest / Python 3.12** con installazioni fisse (`.github/workflows/ci.yml`); lo strato degli artefatti richiede gli alberi registrati in `E:\AI\training`, che non sono presenti in git, quindi il CI li esclude intenzionalmente. Localmente, `python -m pytest` esegue tutti i **218** test e `python -m pytest -m "not artifacts"` esegue i **210** test riprodotti dal CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
