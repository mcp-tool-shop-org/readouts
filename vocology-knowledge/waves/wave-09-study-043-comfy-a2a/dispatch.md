# Wave 9 — STUDY-043 Comfy Cloud a2a / SVC / cover provenance

**Tip:** `a2ee93c`
**Constraints:** Flips beyond ACCEPT 23/30/50: 0. Nodes invented: 0. Do not invent Cover/Repaint as live Comfy nodes. Fail-transfers flagged.

## Findings → recommendations
- SoftVC/DiffSVC/FreeVC/FreeSVC/LDM-SVC: content-from-source SVC/STS.
- DiffRhythm2/SongEcho/ACE-Step1.5: cover ≠ MIDI score-lock.
- ElevenLabs STS word-keep; SeedAudio prompt/stamps/pitch_rate; LoadAudio input-dir; blake3/UUID assets; ACE denoise=1 ignore; Cover/Repaint unsupported in ComfyUI.
- Hold Git/Nix/PROV/S3/Apache/LoadAudio upload; omit HTTPS→LoadAudio + ACE-as-MIDI fail-transfers.

## Evidence
`/workspace/studio/research/STUDY-043/` five packs + research-raw.json
