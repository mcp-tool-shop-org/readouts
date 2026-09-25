# readouts — model-knowledge · wave dispatches

> The research log: how this KB was built, wave by wave. 19 waves · generated 2026-09-25.

## Wave 0 — Local downloaded workflows (2026-06-02)

_workflows · hands-on · local · +0 models · +0 sources_

Starter workflow .json files fetched from Comfy-Org/workflow_templates

## Wave 1 — Foundation — best current models per domain (2026-06-02)

_all (image, control, video, 3d, audio, llm, comfy) · 14 agents · synthesized · +52 models · +179 sources_

**Verifier:** Reasoning-stripped adversarial verifier per lane; WebFetch as retrieval oracle (existence/license/specs). Family-different prism/roleos path deferred to a later wave.

## Wave 2 — Wave 2 (2026-06-02)

_all (image, control, video, 3d, audio, llm, comfy) · 14 agents · synthesized · +35 models · +96 sources_

**Verifier:** Reasoning-stripped adversarial verifier per lane; WebFetch as retrieval oracle (existence/license/specs). Family-different prism/roleos path deferred to a later wave.

## Wave 3 — Wave 3 (2026-06-02)

_all (image, control, video, 3d, audio, llm, comfy) · 12 agents · synthesized · +21 models · +52 sources_

**Verifier:** Reasoning-stripped adversarial verifier per lane; WebFetch as retrieval oracle (existence/license/specs). Family-different prism/roleos path deferred to a later wave.

## Wave 4 — Wave 4 (2026-06-02)

_all (image, control, video, 3d, audio, llm, comfy) · 8 agents · synthesized · +11 models · +31 sources_

**Verifier:** Reasoning-stripped adversarial verifier per lane; WebFetch as retrieval oracle (existence/license/specs). Family-different prism/roleos path deferred to a later wave.

## Wave 5 — Wave 5 (2026-06-26)

_all (image, control, video, 3d, audio, llm, comfy) · 2 agents · synthesized · +2 models · +2 sources_

**Verifier:** Reasoning-stripped adversarial verifier per lane; WebFetch as retrieval oracle (existence/license/specs). Family-different prism/roleos path deferred to a later wave.

## Wave 6 — Beyond image-gen — ComfyUI / Comfy-Cloud feasibility (cloud_feasible axis) (2026-06-30)

_cross-domain cloud-feasibility axis (video, audio, 3d, caption, control) + new audio model + Comfy Cloud platform · 15 agents · synthesized · +1 models · +2 sources_

**Verifier:** study-swarm wf_92f13b67-f91 (2026-06-30): 7 research lanes -> per-lane reasoning-stripped WebFetch retrieval-oracle verifier (existence / cloud-support / license) -> completeness critic. Receipts in verification.md. Family-different prism/roleos path deferred (same posture as waves 1-5).

## Wave 7 — Cloud audio measured — Comfy-Agent dialog receipts (the Motif front-end) (2026-08-19)

_audio + comfy — EMPIRICAL provenance class: measured on this account (billing feed, pulled workflow records, decoded FLAC headers, LUFS manifests), plus agent-reported live-catalog facts marked as such · 2 agents · synthesized · +0 models · +6 sources_

**Verifier:** NOT a web-retrieval swarm: a 5-round dialog with the Comfy Cloud in-app agent (live-catalog access), every load-bearing claim re-verified from this rig over the official API — jobs re-billed from the account feed, graphs re-pulled by workflow_id, outputs re-downloaded and FLAC-header-decoded, LUFS manifests read. Two agent claims corrected by measurement (stems decode 44.1 kHz, not 48; SFX v2 silently lost its duration input); two KB claims corrected by the agent's catalog access (ACE-Step license string not surfaced by the catalog; Chatterbox now ON cloud, superseding wave-6 'unknown'). Claims that remain single-source (agent catalog browsing, not independently measured) are labeled 'agent-reported 2026-08-19' in their notes and stay advisory until re-measured. Receipts: model-knowledge/dialogs/comfy-agent/ rounds 01-05.

## Wave 8 — Cloud caption measured — Comfy-Agent captioner thread receipts (+ the local native-transformers pin) (2026-08-19)

_caption + comfy — EMPIRICAL provenance class: measured on this account (billing feed re-pulled at ingest, graph pulled by workflow_id and archived both forms, caption artifact on disk) and on this rig (plain-sight v0.1.0 commit fdd49b3, HF license API re-pulled at ingest), plus agent-reported live-catalog facts marked as such · 2 agents · synthesized · +0 models · +6 sources_

**Verifier:** NOT a web-retrieval swarm: a 3-round dialog with the Comfy Cloud in-app agent (2026-08-19, thread closed both sides), every load-bearing claim re-verified from this rig — billing feed re-pulled LIVE at ingest (job 26a78ccd = 6.732932 gpu-sec, rtx_pro_6000), archived api-format graph matched widget-for-widget against the ordered spec, editor-format graph passed mechanical link-node cross-reference (7 nodes / 7 links), caption artifact on disk (454 bytes, 5 sentences), florence-community/Florence-2-large HF license tag re-pulled LIVE at ingest (mit, 441k downloads), plain-sight DEFAULT_MODEL_ID grepped from source at commit fdd49b3. TWO corrections to our own KB landed by this wave: (1) waves 1/3 'credit-FREE on the cloud GPU' is FALSE — cloud Florence-2 bills active GPU-sec like any OSS job; (2) the intake's derived '~1.3 credits/caption' did not survive verification — 6.73 gpu-sec at the wave-6 verified ~0.266 cr/GPU-sec rate is ~1.8 credits (arithmetic slip caught at ingest; gpu_seconds is the authoritative figure). Claims sourced only from the agent's catalog browsing (one-image-per-job, no-8B-VLM-packs absence claims) are labeled 'agent-reported 2026-08-19' and stay advisory until re-measured. Receipts: model-knowledge/dialogs/comfy-agent/ captioner rounds 01-03.

## Wave 9 — Local TTS append from DR-001 (Qwen3-TTS/Kokoro/Chatterbox already present — five new audio rows, all unverified) (2026-08-30)

_audio — local TTS models from the 2026-08-30 DR-001 pack; no duplicate of Chatterbox, Qwen3-TTS, or Kokoro-82M · 1 agents · synthesized · +5 models · +9 sources_

**Verifier:** JOB-R-014 retrieval-check. verified=1 only where overall=confirmed: Fun-CosyVoice 3.0 0.5B, IndexTTS-2.5, F5-TTS (official ckpt), piper1-gpl. Pocket TTS stays unverified (weight SPDX unconfirmed). saghul/local-tts stays extra. Remainder 🛑 operator prism.

## Wave 10 — Wave 10 — STUDY-005 reopen: Alice distill + FLUX.1-dev NC contrast (shortlist mostly already present) (2026-09-06)

_image-base, video — commercial-first reopen; Pocket TTS 127 untouched · 3 agents · synthesized · +2 models · +2 sources_

**Verifier:** STUDY-015 from STUDY-005 Verifier ✅. Omitted already-in-DB shortlist (Z-Image, Qwen-Image/-Edit, ControlNet Union, FLUX.2-klein, Wan2.2, TRELLIS.2, TripoSG, Qwen3, FLUX.1-Kontext). A2 LoRA-via-LF + A8 elastic-GPU omitted (unverified). Pocket 127 stays verified=0. New rows default unverified (empty verdicts).

## Wave 11 — Wave 11 — STUDY-030 IMAGE deepen (papers + HF cards + license/VRAM holds; no new models) (2026-09-07)

_image-base — open IMAGE deepen; commercial-safe HF; license/VRAM honesty; Pocket 127 untouched · 3 agents · synthesized · +0 models · +16 sources_

**Verifier:** STUDY-030 Verifier ✅. Scholar 8/8 papers. Practitioner 8/8 HF (commercial-safe + FLUX.2-dev NC contrast). Analogist 1–6 hold; #7–#8 fail-transfer omitted. No new model rows (HDM deepen-local only). Pocket 127 untouched. FLUX.2-dev commercial flip: 0. Named models invented: 0.

## Wave 12 — Wave 12 — STUDY-031 VIDEO deepen (papers + Wan/LTX cards + KV/cinematic holds; no new models; A14B-32GB invent: 0) (2026-09-07)

_video — open VIDEO deepen; Wan TI2V-5B/Distill ≤32GB; A14B/S2V ≥80GB peers; LTX conditional; Pocket 127 untouched · 3 agents · synthesized · +0 models · +22 sources_

**Verifier:** STUDY-031 Verifier ✅. Scholar 8/8. Practitioner 7 verified + A14B card verified without consumer-VRAM-offload clause. Analogist 1–6 hold; #7–#8 fail-transfer omitted. No new model rows. Pocket 127 untouched. A14B-32GB invent: 0. Named models invented: 0.

## Wave 13 — Wave 13 — STUDY-032 3D deepen (papers + MIT/Hunyuan cards + NC-dep/game-ready holds; no new models) (2026-09-07)

_3d — open 3D deepen; TRELLIS/Hi3DGen/TripoSG MIT ≤32GB; Hunyuan conditional contrast; NC dep poison; Pocket 127 untouched · 3 agents · synthesized · +0 models · +22 sources_

**Verifier:** STUDY-032 Verifier ✅. Scholar 8/8. Practitioner 8/8 (Hunyuan conditional — no permissive flip). Analogist 1–6 hold; #7–#8 fail-transfer omitted. No new model rows. Pocket 127 untouched. Named models invented: 0.

## Wave 14 — Wave 14 — STUDY-033 LLM/VLM/caption deepen (no TTS; JoyCaption Apache invent: 0; no quant-as-card-text) (2026-09-07)

_llm, caption — CapRL/Qwen/Florence/Gemma deepen; JoyCaption Llama not Apache; Pocket 127 untouched; TTS invent: 0 · 3 agents · synthesized · +0 models · +21 sources_

**Verifier:** STUDY-033 Verifier ✅. Scholar 8/8. Practitioner 8/8 soft notes (quant phrase not on card; JoyCaption Apache invent: 0). Analogist 1–6 hold; #7–#8 fail-transfer omitted. No new models. Pocket 127 untouched. TTS invent: 0.

## Wave 15 — Wave 15 — STUDY-050 IMAGE leftover deepen (Pocket 127 stays; models invented: 0) (2026-09-07)

_image-edit / image-control — RF/DiT edit-control beyond STUDY-030; license/VRAM deepen; Pocket 127 stays verified=0; models invented: 0; no Apache on NC · 3 agents · synthesized · +0 models · +22 sources_

**Verifier:** STUDY-050 Verifier ✅. Scholar 8/8. Practitioner 8/8. Analogist 1–6 hold; #7–#8 fail-transfer omitted. Pocket 127 stays verified=0. Models invented: 0. Do not invent Apache on NC (Kontext). Extras-only land (no new model rows).

## Wave 16 — Wave 16 — STUDY-051 VIDEO VRAM honesty (A14B-32GB invent: 0; Pocket stays) (2026-09-07)

_video — Wan/Hunyuan VRAM honesty beyond STUDY-031; A14B ≥80GB refuse; offload≠fit; GGUF labels unverified; Pocket 127 stays; A14B-32GB invent: 0 · 3 agents · synthesized · +0 models · +21 sources_

**Verifier:** STUDY-051 Verifier ✅. Scholar 8/8. Practitioner hold (A14B ≥80GB refuse; GGUF GB table unverified). Analogist 1–6 hold; #7–#8 fail-transfer omitted. A14B-32GB invent: 0. Pocket 127 stays. Extras-only.

## Wave 17 — Wave 17 — STUDY-052 3D TRELLIS/Hunyuan deepen (Hunyuan flip: 0; Pocket stays) (2026-09-07)

_3d — TRELLIS MIT vs Hunyuan Community beyond STUDY-032; Hunyuan flip: 0; no invent Hunyuan Apache; Pocket 127 stays · 3 agents · synthesized · +0 models · +22 sources_

**Verifier:** STUDY-052 Verifier ✅. Scholar 8/8. Practitioner 8/8. Analogist 1–6 hold; #7–#8 fail-transfer omitted. Hunyuan flip: 0. Pocket 127 stays. Do not invent Hunyuan Apache. Extras-only.

## Wave 18 — Wave 18 — STUDY-053 caption/VLM deepen (TTS invent: 0; JoyCaption Apache invent: 0) (2026-09-07)

_caption — deepen beyond STUDY-033; TTS invent: 0; JoyCaption Llama Community not Apache; Pocket 127 stays · 3 agents · synthesized · +0 models · +22 sources_

**Verifier:** STUDY-053 Verifier ✅. Scholar 8/8. Practitioner 8/8. Analogist 1–6 hold; #7–#8 fail-transfer omitted. TTS invent: 0. JoyCaption Apache invent: 0. Pocket 127 stays. Extras-only.
