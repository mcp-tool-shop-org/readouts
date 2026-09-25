# Wave 2 — Prompt craft: what text encoders actually read

**Date:** 2026-06-07 · **Swarms:** 3 (encoder mechanics 13 agents, negative prompts 6, seed-vs-prompt 6) · **Recipes:** 103 (102 verified) · **Sources:** 195

The lane that exists so no session — human or model — ever prose-dumps an encoder again. Born from a real failure: a hero (Kael) generated as a washed-out, faceless, generic nobody, and the operator wasted a loop tweaking tonemaps and re-rolling instead of fixing the actual cause (a prompt that fed a T5 encoder narrative prose it cannot ground). Every rule below is tagged for grounding; debunked myths are stored as `kind=anti-pattern / status=avoid` so searching the myth returns the debunk. Full encoder write-up: `E:/AI/trellis-work/encoder-prompt-craft-doctrine.md`.

## 1. Truncation — how many characters before it stops listening
| Encoder | Hard limit | Load-bearing budget | At the cutoff |
|---|---|---|---|
| **CLIP** (SDXL) | 77 tokens | **~20 effective tokens ≈ 75–90 chars** | silent tail drop; positions past ~20 barely trained (Long-CLIP arXiv:2403.15378) |
| **T5-XXL** (Chroma/FLUX-dev) | **512 ≈ ~350 words / ~1,800 chars** | first ~60% | silent truncation (schnell + Chroma **inpaint** = 256 — a footgun) |
| **Qwen-Image** (Qwen2.5-VL) | 512 default (1024 ceiling) | ~1,900 chars | silent |
| **Z-Image** (Qwen3-4B) | 512 | ~2,000 chars | silent |

**Universal: the tail is dropped — never bury the subject at the end.** (Kael ran on Chroma/T5 = 512 tokens; the ~110-word prompt was well within budget. Length was never the problem — depictability was.)

## 2. Per-encoder cheat sheet
- **CLIP/SDXL** — front-load identity in the first ~20 tokens; dialect matches the *checkpoint* (tags for Pony/Illustrious, phrases for base SDXL); `(token:1.2)` works (modest); `BREAK` isolates subjects to kill color-bleed.
- **T5/Chroma** — real grammatical sentences (T5 parses clauses + spatial relations); **periods bias realism, commas bias cartoon** on Chroma; 60–150 words of pure visual detail; **weighting syntax is dead on T5** (restate instead); Chroma's negative works, FLUX's is ignored.
- **Qwen/Z-Image** — structured paragraphs answering **color/shape/size/texture/count/spatial** (its built-in system prompt asks exactly that); one short official quality tail, don't stack; Z-Image's negative is ignored (distilled).

## 3. Depictability (the craft heart — the direct Kael fix)
- **Law 1 — concrete-visual beats abstract/narrative** [EMPIRICAL CLIP 2103.00020; Scaling-Down-Encoders 2503.19897; EmoGen 2401.04608]. Abstract tokens are *noise, not nothing*.
- **Law 2 — describe what's VISIBLE, not what's TRUE** [EMPIRICAL reporting-bias 2602.23351]. Encoders never learned causation→pixel. Ask "what would a frame-grab show?"
- **Law 3 — attention is a zero-sum budget** [EMPIRICAL attention-regulation 2403.06381]. Every backstory token starves a depictable one.
- **Worked fix:** `weary spacer worn by grief, guarded and steady` → `hollow cheeks, dark under-eye circles, three-day stubble, downturned mouth; arms crossed, chin lowered; level gaze, squared shoulders`. **Backstory stays in the bible, never in the encoder.**

## 4. Negative prompts (the gap from wave-1, now filled)
- **What it mechanically does** [EMPIRICAL Ho & Salimans 2022, arXiv:2207.12598]: a negative prompt **replaces the unconditioned branch of CFG** — generation is pushed along the vector *away from* the negative embedding, not filtered. **Duplicating a concept in both positive and negative cancels it.** Put only things genuinely absent from your positive intent (e.g. `photographic, 3d render` to defend a flat 2.5D cel look).
- **CFG scale is the negative-strength dial AND the "frying" cause** [EMPIRICAL Lin et al. 2023, arXiv:2305.08891]: large guidance weight inflates the latent's standard deviation → over-exposure / blown highlights / neon saturation. **This is a third cause of Kael's wash** (alongside AgX tonemap + TRELLIS albedo-flattening). SDXL: **CFG 4–7, start 5–6**; 9+ fries. Oversaturated output → **lower CFG first**, don't edit the prompt.
- **The fix for needed-high-CFG: RescaleCFG / guidance_rescale ~0.7** [Lin et al. 2023] — renormalizes the latent's std back down so you keep prompt adherence without the deep-fried palette (ComfyUI `RescaleCFG` node).
- **Distilled/turbo models ignore negatives** (FLUX-dev/schnell, Z-Image-Turbo, SDXL-Turbo/Lightning): CFG distilled to one pass, cfg=1 → uncond==cond → the negative term vanishes. **NAG / PAG** restore negative-like control on those.
- **Bare-concept rule:** put `blurry`, `hat` — NOT `no hat` (the field already means *away-from*).
- **Mega-block negatives are cargo cult** — a 50-tag copy-paste dilutes and truncates (77-token cap on the negative too); use a **short, targeted** negative that fixes an *observed* defect.
- **Negative-embedding textual inversions** (EasyNegative, ng_deepnegative, badhandv4…) are mostly **SD1.5-trained and don't transfer to SDXL**, and carry **unverified Civitai licenses** → commercial-unsafe. Avoid for shipped work.

## 5. Seed vs prompt (the re-roll-vs-rewrite diagnostic)
- **The seed only chooses the starting Gaussian noise; it carries no semantic content** [EMPIRICAL DDPM 2006.11239, LDM 2112.10752]. Same seed + prompt + sampler + steps + CFG = pixel-identical (full determinism).
- **Division of labor**: seed fixes **composition, pose, framing, which face-instance**; prompt fixes **what the character IS** (content, attributes, style) [EMPIRICAL "All Seeds Are Not Equal" 2411.18810].
- **THE DIAGNOSTIC (would have saved the Kael loop):** a weak/underspecified prompt regresses to the dataset mean — a generic nobody — **no matter the seed**. Re-rolling re-samples *within that generic basin* → a different generic nobody every time. **Signature of a prompt miss = "varied yet uniformly bland."** → STOP re-rolling, add load-bearing identity tokens (distinct silhouette, specific clothing/material, age, explicit pose verb, character descriptor). **Do NOT touch tonemaps/lighting/render settings to fix a content problem.**
- **When seed IS the lever:** content is right but you want a different *sample* (pose/face/framing) → re-roll, or run a batch of N seeds. **Seed-lock to A/B a prompt change** (hold seed, change one token, isolate the effect).
- **Folklore, debunked:** no universal "magic/lucky seed" (seed quality is prompt/model/resolution-conditional); a good seed **does not transfer** across models, samplers, or resolutions; a fixed seed does **NOT** give character consistency (that comes from prompt/reference/LoRA). Reproducibility needs seed **+** model + sampler + steps + CFG + resolution + graph; ancestral/SDE samplers add per-step noise and are less seed-stable.

## 6. Anti-patterns (stored as queryable `avoid` recipes)
Narrative filler · backstory/motive tokens · abstraction/emotion words · quality-tag stacking · negation in the positive · multi-subject color-bleed on CLIP · spatial logic on CLIP · tail-burial · wrong dialect per checkpoint · full-body-starves-the-face · mega-negative-blocks · SD1.5-negative-embeddings-on-SDXL · "magic seeds" · re-rolling a prompt miss.

**One line:** the encoder gives you the right *kind* of thing; the prompt's depictable tokens make it *specific*; the seed picks *which sample*; CFG controls *how hard* and *how fried*; reference-conditioning (not text, not seed) gives you the *same* character twice.
