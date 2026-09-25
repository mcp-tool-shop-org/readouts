# Diffusion Qwen Lora
_auto-created from wave lane_ · wave 16 · 2026-09-13 · [‹ catalog index](README.md)

5 techniques · 5 recommended · 5 measured-on-rig. Narrative + plan: [dispatch](../waves/wave-01-foundation/dispatch.md).

| ↓ | Technique | Method | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|-----------|--------|---------|----------|------|-----|--------|---|
| 1 | Clean (on-canon) dataset = no late embedding-cloud collapse — 3rd cross-run confirmation; pick the ship checkpoint by geometry, not CLIP-sim | evaluation | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | Qwen-Image literalizes NOUNS in style descriptors — name light by material, not object (58/58 lantern-prop rate; negatives lose) | dataset | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | Qwen-Image style-LoRA on 32GB (AI-Toolkit uint3+ARA) — MEASURED on the 5090 (the first Qwen-Image-as-base row) | lora | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | Shape-anchored img2img for silhouette-hard creature classes — the base silhouette prior overrides text even with the style LoRA loaded | dataset | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | TRELLIS turnaround fragility for winged+headed creatures — fix it at the concept stage, not with restylize denoise | dataset | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |

## Detail

### Clean (on-canon) dataset = no late embedding-cloud collapse — 3rd cross-run confirmation; pick the ship checkpoint by geometry, not CLIP-sim · `recommended` · ▣ measured
**MEASURED across three single-lever retrains on the IDENTICAL pinned recipe (only the dataset changed): a clean on-canon dataset shows NO late embedding-cloud collapse, while off-canon exemplars drive one. v1 (2 off-canon widows in one class) collapsed late (anisotropy 8.2->12.5 by step 2000 + effdim drop). v2 (re-curated) recovered. v3 (bestiary, 8 classes, every class clean): anisotropy peaks 13.27@1500 then RECOVERS to 11.55@2000, effdim steady ~6.9, loss monotone to 0.096. Ship checkpoint selected by CMMD + embedding-cloud geometry = 1750 @1.5 (NOT step-2000; raw CLIP-sim alone shipped the v1 overfit). Per-class A/B (SigLIP2 external verifier + full looked-at pass): new classes on-canon under bare trigger, OLD classes hold (widow faceless / hound / tithe), no-trigger gating stays photoreal with the LoRA loaded.**
The cross-run hypothesis from wave-08 (off-canon exemplars drive late collapse) now has a third data point, and the first at multi-class scale (8 classes, 99 records). vector-caliper baseline #3 archives the trajectory. The practical rule is checkpoint-selection discipline: geometry (effdim/anisotropy) + distribution (CMMD) + eyes, never similarity alone.
- **For the pipeline:** Keep the recipe pinned and treat the dataset as the single lever between LoRA versions — it makes trajectory differences attributable. Capture per-checkpoint embedding-cloud geometry every run and pick the ship checkpoint by CMMD + geometry + looked-at. A clean dataset is also a training-stability lever, not only a quality lever.
- **Method:** evaluation · **Applies to:** diffusion · **Base:** Qwen-Image · **Kind:** finding
- **Seed:** pinned recipe · **Runs:** 3 · **Tuning budget:** checkpoint trajectory captured per run (8 points); no extra tuning · **Search:** single pinned recipe; checkpoint chosen post-hoc by CMMD + cloud geometry + looked-at
- **Variance:** Three within-recipe runs (v1/v2/v3), 8 checkpoints each; the collapse/no-collapse outcome is qualitative and consistent (1 collapse with off-canon data, 2 clean without).
- **Validated under:** RTX 5090 32GB; AI-Toolkit uint3+ARA + qfloat8-TE; dataset_tallow_fen_v3 (80 train); CLIP ViT-B/32 cloud metrics; 2026-06-17.
- **Base model (model-knowledge):** `qwen-image`
- **Builds on (stage ?):** Qwen-Image style-LoRA on 32GB (AI-Toolkit uint3+ARA) — MEASURED on the 5090 (the first Qwen-Image-as-base row)
- **Output license:** commercial **yes** — Method finding; base-agnostic.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| ship_checkpoint | 1750 of 2000 | ○ | CMMD-min 0.0963 + healthy geometry; aniso recovers after a 1500 peak |
| selection_metric | CMMD + embedding-cloud geometry + looked-at | ● | never CLIP-sim alone (the step-2000 trap) |
| single_lever | dataset only; recipe byte-identical to v1/v2 | ● |  |

- **Datasets:** Tallow Fen bestiary v3 package (tp-20260617-132101-7bba) (training, license studio-owned synthetic; Apache-2.0 generating base)

**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| diffusion-style | CMMD + embedding-cloud geometry per checkpoint | aniso 10.1->12.5->...->13.27@1500->11.55@2000; effdim steady ~6.6-7.1; ship 1750 | min CMMD + geometry health | ✓ | clip-vit-b32 |
| diffusion-canon | SigLIP2 contrastive canon probes + looked-at A/B | Pall/Brood clean bare-trigger; old classes hold; gating clean | per-class majority + eyes | ✓ | siglip2-so400m |

- **Best for:** LoRA checkpoint selection + training-stability via dataset hygiene (checkpoint-selection, fit 5)
- **Verify:** verdict=confirmed | currency=measured 2026-06-17 | 3rd within-recipe run; v3 aniso recovers 13.27@1500->11.55@2000, effdim steady; ship 1750 by CMMD+geometry; vector-caliper baseline #3
- **Sources:** [vector-caliper baselines v1/v2/v3 (cross-run trajectory)](https://github.com/mcp-tool-shop-org/tool-shop-studio) (studio (rig-measured), 2026) — 3-run trajectory: 1 late collapse (off-canon) vs 2 clean

### Qwen-Image literalizes NOUNS in style descriptors — name light by material, not object (58/58 lantern-prop rate; negatives lose) · `recommended` · ▣ measured
**MEASURED across two full neutral-object waves (2026-06-09): the style descriptor phrase 'a single warm lantern light in cold fen gloom' produced a physical lantern PROP in 58/58 neutral-object images, INCLUDING a 28/28 wave with 'lantern, oil lamp, candle, lamp, torch, light fixture' in the negative prompt — on Qwen-Image, negative prompts cannot beat a noun in the positive style descriptor. Rewording the light source by MATERIAL ('one warm tallow light in cold sunless gloom', the canon lighting clause verbatim) eliminated the prop in the next 28-image wave while preserving the chiaroscuro: the warm light re-rendered as material glow (inside a cracked pot, embers, backlight) instead of a repeated object.**
Found while building a style-on-neutral-subjects LoRA dataset: a 100%-correlated prop across the dataset would leak into the style trigger regardless of caption attribution, so the prop had to go at generation time. Wave 3 (no anti-lantern negative): 30/30 lanterns. Wave 3b (strong anti-lantern negatives): 28/28 lanterns. Wave 3c (descriptor reworded to material): 0/28 lantern objects; small varied flames/glows remained and were captioned per-image as content.
- **For the pipeline:** When authoring style descriptors for Qwen-Image dataset waves, audit every concrete NOUN — each is a latent prop. Name light sources by material/quality ('warm tallow light', 'cold grey daylight'), not by emitting object. Do not rely on negative prompts to suppress a noun the positive prompt asserts. This is dataset-craft canon for every sdlab project generating on the Qwen base.
- **Method:** dataset · **Applies to:** diffusion · **Base:** Qwen-Image · **Kind:** failure-fix
- **Runs:** 3
- **Variance:** Three 28-30 image waves, fixed seeds per wave; the effect was 100%-of-wave in both failing configurations and 0%-of-wave after the fix — no statistics needed.
- **Validated under:** Qwen-Image fp8 native graph, cfg 3.5, euler/simple, 22 steps, 1024px; sdlab generate; RTX 5090; 2026-06-09.
- **Base model (model-knowledge):** `qwen-image`
- **Output license:** commercial **yes** — Prompt-craft finding; base-agnostic license-wise.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| failing_phrase | a single warm lantern light in cold fen gloom | ○ | lantern prop in 58/58 across waves 3+3b |
| fixed_phrase | one warm tallow light in cold sunless gloom | ○ | 0/28 lantern objects in wave 3c; lighting intent preserved |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| a style-descriptor noun materializes as a physical object in ~100% of generations | Qwen-Image's strong prompt adherence treats every concrete noun as depictable content; negatives cannot override the positive assertion | reword the descriptor to name the QUALITY/MATERIAL instead of the object | style_prefix |

- **Best for:** style-descriptor authoring for Qwen-base dataset waves (dataset-craft, fit 5)
- **Verify:** verdict=confirmed | currency=measured 2026-06-09 | three-wave A/B/B' with 86 looked-at images; binary outcome per wave
- **Sources:** [tallow-fen waves 3/3b/3c (prompt packs + 86 looked-at images + curation records)](https://github.com/mcp-tool-shop-org/style-dataset-lab/pull/25) (studio (rig-measured), 2026) — 30/30 and 28/28 lantern props pre-fix; 0/28 post-fix

### Qwen-Image style-LoRA on 32GB (AI-Toolkit uint3+ARA) — MEASURED on the 5090 (the first Qwen-Image-as-base row) · `recommended` · ▣ measured
**MEASURED end-to-end on the 5090 (tallow_fen_style_v1, 2026-06-09): a rank-16 style LoRA on the 20B Qwen-Image DiT trains in ~2h10m at 3.6-4.7 s/it and ~18GB peak VRAM using Ostris AI-Toolkit with uint3+ARA transformer quantization (ostris's own 'required for 32GB'), TE qfloat8, low_vram, cache_text_embeddings + cache_latents_to_disk, adamw8bit lr 1e-4, 2000 steps. The resulting LoRA loads NATIVELY in ComfyUI LoraLoaderModelOnly (no key conversion). Trigger-only prompts carry the trained style to unseen subjects; the no-trigger gating probe stayed photoreal through all 2000 steps. Best checkpoint was 1250 of 2000 — step 2000 had the HIGHEST CLIP-sim (0.7937) but with embedding-cloud anisotropy spiking 8.2->12.5 and effective dimension collapsing 7.0->6.76: overfit masquerading as improvement, visible to eyes as monochrome drift on neutral subjects. CMMD minimum (0.1351) and looked-at agreed on 1250. ComfyUI inference strength sweep: 1.0 visibly weaker than the training sampler, 1.5 = dataset look, 1.75 = content bleed (fen moss on neutral objects).**
Dataset = sdlab style-on-neutral-subjects package (44 train images: 24 creatures + lantern-free neutral objects + lantern-as-subject keepers), captions 'trigger, a concept, <content-only prose>' with the trigger IN the caption text because cache_text_embeddings locks captions at cache time (trigger_word injection does not work with cached embeddings). Base = Qwen/Qwen-Image HF snapshot 75e0b4be (full bf16 repo, ~54GB; the ARA is calibrated against original weights so the on-rig ComfyUI fp8 single-file was NOT used as the training base). Per-checkpoint eval: fixed 12-prompt grid x 8 checkpoints, CLIP ViT-B/32 cloud measured (sim-to-curated-centroid, CMMD, spread/anisotropy/effective-dimension). Run config pinned at E:/AI/training/tallow_fen_style_v1.yaml; dataset pkg tp-20260609-201716-4744; trajectory series archived in vector-caliper/baselines/.
- **For the pipeline:** Qwen-Image is now a practical 32GB style-LoRA base: use the ostris 24gb example as the recipe spine (uint3+ARA is mandatory; qfloat8-TE; low_vram), rank 16 transfers from the DiT guidance, and budget checkpoint selection by distribution + GEOMETRY metrics plus eyes — never by similarity alone (the step-2000 trap). Plan inference strength ~1.5 in ComfyUI (mirrors the Chroma precedent where ComfyUI strength ran hotter than the training sampler). Keep ALL intermediate checkpoints (peak was at 62% of the run).
- **Method:** lora · **Applies to:** diffusion · **Base:** Qwen-Image · **Kind:** recipe
- **Seed:** 42 · **Runs:** 1 · **Tuning budget:** 1 training run + 4-point inference strength sweep + 8-checkpoint eval grids (96 images) · **Search:** pinned single recipe; checkpoint + strength selected post-hoc by CMMD + cloud geometry + looked-at
- **Variance:** Single 2000-step run; the checkpoint trajectory (8 points) is within-run. Strength sweep n=2 subjects x 4 strengths, looked-at. A/B vs no-LoRA baseline n=24 per arm (same seeds), CLIP-sim/CMMD + SigLIP2 contrastive probes + full looked-at pass.
- **Validated under:** RTX 5090 32GB native Windows; AI-Toolkit (April-2026 clone) venv torch 2.9.1+cu128; Qwen/Qwen-Image bf16 + uint3|ARA + qfloat8 TE; 44-image dataset @ 512/768/1024 bucketing; watchdog 31200MiB/87C active throughout; 2026-06-09.
- **Base model (model-knowledge):** `qwen-image`
- **Output license:** commercial **yes** — Qwen-Image is Apache-2.0; the LoRA inherits it. Output commercial-clean given a clean dataset (this one is studio-synthetic from canon).
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| quantization | uint3/ostris/accuracy_recovery_adapters/qwen_image_torchao_uint3.safetensors | ● | ostris: 3-bit+ARA required for 32GB-class cards on the 20B; ARA is calibrated for ORIGINAL weights — train from the HF repo, not a pre-quantized fp8 single-file |
| qtype_te | qfloat8 | ● |  |
| low_vram_plus_caching | low_vram + cache_text_embeddings + cache_latents_to_disk | ● | cached TE means trigger_word injection is a no-op — put the trigger in the caption text |
| rank_alpha | 16/16 | ○ | DiT style-LoRA floor per the Chroma/klein guidance; adapter = 295MB on the 20B |
| throughput | 3.6-4.7 s/it, ~18GB peak, ~2h10m / 2000 steps | ○ | sampling adds ~5min per 4-prompt grid every 250 steps |
| best_checkpoint | 1250 of 2000 | ○ | CMMD min 0.1351 + healthy geometry; step-2000 sim-uptick was cloud-collapse overfit |
| comfyui_strength | 1.5 | ○ | sweep: 1.0 weak / 1.5 dataset-look / 1.75 content bleed; loads natively in LoraLoaderModelOnly |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| trainer crashes at import: torchaudio _torchaudio.pyd 'specified procedure could not be found' | requirements resolve pulled torchaudio 2.11 against torch 2.9.1; config_modules.py imports torchaudio unconditionally | pin torchaudio==torch minor (2.9.1+cu128) | torchaudio |
| later checkpoints' eval grids silently identical to the first checkpoint | ComfyUI caches LoRA-patched models keyed on the lora_name STRING and does not re-read a same-named file whose bytes changed | unique lora filename per checkpoint; budget VRAM for the accumulated patched-model caches (8 cached LoRAs + a fresh load tripped a 31.2GB watchdog) | lora_name |
| ComfyUI killed mid-pipeline by the VRAM/RAM watchdog during or after training | trainer load spikes system RAM >=90%; separately, ollama-intern prewarms hermes3:8b with keep_alive=-1 (5GB resident forever) which collides with ComfyUI's 20B under a 31.2GB ceiling | stop ComfyUI before training; `ollama stop <model>` before any image-gen/training block; restart ComfyUI after | vram_budget |
| one creature class regresses to an off-canon mode under trigger prompts (skull faces on a canonically faceless creature, 6/8) | 2 off-canon exemplars in an 8-image class (25% of the class mode) + the base model's strong prior for that mode; accurate captions and prompt negatives do NOT contain it at inference | per-creature canon needs DATASET-level enforcement: curate the off-canon exemplars out and outnumber the prior with on-canon ones. MEASURED v2 outcome (2026-06-10, single-lever retrain, 2 skull exemplars out / 5 faceless in): trigger-prompt faceless rate 2/8 -> 6/8 by eyes (5/8 by SigLIP2 probe — one marginal disagreement where the probe text is confounded by the skeletal body), remaining misses concentrated on the seeds that produced the original off-canon exemplars. BONUS: the v2 trajectory shows NO late cloud-collapse (v1 aniso 8.2->12.5 by 2000; v2 recovers to 8.1 with CMMD min 0.1333 AT 2000) — hypothesis: off-canon exemplars drove v1's late collapse. v2 ship ckpt = 1500 @ strength 1.5. | dataset_curation |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| diffusion-style | CLIP-sim-to-curated-centroid (ViT-B/32) | arm A baseline 0.9055 (inflated: members of the centroid) / arm B descriptor+LoRA 0.8925 / arm C trigger-only 0.8686; n=24 per arm | directional only — arm A is structurally inflated | ✓ | clip-vit-b32 |
| diffusion-style | CMMD vs curated set | min 0.1351 @ step 1250; 0.1431 @ 2000 with anisotropy 12.5 | min over checkpoints | ✓ | clip-vit-b32 |
| diffusion-canon | SigLIP2 contrastive canon probes (good-vs-bad description) | hound 8/8, bog-tithe 8/8 canon-correct both arms; widow 2/8 (the diagnosed regression) | per-class majority | ✓ | siglip2-so400m |

- **Best for:** commercial-safe studio style LoRA on a 32GB card (20B-class DiT base) (style-lora, fit 5) ; trigger-carried house style for unseen subjects (props/locations/creatures) (style-transfer, fit 5)
- **Verify:** verdict=confirmed | currency=measured 2026-06-09 | oracle = rig + harness + full looked-at pass; v2 retrain MEASURED 2026-06-10: dataset-level canon enforcement confirmed (widow 2/8 -> 6/8 eyes, 5/8 SigLIP2; no late trajectory collapse; ship ckpt 1500 @ 1.5)
- **Sources:** [tallow_fen_style_v1 pinned run (config + log + 8 checkpoints + A/B + trajectory)](https://github.com/mcp-tool-shop-org/style-dataset-lab/pull/25) (studio (rig-measured), 2026) — full measured run: 3.6-4.7 s/it, ~18GB, ckpt-1250 ship, strength 1.5, gating clean ; [ai-toolkit train_lora_qwen_image_24gb.yaml + qwen_image arch (uint3+ARA example)](https://github.com/ostris/ai-toolkit) (ostris, 2026) — uint3+ARA quantization is the blessed 24-32GB fit for Qwen-Image LoRA training ; [studio sprite pipeline runbook (Phase-1 results section)](https://github.com/mcp-tool-shop-org/tool-shop-studio) (studio, 2026) — ops gotchas + earned rules recorded same-day

### Shape-anchored img2img for silhouette-hard creature classes — the base silhouette prior overrides text even with the style LoRA loaded · `recommended` · ▣ measured
**MEASURED on the 5090 (tallow_fen_style_v3 bestiary build + production, 2026-06-17): for creature classes whose canonical silhouette has NO limbs/head/face, Qwen-Image's base silhouette prior overrides the positive text prompt EVEN WITH the trained style LoRA at strength 1.5 — bare txt2img grows limbs/snouts/skulls. Rust Boil (a limbless swollen dome) scored 0/24 on-canon across txt2img attempts; Mire Maw (a leaning cone) 2/32; Peat Dredge grew a front snout/trunk. FIX = shape-anchored img2img: build a crude PIL silhouette mock from master-palette colour blocks, then run it through NO-LoRA Qwen img2img at denoise 0.6-0.75; the mock imposes the silhouette txt2img cannot hold (Boil geometry 8/8 at d0.6-0.7 after 24 txt2img failures / 6 distinct face-and-limb attractors). The SAME three classes that needed i2i to build the dataset need i2i (or low inference strength) to PRODUCE: the LoRA supplies correct material/surface/painterly style, but the base prior wins on gross shape. The face prior is hydraulic — it erupts at focal points, crowns, and dark-water reflections; give it no dark void to colonize.**
Discovered while filling dataset v3's new classes and confirmed again at production/turnaround time. Silhouette-hard = the canonical form lacks the anatomy the base model expects (no limbs / no head / no face). The fix is geometry-first: a denoise-0.6-0.75 img2img pass over a flat colour-block mock anchors the outline, then the LoRA (or a later restylize pass) paints the surface. Classifies the bestiary into two production lanes: silhouette-easy (Pall/Brood/old classes = bare-trigger txt2img @1.5) and silhouette-hard (Boil/Dredge/Maw = shape-anchored i2i / turnaround).
- **For the pipeline:** Before generating a new creature class, predict whether its silhouette is 'hard' (limbless/headless/faceless). If so, do NOT budget bare txt2img — author a PIL silhouette mock and run shape-anchored img2img (denoise 0.6-0.75, no-LoRA for the anchor, then restylize). Route silhouette-hard classes to the i2i/turnaround production lane permanently. Never name a creature feature that is itself a strong base-prior attractor (a named jaw/face) in a positive prompt — it polymorphizes the whole body.
- **Method:** dataset · **Applies to:** diffusion · **Base:** Qwen-Image · **Kind:** failure-fix
- **Seed:** varied per wave · **Runs:** 1 · **Tuning budget:** per silhouette-hard class: 1 PIL mock (1-3 revisions) + a denoise x seed i2i sweep (~8-24 images), looked-at · **Search:** PIL silhouette mock -> no-LoRA Qwen img2img denoise/seed sweep -> looked-at + SigLIP2 canon probe; reroll on attractor eruption
- **Variance:** Boil: 24 txt2img failures then 8/8 i2i geometry across a denoise(0.6-0.78) x seed sweep, all looked-at. Maw: 2/32 txt2img then closed via mock-v3 (textured cone + sparse broken-snag crown). Single dataset+production run; the per-class counts are within-run, every image opened.
- **Validated under:** RTX 5090 32GB; Qwen-Image fp8 native graph (UNETLoader qwen_image_fp8 + qwen_2.5_vl_7b TE + ModelSamplingAuraFlow shift 3.1), euler/simple 22 steps cfg 3.5 1024px; tallow_fen_style_v3 @1.5 for production, no-LoRA for the dataset anchor; 2026-06-17.
- **Base model (model-knowledge):** `qwen-image`
- **Builds on (stage ?):** Qwen-Image style-LoRA on 32GB (AI-Toolkit uint3+ARA) — MEASURED on the 5090 (the first Qwen-Image-as-base row)
- **Output license:** commercial **yes** — Studio-synthetic from authored canon; Qwen-Image Apache-2.0.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| anchor_denoise | 0.6-0.75 | ● | no-LoRA img2img over the PIL mock; below ~0.55 the mock colours show through, above ~0.8 the base prior re-grows anatomy |
| mock_construction | flat master-palette colour blocks (PIL) | ● | Maw needed a TEXTURED cone + SPARSE broken-snag crown; a dense crown / heavy tangle re-admits apex faces |
| production_lane | i2i / turnaround for silhouette-hard classes | ○ | Boil/Dredge/Maw; Pall/Brood/old classes stay bare-trigger txt2img @1.5 |

- **Datasets:** Tallow Fen bestiary v3 package (tp-20260617-132101-7bba) (training, license studio-owned synthetic; Apache-2.0 generating base)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| a limbless/headless/faceless creature grows limbs, a snout, or a skull under bare txt2img even with the style LoRA at 1.5 | the base diffusion silhouette/anatomy prior is stronger than the positive prompt for out-of-distribution body plans; the style LoRA changes surface, not gross shape | shape-anchored img2img over a PIL silhouette mock (denoise 0.6-0.75); route the class to the i2i/turnaround lane | production_lane |
| faces erupt specifically at crowns, focal points, and dark-water reflections | the face prior is hydraulic — it fills high-salience voids | give the composition no dark focal void; sparse crowns over dense; reroll on eruption | composition |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| diffusion-canon | SigLIP2 contrastive canon probes (good-vs-Forbidden-line) | Boil/Maw drift caught on the face/limb axis; i2i-anchored outputs pass; verifier confirmed by looked-at | per-class majority | ✓ | siglip2-so400m |

- **Best for:** generating limbless/headless/faceless creature classes on a strong-prior base (shape-control, fit 5)
- **Verify:** verdict=confirmed | currency=measured 2026-06-17 | oracle = rig + SigLIP2 probes + full looked-at; Boil 0/24 txt2img -> 8/8 i2i; same 3 classes need i2i to dataset AND to produce
- **Sources:** [tallow-fen bestiary v3 dataset + shape-anchor i2i waves (mocks + sweeps + records)](https://github.com/mcp-tool-shop-org/style-dataset-lab/pull/27) (studio (rig-measured), 2026) — Boil 0/24 txt2img -> 8/8 i2i geometry; Maw closed via sparse-crown mock

### TRELLIS turnaround fragility for winged+headed creatures — fix it at the concept stage, not with restylize denoise · `recommended` · ▣ measured
**MEASURED on the 5090 (Fen Pall turnaround, 2026-06-17): a winged+headed creature whose concept shows thin wings on bone struts produces a strutty, skull-prone TRELLIS.2 mesh — its side/rear 8-direction views erupt into skull / exposed-ribcage / gargoyle-face under the restylize img2img pass (denoise 0.55), even with the v3 LoRA. SigLIP2 scored the stylized-skull frames HIGHEST (a stylized skull matches the concept's palette/style), so the external verifier under-penalizes a face on an otherwise-correct silhouette — the human looked-at pass carried the canon-veto. Low-denoise reroll could NOT repair it (the drift is mesh-level geometry, not restylize freedom). The fix is upstream at the CONCEPT stage: generate the turnaround concept with a fuller CONTINUOUS amber membrane (bone struts hidden beneath it) + a large round featureless head-bulb + the drift attractors (skull, face, eye sockets, skeleton, exposed ribs, spindly limbs, clawed hands) in the concept-stage NEGATIVE. Two concepts were meshed: a fuller-continuous-membrane one (won, 8/8 clean — featureless head holds on every angle) and a folded/perched-pose one (rejected — meshed solid but over-corrected, losing the winged identity to a hooded mossy blob whose rear view degenerated to a mossy cairn).**
Generalizes the shape-control finding into 3D: for the mesh-turnaround lane, the silhouette must be solved in the CONCEPT before TRELLIS, because no downstream restylize denoise repairs mesh-level geometry. Limbless/heap forms (Rust Boil dome, Wick Brood fused heap) turned around clean with no special handling (Boil 8/8 — a limbless dome carried clean through mesh into 3D; Brood 8/8 after rerolling 2 single-organism drifts). The winged+headed form is the fragile case and the one that needs the concept-stage discipline.
- **For the pipeline:** For TRELLIS turnarounds of winged/limbed/headed creatures, author the concept for a SOLID, continuous silhouette (membranes filled, struts hidden, head round and featureless) and put the base-prior attractors in the concept-stage negative. Do NOT use a folded/perched pose to force solidity — it kills the creature's identity. Trust eyes over SigLIP2 for focal-feature (face/skull) drift; SigLIP2 weights global palette and will rank a stylized skull high.
- **Method:** dataset · **Applies to:** diffusion · **Base:** Qwen-Image · **Kind:** failure-fix
- **Seed:** 8850-8855 (concept pool); 7000-7001 (reroll) · **Runs:** 1 · **Tuning budget:** 1 concept pool (6) + 2 TRELLIS meshes + 2 restylize sets + targeted low-denoise rerolls; ~1 GPU hour · **Search:** concept pool with attractors negated -> TRELLIS.2 mesh -> 8-dir -> Qwen restylize @1.5 -> SigLIP2 gate + looked-at -> low-denoise reroll on weak frames -> contact sheet
- **Variance:** Pall: original turnaround ~5/8 with skull drift on left/front_right/back_left; concept-stage re-mesh of 2 of 6 candidates -> winner 8/8, looser folded candidate rejected. Brood 8/8 (2 rerolls), Boil 8/8 (3 rerolls). Every frame and every reroll candidate looked-at.
- **Validated under:** RTX 5090 32GB; TRELLIS.2-4B (trellis2-env), ptype 1024_cascade; Qwen-Image restylize + tallow_fen_style_v3 @1.5, denoise 0.55 (reroll 0.38-0.54); SigLIP2-so400m gate; 2026-06-17.
- **Base model (model-knowledge):** `qwen-image`
- **Output license:** commercial **yes** — TRELLIS.2 MIT; Qwen Apache-2.0.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| concept_membrane | thick CONTINUOUS membrane, struts hidden | ● | thin wings-on-struts -> strutty skeletal mesh from side/rear |
| concept_negative | skull, face, eyes, eye sockets, skeleton, exposed ribs, spindly limbs, clawed hands | ● | kill the base-prior attractors at the concept stage so the MESH INPUT is clean |
| pose | natural solid pose, NOT folded/perched | ○ | a folded pose over-corrects and kills the winged identity |
| restylize_denoise | 0.55 (reroll 0.38-0.46 to suppress prior) | ○ | cannot fix mesh-level geometry; only surface |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| side/rear turnaround frames of a winged+headed creature show a skull, exposed ribcage, or gargoyle face | thin wings-on-bone-struts concept -> strutty skull-prone TRELLIS mesh; restylize re-grows anatomy in the ambiguous side/rear silhouette | re-mesh from a concept with a fuller continuous membrane + round featureless head + attractors in the concept-stage negative | concept |
| SigLIP2 ranks a stylized-skull frame higher than an under-stylized correct frame | the embedding weights global palette/style; a stylized skull matches the concept, a local face drift is under-penalized | gate picks, EYES confirm; the human looked-at pass holds the canon-veto on focal-feature drift | verifier |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| diffusion-canon | SigLIP2 cross-view similarity vs concept + full looked-at | Pall re-mesh v4 mean 0.905 (no false-high skull outliers after eyes cleared drift); Brood/Boil 8/8 | per-frame eyes + SigLIP corroboration | ✓ | siglip2-so400m |

- **Best for:** TRELLIS mesh turnarounds of winged/limbed/headed creatures (turnaround, fit 5)
- **Verify:** verdict=confirmed | currency=measured 2026-06-17 | Pall re-mesh -> 8/8; folded-pose candidate rejected; Brood/Boil 8/8; SigLIP2 under-penalizes face-on-correct-silhouette (eyes carry the veto)
- **Sources:** [tallow-fen v3 turnarounds (concepts + meshes + restylize + reroll + contact sheets)](https://github.com/mcp-tool-shop-org/tool-shop-studio) (studio (rig-measured), 2026) — Pall 8/8 after concept-stage re-mesh; Brood 8/8; Boil 8/8 limbless dome into 3D

