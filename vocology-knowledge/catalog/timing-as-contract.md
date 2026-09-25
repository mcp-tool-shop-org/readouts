# Timing is a contract; Comfy fills the window
_auto-created from wave lane_ · wave 13 · 2026-09-14 · [‹ catalog index](README.md)

22 findings · 7 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| ACE-Step | Gong et al. · 2025 | ACE-Step's audio_duration sizes a latent canvas - literally frame_length = int(duration * 44100 / 512 / 8), used as the last dimension of the (bsz, 8, 16, frame_length) latent - and it is not note MIDI: the model generates audio latents by diffusion and 'midi' appears nowhere in the repository. Correction: BPM is NOT an ACE-Step parameter at all (zero occurrences repo-wide); tempo can only ride along as free text inside the tag prompt, so it exerts no structural timing control. Gong et al., arXiv:2506.00045, 28 May 2025. | ✓ |
| ByteDanceSeedAudio | Comfy-Org · 2026 | The ComfyUI ByteDanceSeedAudio node documents per-sentence timestamp stamps of the form [5.5s:8.0s] that control 'when and how long' a quoted line is spoken - i.e. an absolute output timeline. Two limits the original claim missed: (1) stamps work only on model 'seed-audio-1.0-multilingual'; the tooltip states 'seed-audio-1.0: English and Chinese only, no timing control'. (2) 'Writes leading silence' is NOT documented anywhere in the node source or the Comfy docs - treat it as an unverified empirical observation and re-measure before depending on it. Limits: max 2 minutes per run, 3000 characters. | ✓ |
| Exploring Neural Transducers for End-to-End Speech Recognition (CTC vs attention) | Battenberg et al. · 2017 | CTC = hard monotonic latent alignments; attention = soft weighted frames. Holds for why CTC lyrics-to-audio ≠ lyrics-to-MIDI score-lock. Author per Verifier: Battenberg et al. (not Battenberg). | ✓ |
| Hybrid CTC/attention ASR | Watanabe / MERL · 2017 | CTC constrains monotonicity; attention alone is too flexible for speech order — prefer hard note/lyric schedules over free soft attention for practice lock. | ✓ |
| Sinsy | Hono et al. · 2021 | Sinsy time-lag: vowel onset tracks the score; consonants anticipate. | ✓ |
| music21 lyricTimingsFromEvents / MIDI translate | Cuthbert / music21 · 2024 | Music IR keeps lyric meta timestamps separate from Note pitch/time — dual IR clocks; one Lyric tick does not encode melisma across many MIDI notes. | ✓ |
| pretty_midi Lyric container | Raffel / pretty_midi · 2024 | pretty_midi Lyric events are separate from Note objects — dual-clock analog for lyric vs note schedules. | ✓ |
| Apache License 2.0 §4 Redistribution | ASF · 2004 | Analog: Derivative Works may add different license terms on modifications while retaining notices. Holds for Kokoro Apache CAST vs paid-ToS STS output (C5) — transform can change distribution terms. Limit: software redistribution ≠ every Cloud ToS clause. | · |
| Deleting object versions (S3 Versioning) | AWS · docs | Analog: simple DELETE inserts a delete marker (soft-delete); permanent remove needs versionId. Holds for soft-delete vs rewrite of the lock artifact. Limit: S3 bucket ops ≠ jam-session score edits. | · |
| Gaps: ACCEPT 23/30/50 flip-cap only; Flips beyond ACCEPT: 0; Nodes: 0 | vocology-knowledge · 2026 | Counts are README/catalog/DB/script/dispatch stamps after 041–043; ACCEPT 23/30/50 appears only as flip-cap constraint language. | · |
| Git Internals | Git Objects · Chacon & Straub / git-scm | Analog: content-addressable store — insert bytes, retrieve by SHA-1 key. Holds for Cloud upload key / lock.wav identity (hash-addressed input, not a mutable path). Limit: git object DB ≠ Comfy Cloud storage API. | · |
| How Nix Works / content-addressed store | NixOS · docs | Analog: hermetic builds keyed by content hashes of inputs. Holds for immutable input→transform pipelines (same lock bytes ⇒ same CAS identity before STS). Limit: package store ≠ audio STS service. | · |
| IndexTTS2 | Zhou et al. · 2025 | Autoregressive TTS has no duration unless token count / MFA durations are inputs. | · |
| LoadAudio | Comfy-Org · docs | Analog: loads only files present in ComfyUI input directory after upload. Holds for upload→storage-key→LoadAudio→STS pipeline (wave-02 finding 21). Limit: local input folder wording; Cloud key shape is operator-verified separately. | · |
| PROV-DM: The PROV Data Model | W3C · 2013 | Analog: Entity + Activity + derivation (`wasDerivedFrom`) for input→transform→output lineage. Holds for lock.wav Entity → STS/Seed Activity → timbre-transformed Entity. Limit: generic provenance model; no audio clock/score semantics. | · |
| README vs catalog: 12 matches; parenthetical nine lag vs 12 (report only) | vocology-knowledge · 2026 | Status 12/175 matches DB verified=1 12 and catalog shortlist 12 ✓; parenthetical says nine abstract-supported accepts from wave-1 — wording lag vs 12 (report only). | · |
| README.md Catalog 175 · 12/175 · 9 waves | vocology-knowledge · 2026 | Catalog 175 · 12/175 · 9 waves; waves 7–9 cite 21/21/22 findings verified=0. | · |
| catalog/README.md 175 findings · 12/175 verified | vocology-knowledge/catalog · 2026 | 175 findings · 12/175 verified; NEVER hand-edited; lane bullets 31+8+27+38+41+6+1+14+9 (=175); verified shortlist table lists 12 ✓ rows. | · |
| findings.db 175 / verified 12 / waves 9 | vocology-knowledge/findings.db · 2026 | findings 175; verified=1 12 / verified=0 163; waves 9; categories 9; finding_sources 174. | · |
| scripts/gen_catalog.py never hand-edit | vocology-knowledge/scripts · 2026 | generate catalog/*.md from findings.db; NEVER hand-edit catalog/; per-lane header emits findings · verified counts from DB. | · |
| scripts/refresh_meta.py FROM DB | vocology-knowledge/scripts · 2026 | Derive meta currency FROM the DB (MAX wave), never the ingest wave (MetaDriftError path). | · |
| wave-07/08/09 dispatch flip-cap 0 | vocology-knowledge/waves · 2026 | wave-07/08/09 dispatch constraints: Flips beyond ACCEPT 23/30/50: 0; wave-09 also | · |

## Detail

### ACE-Step · `load-bearing`
**ACE-Step's audio_duration sizes a latent canvas - literally frame_length = int(duration * 44100 / 512 / 8), used as the last dimension of the (bsz, 8, 16, frame_length) latent - and it is not note MIDI: the model generates audio latents by diffusion and 'midi' appears nowhere in the repository. Correction: BPM is NOT an ACE-Step parameter at all (zero occurrences repo-wide); tempo can only ride along as free text inside the tag prompt, so it exerts no structural timing control. Gong et al., arXiv:2506.00045, 28 May 2025.**
- **Implication:** ACE-Step cannot honor New Britain onsets.
- **Identifier:** `arXiv:2506.00045`
- **Verify:** Pipeline code: frame_length = int(duration * 44100 / 512 / 8), then shape=(bsz,8,16,frame_length) - duration literally sizes the latent. But GitHub code search over the whole repo returns 0 hits for 'bpm' and 0 for 'midi'.
- **Sources:** [ACE-Step](https://arxiv.org/abs/2506.00045)

### ByteDanceSeedAudio · `load-bearing`
**The ComfyUI ByteDanceSeedAudio node documents per-sentence timestamp stamps of the form [5.5s:8.0s] that control 'when and how long' a quoted line is spoken - i.e. an absolute output timeline. Two limits the original claim missed: (1) stamps work only on model 'seed-audio-1.0-multilingual'; the tooltip states 'seed-audio-1.0: English and Chinese only, no timing control'. (2) 'Writes leading silence' is NOT documented anywhere in the node source or the Comfy docs - treat it as an unverified empirical observation and re-measure before depending on it. Limits: max 2 minutes per run, 3000 characters.**
- **Implication:** jam-sessions startSec/durationSec emit those stamps; Python is the clock.
- **Identifier:** `Comfy ByteDanceSeedAudio`
- **Verify:** Node source read. Tooltip verbatim: a line 'can start with a timestamp range that controls when and how long it is spoken, e.g. [5.5s:8.0s]'. Stamps are multilingual-model-only; leading silence is undocumented.
- **Sources:** [ByteDanceSeedAudio](https://docs.comfy.org/built-in-nodes/ByteDanceSeedAudio)

### Exploring Neural Transducers for End-to-End Speech Recognition (CTC vs attention) · `load-bearing`
**CTC = hard monotonic latent alignments; attention = soft weighted frames. Holds for why CTC lyrics-to-audio ≠ lyrics-to-MIDI score-lock. Author per Verifier: Battenberg et al. (not Battenberg).**
- **Implication:** CTC vs attention analog hold-with-limit.
- **Identifier:** `arXiv:1707.07413`
- **Verify:** Full text verbatim: CTC models 'marginalize over all possible hard alignments while the attention mechanism models a soft alignment between each output step and every input step'. Battenberg+10, 2017. Speech (Hub5'00).
- **Sources:** [Exploring Neural Transducers for End-to-End Speech Recognition (CTC vs attention)](https://arxiv.org/abs/1707.07413)

### Hybrid CTC/attention ASR · `load-bearing`
**CTC constrains monotonicity; attention alone is too flexible for speech order — prefer hard note/lyric schedules over free soft attention for practice lock.**
- **Implication:** Hybrid CTC constraint hold-with-limit.
- **Identifier:** `merl:TR2017-190`
- **Verify:** TR2017-190 PDF verbatim: 'This basic temporal attention mechanism is too flexible in the sense that it allows extremely nonsequential alignments'; 'CTC permits the efficient computation of a strictly monotonic alignment'.
- **Sources:** [Hybrid CTC/attention ASR](https://www.merl.com/publications/docs/TR2017-190.pdf)

### Sinsy · `load-bearing`
**Sinsy time-lag: vowel onset tracks the score; consonants anticipate.**
- **Implication:** stamps should target vowel windows, not letter onsets.
- **Identifier:** `arXiv:2108.02776`
- **Verify:** Sinsy Sec III-C time-lag model, verbatim: 'humans generally tend to begin to utter consonants earlier than the absolute musical note onset timing'; it uses 'the first vowel or silence for rests' as the reference phoneme.
- **Sources:** [Sinsy](https://arxiv.org/abs/2108.02776)

### music21 lyricTimingsFromEvents / MIDI translate · `load-bearing`
**Music IR keeps lyric meta timestamps separate from Note pitch/time — dual IR clocks; one Lyric tick does not encode melisma across many MIDI notes.**
- **Implication:** Lyric IR ≠ note IR hold-with-limit.
- **Identifier:** `music21:midiTranslate`
- **Verify:** Source read: lyricTimingsFromEvents(...) -> dict[int, str] reads only MetaEvents.LYRIC; 'If more than one lyric is found at a given tick time, the last one found is stored' - one tick, one string, so melisma cannot be encoded.
- **Sources:** [music21 lyricTimingsFromEvents / MIDI translate](https://music21.org/music21docs/moduleReference/moduleMidiTranslate.html)

### pretty_midi Lyric container · `load-bearing`
**pretty_midi Lyric events are separate from Note objects — dual-clock analog for lyric vs note schedules.**
- **Implication:** pretty_midi lyric container hold-with-limit.
- **Identifier:** `pretty_midi:Lyric`
- **Verify:** Source read: class Lyric holds only (text, time), distinct from Note (velocity, pitch, start, end), and lyrics live on the top-level PrettyMIDI.lyrics list rather than on Instrument. Dual-clock analog holds.
- **Sources:** [pretty_midi Lyric container](https://craffel.github.io/pretty-midi/containers.html)

### Apache License 2.0 §4 Redistribution · `directional`
**Analog: Derivative Works may add different license terms on modifications while retaining notices. Holds for Kokoro Apache CAST vs paid-ToS STS output (C5) — transform can change distribution terms. Limit: software redistribution ≠ every Cloud ToS clause.**
- **Implication:** STUDY-043 provenance analog hold-with-limit. Fail-transfers omitted.
- **Identifier:** `https://www.apache.org/licenses/LICENSE-2.0`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Apache License 2.0 §4 Redistribution](https://www.apache.org/licenses/LICENSE-2.0)

### Deleting object versions (S3 Versioning) · `directional`
**Analog: simple DELETE inserts a delete marker (soft-delete); permanent remove needs versionId. Holds for soft-delete vs rewrite of the lock artifact. Limit: S3 bucket ops ≠ jam-session score edits.**
- **Implication:** STUDY-043 provenance analog hold-with-limit. Fail-transfers omitted.
- **Identifier:** `https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeletingObjectVersions.html`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Deleting object versions (S3 Versioning)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeletingObjectVersions.html)

### Gaps: ACCEPT 23/30/50 flip-cap only; Flips beyond ACCEPT: 0; Nodes: 0 · `directional`
**Counts are README/catalog/DB/script/dispatch stamps after 041–043; ACCEPT 23/30/50 appears only as flip-cap constraint language.**
- **Implication:** STUDY-064 catalog/README honesty.
- **Identifier:** `file://vocology-knowledge/gaps-accept-flip-cap`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Gaps: ACCEPT 23/30/50 flip-cap only; Flips beyond ACCEPT: 0; Nodes: 0](https://github.com/mcp-tool-shop-org/readouts-internal/blob/main/vocology-knowledge/README.md)

### Git Internals · `directional`
**Analog: content-addressable store — insert bytes, retrieve by SHA-1 key. Holds for Cloud upload key / lock.wav identity (hash-addressed input, not a mutable path). Limit: git object DB ≠ Comfy Cloud storage API.**
- **Implication:** STUDY-043 provenance analog hold-with-limit. Fail-transfers omitted.
- **Identifier:** `https://git-scm.com/book/en/v2/Git-Internals-Git-Objects`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Git Internals](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

### How Nix Works / content-addressed store · `directional`
**Analog: hermetic builds keyed by content hashes of inputs. Holds for immutable input→transform pipelines (same lock bytes ⇒ same CAS identity before STS). Limit: package store ≠ audio STS service.**
- **Implication:** STUDY-043 provenance analog hold-with-limit. Fail-transfers omitted.
- **Identifier:** `https://nixos.org/guides/how-nix-works/`
- **Verify:** no external verdict — not yet swept
- **Sources:** [How Nix Works / content-addressed store](https://nixos.org/guides/how-nix-works/)

### IndexTTS2 · `directional`
**Autoregressive TTS has no duration unless token count / MFA durations are inputs.**
- **Implication:** a prompt cannot be the metronome.
- **Identifier:** `arXiv:2506.21619`
- **Verify:** no external verdict — not yet swept
- **Sources:** [IndexTTS2](https://arxiv.org/abs/2506.21619)

### LoadAudio · `directional`
**Analog: loads only files present in ComfyUI input directory after upload. Holds for upload→storage-key→LoadAudio→STS pipeline (wave-02 finding 21). Limit: local input folder wording; Cloud key shape is operator-verified separately.**
- **Implication:** STUDY-043 provenance analog hold-with-limit. Fail-transfers omitted.
- **Identifier:** `https://docs.comfy.org/built-in-nodes/LoadAudio`
- **Verify:** no external verdict — not yet swept
- **Sources:** [LoadAudio](https://docs.comfy.org/built-in-nodes/LoadAudio)

### PROV-DM: The PROV Data Model · `directional`
**Analog: Entity + Activity + derivation (`wasDerivedFrom`) for input→transform→output lineage. Holds for lock.wav Entity → STS/Seed Activity → timbre-transformed Entity. Limit: generic provenance model; no audio clock/score semantics.**
- **Implication:** STUDY-043 provenance analog hold-with-limit. Fail-transfers omitted.
- **Identifier:** `https://www.w3.org/TR/prov-dm/`
- **Verify:** no external verdict — not yet swept
- **Sources:** [PROV-DM: The PROV Data Model](https://www.w3.org/TR/prov-dm/)

### README vs catalog: 12 matches; parenthetical nine lag vs 12 (report only) · `directional`
**Status 12/175 matches DB verified=1 12 and catalog shortlist 12 ✓; parenthetical says nine abstract-supported accepts from wave-1 — wording lag vs 12 (report only).**
- **Implication:** STUDY-064 catalog/README honesty.
- **Identifier:** `file://vocology-knowledge/catalog-parenthetical-lag`
- **Verify:** no external verdict — not yet swept
- **Sources:** [README vs catalog: 12 matches; parenthetical nine lag vs 12 (report only)](https://github.com/mcp-tool-shop-org/readouts-internal/blob/main/vocology-knowledge/catalog/README.md)

### README.md Catalog 175 · 12/175 · 9 waves · `directional`
**Catalog 175 · 12/175 · 9 waves; waves 7–9 cite 21/21/22 findings verified=0.**
- **Implication:** STUDY-064 catalog/README honesty.
- **Identifier:** `file://vocology-knowledge/README.md`
- **Verify:** no external verdict — not yet swept
- **Sources:** [README.md Catalog 175 · 12/175 · 9 waves](https://github.com/mcp-tool-shop-org/readouts-internal/blob/main/vocology-knowledge/README.md)

### catalog/README.md 175 findings · 12/175 verified · `directional`
**175 findings · 12/175 verified; NEVER hand-edited; lane bullets 31+8+27+38+41+6+1+14+9 (=175); verified shortlist table lists 12 ✓ rows.**
- **Implication:** STUDY-064 catalog/README honesty.
- **Identifier:** `file://vocology-knowledge/catalog/README.md`
- **Verify:** no external verdict — not yet swept
- **Sources:** [catalog/README.md 175 findings · 12/175 verified](https://github.com/mcp-tool-shop-org/readouts-internal/blob/main/vocology-knowledge/catalog/README.md)

### findings.db 175 / verified 12 / waves 9 · `directional`
**findings 175; verified=1 12 / verified=0 163; waves 9; categories 9; finding_sources 174.**
- **Implication:** STUDY-064 catalog/README honesty.
- **Identifier:** `file://vocology-knowledge/findings.db`
- **Verify:** no external verdict — not yet swept
- **Sources:** [findings.db 175 / verified 12 / waves 9](https://github.com/mcp-tool-shop-org/readouts-internal/blob/main/vocology-knowledge/findings.db)

### scripts/gen_catalog.py never hand-edit · `directional`
**generate catalog/*.md from findings.db; NEVER hand-edit catalog/; per-lane header emits findings · verified counts from DB.**
- **Implication:** STUDY-064 catalog/README honesty.
- **Identifier:** `file://vocology-knowledge/scripts/gen_catalog.py`
- **Verify:** no external verdict — not yet swept
- **Sources:** [scripts/gen_catalog.py never hand-edit](https://github.com/mcp-tool-shop-org/readouts-internal/blob/main/vocology-knowledge/scripts/gen_catalog.py)

### scripts/refresh_meta.py FROM DB · `directional`
**Derive meta currency FROM the DB (MAX wave), never the ingest wave (MetaDriftError path).**
- **Implication:** STUDY-064 catalog/README honesty.
- **Identifier:** `file://vocology-knowledge/scripts/refresh_meta.py`
- **Verify:** no external verdict — not yet swept
- **Sources:** [scripts/refresh_meta.py FROM DB](https://github.com/mcp-tool-shop-org/readouts-internal/blob/main/vocology-knowledge/scripts/refresh_meta.py)

### wave-07/08/09 dispatch flip-cap 0 · `directional`
**wave-07/08/09 dispatch constraints: Flips beyond ACCEPT 23/30/50: 0; wave-09 also**
- **Implication:** STUDY-064 catalog/README honesty.
- **Identifier:** `file://vocology-knowledge/waves/wave-07-09-dispatch`
- **Verify:** no external verdict — not yet swept
- **Sources:** [wave-07/08/09 dispatch flip-cap 0](https://github.com/mcp-tool-shop-org/readouts-internal/blob/main/vocology-knowledge/waves/)

