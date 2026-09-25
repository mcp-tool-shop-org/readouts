# Wave 1 — Verification receipt

**Method:** Each of the 6 research lanes was followed by a separate adversarial retrieval-verifier agent (a different lens, researcher reasoning hidden). For every entry the verifier WebFetched the source URLs and checked (1) the tool/model exists and resolves, (2) the license / `commercial_use` claim is accurate — the decisive field — correcting it where wrong, and (3) currency. Default verdict on uncertainty = NOT verified. Per the readouts convention this is a same-model-family verifier + a retrieval oracle (the live page is the decorrelating element); the planned upgrade is a family-different verifier.

**Result: 52 / 53 verified.** The one unverified entry (ControlNet OpenPose pose-grid, sheet-direct) resolves but its specific pose-grid claim wasn't fully confirmable — kept as `verified=0`, status recommended, for a later pass.

## Notable verifier corrections / confirmations (license = decisive)
- **Hunyuan3D-2.1** — confirmed from the LICENSE file: commercial permitted only &lt;1M MAU AND territory **excludes EU/UK/South Korea**; attribution required. `commercial_use=conditional`, status downgraded to situational (real legal hazard for a worldwide JRPG).
- **TRELLIS.2-4B** — MIT confirmed on both the GitHub repo and the HF model card (code + weights). Corroborates wave-0.
- **Step1X-3D** — Apache-2.0 confirmed via the GitHub license API.
- **Zero123 lineage** — Zero123++/Era3D confirmed CC-BY-NC → avoid; Stable-Zero123/SV3D confirmed conditional. **MV-Adapter** confirmed Apache → the clean NVS option.
- **Sparc3D** — academic/non-commercial → avoid for shipped assets.

## Caveat
evidence_strength here is research-level (reproduced-from-source / community-claim / single-reported-run), NOT measured on this rig. VRAM/quality figures are as-reported by sources; promote an entry to `measured-on-rig` only after the studio runs it (the wave-0 pattern). Verified means "the source resolves and the license is accurate," not "we ran it."
