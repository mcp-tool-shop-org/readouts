<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.md">English</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/readouts/readme.png" alt="readouts" width="400" />
</p>

<h1 align="center">readouts</h1>

<p align="center">
  Verified, source-backed SQLite knowledge bases that an agent reads one slice at a time.
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/readouts/actions/workflows/verify.yml"><img src="https://github.com/mcp-tool-shop-org/readouts/actions/workflows/verify.yml/badge.svg" alt="verify" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License" /></a>
  <a href="https://mcp-tool-shop-org.github.io/readouts/"><img src="https://img.shields.io/badge/Landing_Page-live-34d399" alt="Landing Page" /></a>
</p>

---

readouts è un insieme di basi di conoscenza sugli strumenti utilizzati da un piccolo studio di sviluppo di videogiochi: Rust, Godot, Blender, tecniche di creazione di sprite e animazioni, modelli di intelligenza artificiale locali e i motori che li eseguono e li addestrano, la voce cantata, i container GPU e il registro XRP.

Ogni base di conoscenza (KB) è un database SQLite con un indice di testo completo. Ogni voce indica le sue fonti, registra la fase di ricerca che l'ha prodotta e contiene un flag `verified`. Solo il verdetto di un verificatore separato può impostare tale flag; l'opinione dell'autore sul proprio lavoro non viene mai presa in considerazione.

Il nome deriva da [loadout-os](https://github.com/mcp-tool-shop-org/loadout-os), che *carica* le conoscenze corrette per un determinato compito. readouts è ciò che legge.

## Le basi di conoscenza

| KB | Cos'è | Stato |
|----|------|--------|
| [blender-knowledge](blender-knowledge/) | Attuale, pratica di Blender 4.x basata sul web per la pipeline di rendering di sprite senza interfaccia utente dello studio (importa un file GLB generato da TRELLIS → esegue il rendering di sprite in 8 direzioni tramite blender --background --python → li compone in un gioco 2.5D) più preparazione generale delle risorse di gioco. | **219 ricette · 10 domini · 8 fasi · 83/219 verificate** |
| [docker-knowledge](docker-knowledge/) | La base di conoscenza alla base del prodotto gpu-container: come impacchettare, misurare e posizionare i modelli in modo corretto su una singola GPU. | **160 risultati · 6 domini · 9 fasi · 73/160 verificate** |
| [godot-knowledge](godot-knowledge/) | Attuale, conoscenza di Godot 4 verificata in modo avversario per la creazione di un RPG tattico a turni 2.5D. | **177 ricette · 6 domini · 7 fasi · 50/177 verificate** |
| [model-knowledge](model-knowledge/) | Base di conoscenza verificata dei migliori MODELLI di intelligenza artificiale generativa locali per scopo (immagine / modifica / controllo / video / 3D / audio / LLM / didascalia) per il sistema RTX 5090, con licenza commerciale prioritaria. | **129 modelli · 9 domini · 19 fasi · 126/129 verificate** |
| [rust-knowledge](rust-knowledge/) | Rust verificato per la creazione di si-rpg-engine (elementi essenziali, avanzati e come il motore lo utilizza: ABI wasm grezza, determinismo dei float, stato e ripristino di Rapier 0.35, byte riproducibili) e un primo livello per la musica di si-jam-sessions, con ogni controllo del codice eseguito da rustc 1.98.1. | **267 ricette · 27 domini · 4 fasi · 266/267 verificate** |
| [sprite-motion-knowledge](sprite-motion-knowledge/) | La tecnica portatile per animare gli sprite per questo sistema | **246 ricette · 19 domini · 8 fasi · 170/246 verificate** |
| [sprites-knowledge](sprites-knowledge/) | La tecnica portatile per creare concept art → sprite 2.5D pronti per il gioco per questo sistema | **215 ricette · 8 domini · 6 fasi · 92/215 verificate** |
| [tensor-engine-knowledge](tensor-engine-knowledge/) | Base di conoscenza verificata dei MOTORI che eseguono e addestrano i modelli di intelligenza artificiale localmente sul sistema RTX 5090 (Blackwell / sm_120 / Windows). | **193 motori · 10 domini · 17 fasi · 134/193 verificate** |
| [training-knowledge](training-knowledge/) | Base di conoscenza verificata delle TECNICHE di addestramento portatili: metodi, ricette, valori degli iperparametri, conoscenze sul set di dati e sulla valutazione per l'addestramento di LoRA / modelli ottimizzati sulla singola RTX 5090 (Blackwell / Windows / WSL2). Il livello "come addestrare" tra i pesi (conoscenza del modello) e il software (conoscenza del motore tensoriale). | **204 tecniche · 13 domini · 16 fasi · 101/204 verificate** |
| [vocology-knowledge](vocology-knowledge/) | Tecnica della voce cantata: vocalità (sorgente-filtro, registri, formante del cantante), prosodia musicale rispetto alla prosodia del parlato, allineamento delle parole alle note, SVS controllabile tramite partitura rispetto ai generatori di canzoni basati sul testo, valutazione dell'ammissione/insegnamento | **317 risultati · 19 domini · 13 fasi · 214/317 verificate** |
| [xrpl-knowledge](xrpl-knowledge/) | Base di conoscenza verificata dell'ECOSISTEMA XRP Ledger per un costruttore: funzionalità del protocollo, tipi di transazione, standard XLS, librerie client e strumenti, ciascuno contrassegnato con il suo stato attuale sulla mainnet / emendamento. Ecosistema completo: XRPL mainnet + Xahau/Hooks + la sidechain XRPL EVM + il livello istituzionale (RLUSD, conformità). | **457 funzionalità · 12 domini · 10 fasi · 362/457 verificate** |

La tabella viene generata da [`index.json`](index.json) tramite `shared/sync_readme_table.py` e `python verify.py` fallisce se si discosta. [`index.md`](index.md) è la stessa mappa scritta per gli agenti e [`index.html`](index.html) la visualizza.

Ogni cartella KB contiene il suo database, un file `catalog/` di pagine Markdown generate per dominio, una cartella `waves/` con i record di ricerca e verifica di ogni fase e il suo `README.md`.

## Avvio rapido

```bash
git clone https://github.com/mcp-tool-shop-org/readouts
cd readouts
python verify.py
```

`verify.py` richiede Python 3.10 o versioni successive e non richiede nulla al di fuori della libreria standard. I database sono semplici file SQLite, quindi qualsiasi client SQLite può aprirli.

Cerca in una KB tramite il suo indice di testo completo, quindi unisci di nuovo alla voce:

```sql
-- sqlite3 rust-knowledge/rust.db
SELECT r.name, r.verified
FROM recipes_fts f
JOIN recipes r ON r.id = f.rowid
WHERE recipes_fts MATCH 'rapier'
LIMIT 5;
```

Aggiungi `AND r.verified = 1` per mantenere solo ciò che il verificatore ha confermato. Lo stesso schema funziona in ogni KB. La tabella delle entità è denominata in [`index.md`](index.md): `recipes`, `findings`, `models`, `engines`, `techniques` o `capabilities`, ciascuna con un indice `<table>_fts` corrispondente. La maggior parte delle KB ha anche una vista `v_recommended` (docker-knowledge e vocology-knowledge hanno `v_load_bearing`). Queste viste selezionano in base al campo di raccomandazione di ciascuna KB, non in base a `verified`.

## Come un'entrata ottiene `verified`

1. **Una fase di ricerca.** Un percorso di ricerca per dominio scrive le voci e ogni voce cita le sue fonti come coppie `{url, claim}`.
2. **Un verificatore separato.** Un secondo agente, che non vede mai il ragionamento del ricercatore, controlla ogni voce rispetto alle pagine che cita e restituisce un verdetto. Nella maggior parte delle fasi, il verificatore proviene dalla stessa famiglia di modelli del ricercatore; alcune fasi aggiungono un membro di una famiglia diversa. Il record di ogni fase indica quale.
3. **Una definizione di `verified`.** `verified = 1` solo quando il verdetto esterno lo indica ([`shared/verdicts.py`](shared/verdicts.py)). Una voce senza verdetto rimane non verificata. Trattala come un'ipotesi, non come un fatto.
4. **Un compilatore, quando c'è codice.** Ogni controllo del codice in rust-knowledge viene compilato e, quando lo richiede, eseguito da `rustc 1.98.1`. Una ricetta il cui esempio fallisce la compilazione non viene mai verificata.

Ogni ciclo di elaborazione registra i propri dati nella cartella `waves/` del Knowledge Base (KB): `dispatch.md` (cosa è stato richiesto e cosa è stato restituito), `research-raw.json` (cosa è stato caricato) e, se presente, `verification.md` (cosa è stato rilevato dal verificatore e dal compilatore). I KB che mantengono un registro permanente dei risultati lo conservano in `verification/verdicts.json`.

## Assegna un agente a una specifica sezione

Due indici di configurazione impediscono a un agente di leggere l'intero corpus:

1. Il file principale [`.claude/loadout/index.json`](.claude/loadout/index.json) indirizza un compito al KB corretto.
2. Il file `.claude/loadout/index.json` di ciascun KB lo indirizza al dominio corretto all'interno di quel KB.

```bash
npx @mcptoolshop/loadout-os validate .claude/loadout/index.json
npx @mcptoolshop/loadout-os resolve --project .
```

`resolve` unisce anche il proprio livello di configurazione globale, se presente.

## Verifica tu stesso il corpus

`python verify.py` rappresenta il livello di base del repository. Verifica che i file generati siano coerenti con i database: che ogni riga di testo completo sia collegata alla sua voce corrispondente, che nessuna voce verificata sia priva di una fonte, che `verified` faccia riferimento a un risultato esterno, che la struttura principale e la tabella di questo file README corrispondano ai database e che nessun collegamento relativo sia interrotto.

- `FAIL` viola un contratto o fornisce dati errati. Blocca la pubblicazione.
- `WARN` è un difetto reale, noto, definito e registrato.

Ogni errore (FAIL) e avviso (WARN) include un codice stabile e un suggerimento per il passaggio successivo. `python verify.py --json` stampa un singolo oggetto JSON per ogni controllo. Il codice di uscita è 0 in caso di esito positivo, 1 in caso di errore e 2 se lo stesso controllo si è interrotto. Il sistema di integrazione continua (CI) lo esegue ogni volta che viene apportata una modifica al corpus.

## Sicurezza e modello di minaccia

- **Cos'è questo repository:** dati. Contiene database SQLite, file Markdown, JSON e gli script Python che li hanno creati. Nessuno script viene eseguito durante l'installazione e non è necessario installare nulla.
- **Il percorso di lettura è locale.** L'interrogazione di un database, `verify.py`, e i generatori (`regen.py`, `shared/gen_*.py`, il file `load_db.py` di ciascun KB, `gen_catalog.py` e `gen_loadout.py`) leggono i file in questa copia locale e scrivono solo i file derivati al suo interno. Non stabiliscono alcuna connessione di rete, non leggono credenziali e non inviano dati di telemetria. `verify.py` non scrive nulla.
- **Gli strumenti di ricerca non lo sono.** Gli script conservati come registro di come sono stati creati i cicli di elaborazione (ad esempio, ciascun `verify_cloud.py`, il file `openrouter_lane.py` di rust-knowledge e il file `verifier/` di tensor-engine-knowledge) chiamano un modello: un daemon Ollama locale o OpenRouter con un `OPENROUTER_API_KEY` che si imposta nell'ambiente. Alcuni recuperano anche le pagine che citano. Nessuna chiave viene archiviata nel repository. `compile_oracle.py setup` scarica le librerie Rust specificate tramite cargo, una sola volta. Nessuno di questi script viene eseguito a meno che tu non lo esegua manualmente.
- **Autorizzazioni:** accesso in lettura alla copia locale; accesso in scrittura solo se si rigenera il contenuto.
- **Nessuna telemetria**, in nessuna parte del repository.
- **Qual è il contenuto:** note di ricerca con citazioni. Una voce non verificata è un'ipotesi, non un fatto. Le note sulla licenza relative a modelli, set di dati e librerie non costituiscono una consulenza legale; leggi la licenza stessa prima di distribuire qualsiasi cosa.

Per segnalare un problema, consulta il file [SECURITY.md](SECURITY.md).

## Manutenzione

Il file [MAINTENANCE.md](MAINTENANCE.md) è il manuale operativo: aggiunta di un ciclo di elaborazione o di un KB, esecuzione di una verifica completa e le insidie che hanno già fatto perdere un pomeriggio a qualcuno. Il file [CONVENTIONS.md](CONVENTIONS.md) descrive la struttura che ogni KB condivide. Il [manuale](https://mcp-tool-shop-org.github.io/readouts/handbook/) illustra in dettaglio l'interrogazione, la verifica e l'instradamento. Le modifiche sono elencate nel file [CHANGELOG.md](CHANGELOG.md).

## Licenza

[MIT](LICENSE)

---

Creato da <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
