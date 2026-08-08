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

Lo stile viene applicato **direttamente sull’oggetto**, nello spazio della texture, e non viene disegnato separatamente per ogni prospettiva per poi essere assemblato successivamente. Si fornisce al programma un modello concettuale in argilla con forme accentuate e questo restituisce una mesh texturizzata il cui colore deriva da un riferimento stilizzato di *quella* stessa mesh; tutte le aree che il riferimento non copre vengono riempite tramite uno strumento di pittura mascherato e una dilatazione che tiene conto della superficie.

Prende il nome dalle due componenti del problema: i poligoni e la superficie che devono delimitare.

## Dove si trova

**Quattro opere sono state selezionate, appartenenti a quattro diverse categorie tematiche, e non richiedono alcun credito.** Ciascuna di esse è stata valutata dal Direttore, che ha utilizzato il formato più adatto – sia esso la versione ridotta (GLB) o il formato completo – e non si è basato su criteri quantitativi predefiniti.

| argomento; materia; soggetto | classe | accettato/a | riferimento / pennello / dilatazione |
|---|---|---|---|
| **Character (W3)** | umanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veicolo, attrezzatura leggera | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bestia, membrane alari | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | oggetto di scena, quasi bidimensionale, con tonalità di grigio su grigio | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Le porzioni di texture sono valide e **non possono essere confrontate tra diversi soggetti** – una nave nasconde la maggior parte della sua superficie all’altezza degli occhi e un animale ne nasconde metà. Confrontare ogni elemento con il proprio limite massimo predefinito, rispetto al quale si ottiene un risultato compreso tra l’**86% e il 93%**: la differenza tra le diverse porzioni è dovuta alla geometria, non a una regressione. [Valori completi, con i rispettivi denominatori](docs/handbook/subjects.md).

**Si tratta di una pipeline, non di un generatore che produce immagini con un solo personaggio.** Contraddicendo le specifiche su otto elementi identificati, il modello ottiene **8 risultati positivi su 8** – con una differenza media ΔE di 46,3 rispetto a 6,2 in cinque immagini di controllo – mentre l’immagine rimane la stessa. La struttura è mantenuta dalla griglia e dai controlli; gli attributi identificati sono influenzati dal prompt.

## Il percorso

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

Passaggio per passaggio, con la relativa spiegazione: **[il manuale](docs/handbook/index.md)**.

## Cosa lo rende efficace?

Sono stati ottenuti sei risultati, ciascuno dei quali è stato il frutto di un esperimento e che, nel complesso, hanno una portata più ampia rispetto all’ambito specifico in cui sono stati prodotti. [La versione completa, con le misurazioni](docs/findings.md).

- **Prima la forma, poi lo stile.** I programmi di ricostruzione interpretano il rumore superficiale come geometria. Un modello in argilla pulito, simile a una scultura, con piani volutamente esagerati, produce una topologia migliore rispetto a uno sprite stilizzato; la copia stilizzata viene generata contemporaneamente e diventa il riferimento cromatico.
- **Definisci i contorni del viso, ottieni un volto.** Un ritaglio che inquadra il busto aggiunge dal **3,1 al 4,5 volte più poligoni** alla testa e la differenza è strutturale: palpebre separate, una piega sul sopracciglio, cavità nasali modellate, non semplicemente una sfocatura più accentuata.
- **Le copie appartengono a una mesh, non a un personaggio.** Riutilizza una copia su diverse mesh e la copertura si riduce del **62% → 22,7%**, perché le braccia si proiettano nello spazio vuoto accanto al modello. Genera le copie dalla mesh che stai per texturizzare, ogni volta.
- **L'identità appartiene al prompt.** Un elemento canonico non menzionato nel prompt compare accidentalmente e scompare allo stesso modo: questo è misurato quando delle ginocchiere dorate sono apparse nell'immagine solo a causa del rumore in un ControlNet difettoso.
- **Chiedi alla geometria, non a una soglia.** Sostituire una maschera con il profilo esatto ottenuto tramite raycasting ha spostato la copertura di riferimento dal **28,4% al 39,1%** dei texel validi: in modo strettamente additivo, senza diffusione e senza l'utilizzo della GPU. Il metodo di keying basato sulla mediana degli angoli è fallito tre volte qui ed è stato abbandonato.
- **Elimina ciò che nessuna telecamera può vedere, dall'atlante e mai dalla mesh.** Il 49% dei texel dell'atlante non è visibile dall'esterno; escludendo queste facce, l'interpolazione si riduce del 68%. Escludere anziché eliminare rende il fallimento impossibile invece di semplicemente rilevabile.

## Cosa non è ancora stato risolto?

Elencati e descritti nella pagina principale, anziché in una nota a piè di pagina. [Tutti sono elencati nel codice](docs/known-defects.md).

- **La fascia della lama rappresenta lo 0,00% del riferimento nella fase 1** su tutte e otto le telecamere: l’acciaio su uno sfondo grigio si allinea perfettamente con la soglia dell’immagine di riferimento. L’unione recupera il 55,72%.
- **Le giunture delle pennellate non sono state livellate.** Un confine di provenienza presenta una variazione **5,5 volte** superiore rispetto alla normale tessitura; l’area indicata dal regista mostra una variazione **9,5 volte** superiore.
- **La dilatazione si estende tra isole dell’atlante non correlate:** il 74,9% dei texel dilatati assume il colore da un’altra isola, con una distanza mediana di 0,177 su una figura alta 1,0.
- **Ogni ricostruzione in questo percorso è un guscio vuoto a doppia parete**, con pareti di circa due voxel. Nessun predicato volumetrico è valido per uno di essi.

## Come funziona questo repository

La disciplina è tanto importante quanto il processo che la sostiene e ha una sua ragion d’essere: in un ciclo precedente, sono state svolte dieci sessioni durante le quali ogni partecipante ha valutato i propri risultati e redatto delle conclusioni che, nella sessione successiva, sono state considerate come fatti accertati. Nulla di tutto ciò poteva essere verificato.

- **Si definiscono le specifiche prima dell'esecuzione, si redige un rapporto al termine e si stabilisce la conclusione alla fine**; inoltre, la sessione in cui viene progettato un esperimento non valuta mai i propri risultati. Venti esperimenti sono disponibili [nei documenti](docs/experiments/).
- **Le correzioni vengono applicate direttamente, accanto alla misurazione che le ha confutate**, e non come semplici eliminazioni silenziose. Sei affermazioni ereditate sono state smentite nella sola sessione iniziale e tutte e sei sono ancora visibili accanto a ciò che le ha sostituite.
- **I risultati negativi rimangono nel repository insieme alla motivazione.** [`tools/superseded/`](docs/tools.md) non è un archivio: chiunque può eseguire questi strumenti e osservare il loro fallimento nello stesso modo.
- **Un risultato negativo è un successo completo**, viene segnalato e chiuso anziché essere modificato per raggiungere un determinato valore.
- **I test vengono eseguiti insieme alla modifica del codice**; 218 test hanno avuto esito positivo grazie al lavoro di due persone, con CI basata su percorsi per i 210 elementi più importanti.
- **È possibile effettuare ricerche nei dati.** È stato creato un indice SQLite + FTS5 sull'intero flusso di dati, verificato su quattro piattaforme. Questo ha permesso di individuare un errore nel conteggio dei risultati che era presente in tre sezioni del testo, contando direttamente i dati stessi.

## Dove si trova tutto

| | |
|---|---|
| **[Il manuale](docs/handbook/index.md)** | la guida: il percorso suddiviso per tappe, gli argomenti trattati, il sistema di classificazione. |
| **[I risultati](docs/experiments/)** | venti esperimenti: specifiche, relazione, valutazione e ogni previsione formulata prima della misurazione |
| **[Cosa ha appreso il percorso](docs/findings.md)** | le scoperte durature e le regole ottenute con fatica, nella loro interezza |
| **[Stato di ogni strumento](docs/tools.md)** | cosa funziona, cosa è obsoleto e le prove per ciascuno |
| **[Difetti noti](docs/known-defects.md)** | tutto ciò che non è stato risolto, misurato e localizzato nel codice |
| **[L'evoluzione, come è avvenuta](docs/arc-history.md)** | la cronologia degli eventi, con le correzioni intatte |
| **[CLAUDE.md](CLAUDE.md)** | come lavorare qui: i ruoli, le regole e il costo di ciascuno |

## Condizioni di licenza

Ogni fase viene eseguita in locale e nel rispetto delle normative commerciali: SDXL (OpenRAIL++), MV-Adapter (open), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Esclusioni deliberate, con la relativa motivazione: **nvdiffrast** (non commerciale – applicata qui tramite un meccanismo di sicurezza strutturale, non tramite attestazione), **Hunyuan3D-Paint** (licenza non valida nell'UE, nel Regno Unito e in Corea del Sud), **MVPaint** e **TEXGen** (nessuna licenza) e **UltraSharp / SUPIR / StableSR** (strumenti di upscaling non commerciali).

## Modello di fiducia e di minaccia

facet viene eseguito interamente sulla propria macchina: ogni strumento è uno script che si esegue su percorsi specificati dall'utente, quindi la domanda utile non è *quali autorizzazioni richiede questa app*, ma *cosa fanno questi script alla tua macchina*. La risposta è fornita dalla misurazione, con ogni ciclo ripetibile; la politica completa è disponibile in [SECURITY.md](SECURITY.md):

- **Dati interessati:** mesh, texture, immagini e file JSON su disco locale, nei percorsi specificati nella riga di comando. Inoltre `docs/index/facet.db`, che sono *derivati*: non contengono nulla che non fosse già un file in questo repository e `facet_index.py build` li rigenera da zero.
- **Dati NON interessati:** nessuna credenziale, mai. Nessuno strumento legge, memorizza o trasmette token, chiavi o password, e nessuno di questi elementi è presente nell'albero: sono stati eseguiti controlli per verificare la presenza di chiavi con prefissi relativi al fornitore, GitHub PAT, token Slack, ID chiave AWS, blocchi di chiavi private, token bearer e assegnazioni inline `api_key`/`password`; **nessuna corrispondenza**, nessun file che assomigli a una credenziale è stato rilevato.
- **Nessun telemetria.** Nessuna raccolta o trasmissione di dati. Non esiste un'opzione per disattivare la raccolta dei dati perché non c'è nulla da cui disattivarsi.
- **Traffico di rete:** due degli strumenti su trentaquattro aprono una connessione socket: `restylize_views.py` e `texpass_brush.py`, ed entrambi chiamano l'API HTTP di ComfyUI all'indirizzo `--host`, con impostazione predefinita `127.0.0.1:8188`. Nessun altro strumento in `tools/` effettua chiamate di rete.
- **Autorizzazioni:** utente standard. Nessuna elevazione dei privilegi, nessuna installazione di servizi, nessuna scrittura nelle impostazioni di sistema o nel registro di sistema.

Tre aspetti critici vengono esplicitamente indicati anziché nascosti, perché una nota sulla sicurezza che elenca solo rassicurazioni non è un modello di minaccia: **le operazioni sui file non sono eseguite in un ambiente isolato** (uno strumento scrive ovunque indichino i suoi argomenti); **i percorsi locali assoluti sono incorporati in molti strumenti e documenti**: 114 occorrenze in 26 file, non si tratta di segreti, ma della divulgazione del layout di una macchina, ed è il motivo per cui la maggior parte degli strumenti non funzionerà senza modifiche altrove; e **i guasti imprevisti vengono visualizzati come tracce di errore di Python**, senza un filtro `--debug` e senza una struttura di errore definita. Le interruzioni deliberate sono messaggi `ANDON:` che contengono la misurazione che le ha attivate. Questo è il contratto dello strumento di ricerca, e [SHIP_GATE.md](SHIP_GATE.md) registra esattamente quando smette di essere sufficiente.

**Stato del supporto:** questo repository viene sviluppato in modo aperto, su un'unica piattaforma, da un unico responsabile e con una coppia rotante di sessioni di consulenza ed esecuzione. `main` è l'unico stato supportato. Non esiste un canale di rilascio, una politica di backporting o un SLA: ciò che esiste è la registrazione: ogni affermazione si trova accanto al codice che la produce e [docs/experiments](docs/experiments/) contiene le specifiche, la relazione e la valutazione per ciascuna di esse.

## Requisiti

Blender 5.x, Python 3.11+ con `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. È necessaria un'installazione locale di ComfyUI solo per il pennello di inpainting. Sviluppato su una RTX 5090; la quantità di VRAM disponibile è più importante della velocità pura.

Il CI esegue il sottoinsieme ermetico della suite su **ubuntu-latest / Python 3.12** con installazioni fisse (`.github/workflows/ci.yml`); lo strato degli artefatti richiede gli alberi registrati in `E:\AI\training`, che non sono presenti in git, quindi il CI li esclude intenzionalmente. Localmente, `python -m pytest` esegue tutti i **218** test e `python -m pytest -m "not artifacts"` esegue i **210** test riprodotti dal CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
