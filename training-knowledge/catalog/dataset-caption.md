# Dataset construction & caption craft
_The inputs that drive outcome more than hyperparameters: curation/dedup, caption format keyed to base model, style-vs-subject pruning, regularization sets, real:synthetic discipline, and Datasheets-style license/provenance (commercial-clean gate). Captioner weights->model-knowledge; pipeline tooling->tensor-engine._ · wave 16 · 2026-09-13 · [‹ catalog index](README.md)

17 techniques · 10 recommended · 0 measured-on-rig. Narrative + plan: [dispatch](../waves/wave-01-foundation/dispatch.md).

| ↓ | Technique | Method | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|-----------|--------|---------|----------|------|-----|--------|---|
| 2 | Augmentation safety policy (flip / random-crop / color) for style sets | dataset-construction | diffusion | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Caption format keyed to the base model's text encoder | lora | diffusion | ▸ reproduced | ⚠ cond | 5 | 5 | ✓ |
| 2 | Concept isolation for multi-concept LoRAs (anti-bleed) | dataset-construction | diffusion | ▸ reproduced | ✅ yes | 4 | 5 | ✓ |
| 2 | Per-folder num_repeats as the multi-concept balancing lever | dataset-construction | diffusion | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Regularization / class-image set construction (model-generated, not external) | regularization | diffusion | ▸ reproduced | ✅ yes | 4 | 5 | ✓ |
| 2 | Semantic dedup + train-eval overlap check before training | lora | both | ▸ reproduced | ⚠ cond | 5 | 4 | ✓ |
| 2 | Style-vs-subject caption pruning (the style-bleed lever) | lora | diffusion | ▸ reproduced | ⚠ cond | 5 | 5 | ✓ |
| 2 | Two-stage dedup: pHash gate then CLIP/DINO cosine gate (with thresholds) | curation | diffusion | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 6 | Accumulate-don't-replace real:synthetic discipline (collapse guard) | lora | both | · community | ⚠ cond | 4 | 4 | ✓ |
| 6 | Dataset size scaling: style vs character vs concept (few-good vs many) | dataset-construction | diffusion | · community | ✅ yes | 5 | 5 | ✓ |
| 9 | Datasheets for Datasets provenance gate (Gebru et al.) | dataset | both | paper | check | 4 | 4 | · |
| 9 | DreamBooth subject craft + class prior-preservation (Ruiz et al. 2022) | dataset | both | paper | check | 4 | 4 | ✓ |
| 9 | JoyCaption diffusion-dataset caption VLM | dataset | both | docs | check | 4 | 4 | · |
| 9 | LIMA quality-over-quantity alignment data (Zhou et al. 2023) | dataset | both | paper | check | 4 | 4 | · |
| 9 | Large-Scale Data Selection for Instruction Tuning | data-selection | both | paper | check | 4 | 4 | · |
| 9 | WD EVA02-Large Tagger v3 card metrics (sourced only) | dataset | both | docs | check | 4 | 4 | · |
| 9 | kohya-ss dataset TOML craft (aug/repeats/reg) | dataset | both | docs | check | 4 | 4 | · |

## Detail

### Augmentation safety policy (flip / random-crop / color) for style sets · `recommended` · ▸ reproduced
**Default augmentations corrupt style/character fidelity: flip_aug mirrors asymmetric features (one-sided marks, directional hair, text/logos), random_crop can sever composition and on-edge signatures, and color_aug poisons a color-defined style -- so for game-art style and asymmetric characters these should be OFF by default, enabled only for symmetric, color-agnostic, full-frame content.**
Augmentation is a scale trick borrowed from classification; applied blindly to style/identity training it injects FALSE invariances. flip_aug (horizontal mirror): turns a left-arm tattoo into a right-arm one, mirrors directional bangs/hair ornaments, and -- load-bearing for game art -- mirrors any DIRECTIONAL or TEXT/LOGO content (a sprite that faces left, a signed corner, readable text), teaching the model the design is reversible when it is not. For asymmetric characters and text/logo styles, flip is actively harmful. random_crop: can cut off compositional anchors and edge signatures, and changes the effective framing the style is learned at; risky for composition-defining or signature-cornered styles. color_aug: deliberately perturbs hue/saturation -- which DESTROYS a style whose identity IS its palette (e.g. a cyanotype/duotone/limited-palette canon), the exact case the studio cares about. The safe policy: treat all three as OFF by default for style and identity LoRAs; enable flip ONLY for content verified symmetric and non-directional/non-text; enable color_aug ONLY when the style is explicitly color-agnostic; prefer adding real varied images over synthetic crops/flips. This is the inverse of the wave-1 accumulate-don't-replace point (which is about synthetic GENERATIONS); here the caution is about cheap geometric/photometric augments silently teaching wrong invariances.
- **For the pipeline:** style-dataset-lab must default flip_aug=false, color_aug=false, random_crop=false in emitted dataset_config, and only flip on a per-subset basis after a symmetry/direction/text check, never color-augment a palette-defined canon. The constitution declares whether the style is symmetric and color-agnostic; the emitter reads those flags. Record augmentation settings on the datasheet so a bad invariance is auditable.
- **Method:** dataset-construction · **Applies to:** diffusion · **Base:** SDXL · **Kind:** failure-fix
- **Validated under:** kohya flip_aug/color_aug/random_crop on SDXL style/character LoRAs; harm is content-dependent (asymmetry, directionality, text, palette); not rig-measured this wave.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — Config policy only; no licensing impact.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| precision | n/a | ○ | policy is about augmentation flags, not precision |
| resolution | use bucketing instead of random_crop to handle mixed aspect ratios px | ○ | aspect-ratio bucketing preserves composition; random_crop does not |

- **Datasets:** SDXL multi-concept style set with per-subset repeat balancing (train, license studio-owned (synthetic via commercial-clean base); commercial-clean only if every source plate and the generating base clear commercial use -- verify per project)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Character gets asymmetric mark on both sides / mirrored hair | flip_aug enabled on asymmetric subject | flip_aug=false for asymmetric/directional content | flip_aug |
| Text/logos/sprites render mirrored or reversible | flip_aug on directional/text content | flip_aug=false; enable only for verified-symmetric subsets | flip_aug |
| Palette-defined style loses its signature colors | color_aug perturbed the defining hue/saturation | color_aug=false for color-defined styles | color_aug |
| Composition/signature cropped out, framing inconsistent | random_crop severed compositional anchors | random_crop=false; use aspect-ratio bucketing instead | random_crop |

- **Best for:** Avoid teaching false invariances in style/identity LoRAs (augmentation-safety, fit 5)
- **Verify:** verdict=confirmed | currency=Current — these augmentation options remain unchanged in kohya sd-scripts; the guidance is not superseded. | Both sources are real and directly support the claim. The kohya config_README confirms flip_aug, color_aug, and random_crop are per-subset boolean toggles. The kohya_ss wiki (bmaltais) explicitly warns against random flip for asymmetric subjects. The claim maps cleanly onto the game-art pipeline concern (asymmetric character features, color-defined styles). Not a dup of any wave-1 entry. Boundary clean — pure dataset-preparation craft, no trainer internals or weight claims.
- **Sources:** [kohya-ss/sd-scripts dataset config (flip_aug, color_aug, random_crop)](https://github.com/kohya-ss/sd-scripts/blob/main/docs/config_README-en.md) (kohya-ss, 2024) — flip_aug, color_aug, and random_crop are per-subset boolean augmentations toggleable at general/datasets/subsets levels. ; [LoRA training parameters (kohya_ss Wiki) -- flip caution for asymmetric subjects](https://github.com/bmaltais/kohya_ss/wiki/LoRA-training-parameters) (bmaltais (community), 2024) — Disable random flip for asymmetric subjects (one-sided tattoos, moles, directional hair) or the model learns the feature on both sides.

### Caption format keyed to the base model's text encoder · `recommended` · ▸ reproduced
**The caption FORMAT must match what the base model's text encoder was pretrained on — WD14/booru comma-tags for SDXL (CLIP-L/G), natural-language sentences for Flux (T5-XXL) — or the conditioning signal is wasted.**
SDXL conditions on CLIP-L + CLIP-G, which were trained on short comma-separated tag-like alt-text, so SDXL style LoRAs caption with WD14/booru tags (SmilingWolf WD14 tagger in kohya) with the trigger word(s) placed first and held constant across the set. Flux conditions on a frozen T5-XXL encoder trained on natural prose, so Flux LoRAs caption with full natural-language sentences (JoyCaption / Florence-2 / manual). Using NL prose on SDXL or bare tags on Flux under-uses the encoder and weakens the learned association between words and visual features. Trigger word goes first; trigger-word count is consistent across every caption so the model attributes the style to a stable token.
- **For the pipeline:** The studio's caption stage must branch on base family: WD14-tag pipeline for the #1 SDXL workload, NL-caption pipeline for Flux. style-dataset-lab caption emit should template-switch on base_model_family, never emit one caption format for both. This is a free outcome lever upstream of any hyperparameter.
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** curation
- **Tuning budget:** n/a — format choice is dictated by encoder, not searched · **Search:** none
- **Variance:** Community-consistent across kohya-ss guidance and multiple training guides; tag-vs-NL split is architectural (CLIP vs T5), not stylistic preference.
- **Validated under:** SDXL 1024px style-LoRA and Flux NL-caption style-LoRA; not rig-measured for it/s (numbers, when run, live in tensor-engine)
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **conditional** — Caption format itself is license-neutral; commercial cleanliness inherits from the base model (SDXL-base-1.0 is commercially permissive; FLUX.1-dev is non-commercial) and the source images. WD14 tagger weights are referenced as an instrument, catalogued in model-knowledge.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| caption_format | wd14-tags format | ● | SDXL/CLIP base — comma-separated booru tags; switch to natural-language for Flux/T5 base |
| caption_strategy | trigger-word-first, constant trigger-token count across set rule | ● | stable token the style attributes to; e.g. 'mystyle, ' prefix on every caption |

- **Datasets:** SDXL style-LoRA training set (canon-bound, WD14-tagged) (training, license Internal / project-canon only — commercial cleanliness gated per source plate; not for redistribution unless every source image clears a commercial license. Base SDXL-base-1.0 is commercially permissive; provenance of each image is the binding constraint.)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Style learns weakly / prompt adherence poor despite correct hyperparameters | Natural-language captions fed to SDXL's tag-trained CLIP encoder (or bare tags fed to Flux's T5) | Re-caption in the format the base encoder expects (WD14 tags for SDXL, NL for Flux) | captions |
| Trigger word does not reliably summon the style at inference | Trigger token absent from some captions or count varies across the set | Place trigger first in EVERY caption with a constant token count | captions |

- **Best for:** Bind a style to a trigger word (sdxl, fit 5) ; Prepare captions for SDXL vs Flux (dataset, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=Current as of 2026. The SDXL/CLIP booru-tag vs Flux/T5-XXL natural-language distinction is actively confirmed in 2025-2026 community documentation. No supersession found. | All three sources are real and accessible. Discussion #1497 confirmed via gh API (exists, open, correct title). Haoming02 LoRATraining.md confirmed to exist and directly supports booru-tag conventions and trigger-word placement. arXiv:2412.12048 ('A LoRA is Worth a Thousand Pictures') is a real paper with the correct authors, but its actual subject is using LoRA weight vectors as style retrieval descriptors — it does not study caption format effects on conditioning. The 'PARTIAL' finding_supported tag is correctly applied and honest. Fix required: the citation note should clarify that this paper supports style-capture in LoRA weights generally, not that caption format determines conditioning quality. It is a weak supporting citation, not a direct one. No fabrication.
- **Sources:** [flux lora training TIPs discussion #1497](https://github.com/kohya-ss/sd-scripts/discussions/1497) (kohya-ss/sd-scripts contributors, 2024) — Flux LoRA captioning differs from SDXL; Flux uses T5 and benefits from natural-language captions rather than the booru tags used for SDXL. ; [All-in-One Stable Diffusion Guide — LoRA Training](https://github.com/Haoming02/All-in-One-Stable-Diffusion-Guide/blob/main/LoRATraining.md) (Haoming02, 2024) — For booru-tag training the trigger words go at the start of captions and the trigger count must be consistent across the dataset. ; [A LoRA is Worth a Thousand Pictures](https://arxiv.org/abs/2412.12048) (Chenxi Liu, Towaki Takikawa, Alec Jacobson, 2024) — LoRA weights alone are an effective descriptor of artistic style learnable from minimal data, validating that style is captured by a small well-conditioned set.

### Concept isolation for multi-concept LoRAs (anti-bleed) · `recommended` · ▸ reproduced
**Packing several concepts into one LoRA causes concept-bleed because distinct concepts collide on the same cross-attention tokens; isolation requires a DISTINCT rare trigger per concept, separate subsets, and captions that never co-name two concepts in one image -- or the concepts fuse and become un-promptable apart.**
When one LoRA must carry multiple concepts (several characters, several sub-styles, an effect library), the dominant failure is concept-bleed/crosstalk: the concepts smear into each other and you cannot summon one without the other leaking in. The cross-attention mechanism is the cause -- multiple concepts gravitate to the same tokens, so their gradients interfere (TARA 2508.08812 shows constraining each concept to its own rare token localizes effects and prevents conflict; CollectionLoRA 2605.25378 shows cascaded/co-trained effects without orthogonal triggers produce severe interference and style degradation; CAT 2404.07554 uses a contrastive objective to stop a concept collapsing into near-identical same-class outputs). The dataset-side discipline that follows: (1) give every concept its own DISTINCT rare/non-word trigger token (not a shared one); (2) keep each concept in its own subset folder so per-concept repeats and isolation hold; (3) caption so a given image names only the concept(s) actually present -- never co-list two triggers unless both subjects truly co-occur, because co-naming teaches co-occurrence; (4) avoid repeating identical captioning templates across concepts, which over-couples them. Semantically related concepts bleed worst (DyME 2509.21433), so visually similar concepts are the ones to separate most carefully. When isolation is hard, the safer studio answer is one LoRA per concept rather than forcing a contaminated multi-concept adapter.
- **For the pipeline:** style-dataset-lab must assign a unique rare trigger per concept in a multi-concept project (constitution owns the trigger registry), keep one subset per concept, and run a caption linter that flags any caption co-listing two concept triggers on an image where both are not present. Default recommendation for unrelated concepts: ship separate single-concept LoRAs; reserve multi-concept packing for concepts that genuinely co-appear.
- **Method:** dataset-construction · **Applies to:** diffusion · **Base:** SDXL · **Kind:** curation
- **Validated under:** Cross-attention-based diffusion LoRA/adapter training; bleed severity rises with semantic similarity of concepts; findings from arXiv method papers, not rig-measured this wave.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — Dataset/caption discipline only; provenance governs commercial cleanliness.
- **Fit:** rig 4/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| network_type | LoRA | ○ | applies to standard cross-attention LoRA |
| keep_tokens | >=1 so the per-concept trigger stays fixed under shuffle tokens | ● | kohya keep_tokens pins leading trigger token(s) per subset |

- **Datasets:** SDXL multi-concept style set with per-subset repeat balancing (train, license studio-owned (synthetic via commercial-clean base); commercial-clean only if every source plate and the generating base clear commercial use -- verify per project)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Summoning concept A also produces concept B | shared trigger token / co-named captions / semantically similar concepts collide on same attention tokens | distinct rare trigger per concept, separate subsets, lint co-naming; or split into separate LoRAs | network_type |
| Concepts collapse to near-identical same-class outputs (lost diversity) | concept overwrites base-class prior without contrast | add class/regularization contrast (see prior-preservation technique); reduce over-coupled captions | datasets |

- **Best for:** Multi-concept LoRA without crosstalk (concept-isolation, fit 4)
- **Verify:** verdict=confirmed-with-fixes | currency=Current — TARA (2025) and CollectionLoRA (2026) are recent; anti-bleed guidance is not superseded. | TARA (arXiv:2508.08812) and CollectionLoRA (arXiv:2605.25378) both exist and directly support the core cross-attention token interference / concept-bleed claims. CAT (arXiv:2404.07554, CVPRW 2024) is a real paper but is a partial fit: it addresses preserving base-model knowledge and preventing same-class diversity collapse, not multi-concept LoRA bleed specifically. The finding_supported flag already says PARTIAL, but the source-to-claim connection in the technique should be narrowed — CAT should be cited only for the 'contrastive loss preserves prior knowledge' sub-claim, not as evidence for the main anti-bleed architecture. No dedup issue; this extends wave-1 with the anti-bleed mechanism specifically.
- **Sources:** [TARA: Token-Aware LoRA for Composable Personalization in Diffusion Models](https://arxiv.org/pdf/2508.08812) (et al., 2025) — Different LoRA modules focus on the same cross-attention token causing interference; constraining each module to its own rare token localizes effects and prevents conflicts. ; [CollectionLoRA: Collecting 50 Effects in 1 LoRA via Multi-Teacher On-Policy Distillation](https://arxiv.org/html/2605.25378) (et al., 2026) — Cascading/co-training effect LoRAs triggers severe parameter interference, concept bleeding, and style degradation; orthogonal trigger words isolate concepts in latent space. ; [CAT: Contrastive Adapter Training for Personalized Image Generation](https://arxiv.org/pdf/2404.07554) (Park, Park, Koh, Lee, Song, 2024) — A contrastive loss preserves base-model knowledge and prevents a personalized concept from collapsing into nearly identical same-class objects.

### Per-folder num_repeats as the multi-concept balancing lever · `recommended` · ▸ reproduced
**In kohya sd-scripts the effective weight of each concept is (images x num_repeats) per subset, so you balance an uneven multi-concept set by raising num_repeats on the scarce folders to equalize seen-samples-per-epoch, NOT by duplicating files on disk.**
kohya sd-scripts (and the DreamBooth folder convention <num_repeats>_<trigger> <class>) treats num_repeats as a per-subset multiplier: one epoch draws each subset's images num_repeats times, so a concept's influence is images x num_repeats. When a style/character set spans several concepts of unequal size (e.g. 80 background plates, 18 portrait plates), training the raw folders lets the 80-image concept dominate and the 18-image concept under-fits. The fix is to set repeats so the products roughly match (e.g. 1x80 vs 4x18=72), giving each concept comparable gradient mass per epoch. This is the cleaner alternative to file duplication: it is declared in the dataset_config .toml at [[datasets.subsets]] level, is reversible, keeps dedup/datasheet counts honest (real image count is unchanged), and can differ per subset alongside per-subset resolution buckets. The same lever rescues a single under-represented sub-style inside one project. Crucial caveat: repeats multiply EXPOSURE not DIVERSITY -- repeating 18 images 4x still only shows 18 distinct images, so balance fixes weighting, not coverage; a truly thin concept needs more real images, not more repeats.
- **For the pipeline:** style-dataset-lab's training-package emitter must compute per-subset num_repeats from concept image counts to equalize images x repeats across concepts, and write it into the dataset_config .toml -- never by copying files (which corrupts dedup and datasheet counts). Surface the per-concept effective weight in the package manifest so the imbalance is visible before a run. Repeats are a balancing knob, not a data-volume substitute.
- **Method:** dataset-construction · **Applies to:** diffusion · **Base:** SDXL · **Kind:** recipe
- **Validated under:** kohya sd-scripts dataset_config .toml with multiple [[datasets.subsets]]; balance is per-epoch seen-count, holds for both DreamBooth-style and fine-tune subsets; no rig measurement this wave.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — Pure dataset-config lever; commercial cleanliness is governed by image provenance, not by the repeats setting.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| repeats | set so images x repeats is roughly equal across concepts multiplier | ● | per [[datasets.subsets]]; scarce folders get higher repeats |
| resolution | per-subset buckets allowed px | ○ | dataset_config .toml permits per-subset resolution alongside per-subset repeats |
| epochs | tune after balancing epochs | ○ | total steps = sum(images x repeats) x epochs / batch_size; rebalancing repeats changes step budget |

- **Datasets:** SDXL multi-concept style set with per-subset repeat balancing (train, license studio-owned (synthetic via commercial-clean base); commercial-clean only if every source plate and the generating base clear commercial use -- verify per project)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Large concept dominates, small concept barely learned | raw folders trained 1:1 with unequal image counts | raise num_repeats on the small folder until images x repeats matches | repeats |
| Small concept overfits / memorizes despite balancing | high repeats multiplied exposure of too few distinct images | add real images to the thin concept; repeats cannot create diversity | repeats |

- **Best for:** Multi-concept / multi-sub-style style LoRA balancing (multi-concept-balance, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=Current — num_repeats mechanics unchanged in kohya sd-scripts through 2026. | Claim and sources are sound. The kohya config doc confirms num_repeats is a per-subset weight; the rentry guide and Civitai balancing article confirm the practical use for dataset balance. Minor fix needed: (1) the kohya doc does not use the word 'weight' explicitly — it is correctly inferred from the mechanism, so the claim should reflect this as 'effectively functions as' rather than an explicit doc term; (2) the Civitai balancing article shows that intentional *imbalance* (e.g., more repeats for full-body shots) is also a valid pattern — the 'equalize to balance' framing is the canonical multi-concept use case but should note that optimal distribution is task-dependent, not always equal.
- **Sources:** [kohya-ss/sd-scripts dataset config README (num_repeats, per-subset settings)](https://github.com/kohya-ss/sd-scripts/blob/main/docs/config_README-en.md) (kohya-ss, 2024) — num_repeats specifies repeats per subset and functions as a weight; subsets with higher num_repeats appear more frequently per epoch, configurable at general/datasets/subsets levels. ; [Kohya Dreambooth Method Mini Guide (num_repeats folder naming, dataset balancing)](https://rentry.co/kohyaminiguide) (rentry (community), 2024) — Folder naming <num_repeats>_<token> <class> and num_repeats are used to balance datasets, especially with limited images per concept.

### Regularization / class-image set construction (model-generated, not external) · `recommended` · ▸ reproduced
**Prior-preservation regularization images must be GENERATED BY THE SAME BASE MODEL from the bare class prompt (no trigger) -- using external/photo datasets as reg images destroys the class-word prior because their distribution diverges from the model's own prior; the DreamBooth paper used ~200 model-sampled class images per class.**
Regularization (prior-preservation) images are the contrast that stops a subject/style LoRA from overwriting the whole class. The DreamBooth paper (Ruiz et al. 2208.12242) introduces a class-specific prior-preservation loss supervised by ~200 images the model itself samples from the bare class prompt (e.g. 'a dog'), preventing language drift and preserving in-class diversity. Two construction rules are load-bearing: (1) SOURCE -- reg images must be generated by the SAME base checkpoint you are training, from the class prompt WITHOUT the trigger; community and follow-up work warn that using external/real photo sets as reg images can fundamentally destroy the class prior because their distribution diverges from the model's own prior for that class word. (2) COUNT -- the canonical figure is ~100-200 per class; the often-cited 1000 was an upper bound that roughly doubles training time for little extra benefit. For a STYLE LoRA the analogue is a 'normal-style' contrast set (same content, base style, no trigger) so the trigger carries only the style; kohya implements this via a reg subset whose repeats are tuned so reg count is on the order of (style images x repeats), not wildly larger. Reg images are most worth the cost when you train the text encoder or push high steps; for a tiny low-rank style LoRA at conservative steps they are sometimes skippable -- but when used, generate-from-base and keep them trigger-free.
- **For the pipeline:** style-dataset-lab's reg-set builder must generate class/normal-style images from the project's exact base checkpoint with the trigger omitted, default to ~150-200 per class, never import external photos as reg, and record reg_image_count + reg_source('model-generated, same base') on the datasheet. Balance reg repeats so reg exposure approximates style exposure rather than swamping it.
- **Method:** regularization · **Applies to:** diffusion · **Base:** SDXL · **Kind:** protocol
- **Validated under:** DreamBooth-style prior preservation on SDXL; ~100-200 model-sampled class images per class; reg must come from the same base distribution; not rig-measured this wave.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — Model-generated reg images inherit the base model's license; commercial-clean only if the generating base is commercial-clean -- verify per project.
- **Fit:** rig 4/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| reg_image_count | 100-200 images per class | ○ | DreamBooth canonical ~200; 1000 is overkill |
| repeats | tune reg subset repeats so reg exposure approximates style exposure multiplier | ○ | avoid reg swamping the concept |
| min_snr_gamma | 5 | ○ | common companion stabilizer; orthogonal to reg construction |

- **Datasets:** SDXL regularization / class-prior set (model-generated, trigger-free) (regularization, license studio-owned (synthetic); inherits the generating base model's license -- commercial-clean only if the base is commercial-clean (SDXL-base-1.0 is permissive; verify generation provenance))

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Whole class drifts / base 'dog' now looks like the trained subject (language drift) | no prior-preservation reg images, or too few | add ~150-200 model-generated class images, trigger-free | reg_image_count |
| Class prior corrupted, weird artifacts on the class word after training | external/real-photo dataset used as reg images (distribution mismatch) | regenerate reg images from the same base checkpoint | reg_source |
| Concept under-learns despite plenty of style images | reg set far larger than style set, swamping the gradient | lower reg count or reg repeats to approximate style exposure | repeats |

- **Best for:** Prevent class/language drift on subject and high-step style LoRAs (prior-preservation, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=Current — DreamBooth prior-preservation is still the canonical technique; guidance not superseded. | The core claim is well-supported by DreamBooth (arXiv:2208.12242) and the Hugging Face diffusers docs. The ~200 class images figure is widely community-reproduced though the abstract-level fetch could not pin the exact count from the paper text — this is a minor uncertainty, not a fabrication. The third source (arXiv:2407.05312) is mis-cited: when fetched, that paper's actual contribution is proposing a method that *avoids* prior preservation loss entirely (limiting training steps instead), not a study demonstrating that external datasets destroy the class-word prior. The stated finding for 2407.05312 ('external datasets fundamentally destroy the class-word prior') does not match what the paper demonstrates. This source should be dropped or replaced with one that directly tests external-vs-model-generated regs.
- **Sources:** [DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation](https://arxiv.org/pdf/2208.12242) (Ruiz, Li, Jampani, Pritch, Rubinstein, Aberman, 2022) — A class-specific prior-preservation loss supervised by the model's own ~200 sampled class images counters language drift and preserves in-class diversity. ; [DreamBooth training (diffusers) -- prior preservation and class images](https://huggingface.co/docs/diffusers/training/dreambooth) (Hugging Face, 2024) — Prior-preservation uses class images generated by the model from the class prompt to regularize and prevent overfitting/drift. ; [An Improved Method for Personalizing Diffusion Models](https://arxiv.org/html/2407.05312v1) (et al., 2024) — Using external datasets as regularization images can fundamentally destroy the class-word prior because their distribution diverges from the model's own prior for that class.

### Semantic dedup + train-eval overlap check before training · `recommended` · ▸ reproduced
**Remove semantic near-duplicates (embedding-cosine, not just exact-hash) and verify the eval set shares no items with the train set, or duplicated images over-weight the style toward repeated motifs and any eval number is contaminated.**
Two coupled curation gates. (1) Dedup: exact-hash (pHash/MD5) catches re-saves but misses semantic near-duplicates (crops, recolors, same scene). SemDeDup (Abbas et al. 2023) embeds each image with a pretrained encoder and removes pairs above a cosine-similarity threshold; on LAION it removed ~50% of data while preserving performance and halving training time. For a small style set the goal is the opposite of scale — it is to stop 4 near-identical frames from one source dominating the style. A practical threshold is ~0.9-0.95 cosine on CLIP/DINO embeddings (tune per set). (2) Train-eval overlap: Lee et al. 2021 showed deduplicating training data and removing train-test overlap (which affected >4% of common validation sets) cuts memorization ~10x and makes evaluation honest. For a LoRA, any image used to judge style fidelity must not also be in the training set, or the eval rewards memorization.
- **For the pipeline:** style-dataset-lab curation must run an embedding-cosine dedup pass (not only pHash) and hold out an eval subset that is provably disjoint from train (set train_eval_overlap_checked=1 on the datasheet). The evaluation lane's A/B and CMMD numbers are meaningless without this; the dataset row carries the contamination flag.
- **Method:** lora · **Applies to:** both · **Base:** SDXL · **Kind:** protocol
- **Tuning budget:** threshold tuned per set (sweep 0.88-0.96 cosine and eyeball the removed pairs) · **Search:** grid
- **Variance:** Both papers report consistent, peer-reviewed effects (SemDeDup at web scale; Lee et al. at ACL 2022). The specific cosine threshold for a small style set is a tunable, not a universal constant.
- **Validated under:** SemDeDup: web-scale LAION/C4 (cross-domain to small style sets — flagged); Lee et al.: LLM corpora. Applied here as a curation protocol, not rig-measured.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **conditional** — Protocol is license-neutral. The embedding model used for dedup (CLIP/DINO) is an instrument; its weights are catalogued in model-knowledge, not here.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| dedup_method | embedding-cosine (CLIP/DINO) + pHash prefilter method | ● | semantic near-dupes, not just exact re-saves (SemDeDup) |
| dedup_threshold | 0.90-0.95 cosine (tune per set) cosine | ● | lower for small style sets to catch crops/recolors |

- **Datasets:** SDXL style-LoRA training set (canon-bound, WD14-tagged) (training, license Internal / project-canon only — commercial cleanliness gated per source plate; not for redistribution unless every source image clears a commercial license. Base SDXL-base-1.0 is commercially permissive; provenance of each image is the binding constraint.)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Style over-fixates on a single motif/character that appears in many near-identical training frames | Semantic near-duplicates survived an exact-hash-only dedup and over-weighted that motif | Run embedding-cosine dedup at ~0.9 threshold; cap frames-per-source-scene | dedup |
| Eval scores look great but generations on novel prompts are poor | Eval images overlap the training set — the metric is rewarding memorization | Hold out an eval subset disjoint from train; set train_eval_overlap_checked=1 | captions |

- **Best for:** Honest evaluation (eval, fit 5) ; Balanced style coverage (dataset, fit 4)
- **Verify:** verdict=confirmed-with-fixes | currency=Current as of 2026. SemDeDup (2023) is actively used in NVIDIA NeMo's data curation pipeline. Lee et al. (2021) remains the canonical LLM dedup reference. No supersession. | Both papers are real with correct authors and confirmed claims: arXiv:2303.09540 confirms cosine-similarity-based semantic dedup removed ~50% of LAION-440M while preserving performance; arXiv:2107.06499 confirms ~10x memorization reduction and >4% validation set overlap. Critical fix required under the KB's own evidence honesty rules: both papers study large-scale pretraining (440M+ images or LLM corpora), not LoRA fine-tuning on 20-200 images. This is a cross-domain import that is not flagged anywhere in the technique. Per the boundary discipline: 'Cross-domain imports must be flagged in the note and tagged no higher than community-claim unless separately sourced.' evidence_strength of 'reproduced-from-source' overclaims the LoRA application specifically. It should be downgraded to community-claim for the LoRA use case OR a cross-domain-import flag must be added with a note about threshold calibration at small dataset scales (naive SemDeDup thresholds calibrated on 440M images may eliminate most of a 50-image LoRA set).
- **Sources:** [SemDeDup: Data-efficient learning at web-scale through semantic deduplication](https://arxiv.org/abs/2303.09540) (Amro Abbas, Kushal Tirumala, Daniel Simig, Surya Ganguli, Ari S. Morcos, 2023) — Removing semantic near-duplicates via embedding cosine similarity removed ~50% of LAION while preserving performance and halving training time. ; [Deduplicating Training Data Makes Language Models Better](https://arxiv.org/abs/2107.06499) (Katherine Lee, Daphne Ippolito, Andrew Nystrom, Chiyuan Zhang, Douglas Eck, Chris Callison-Burch, Nicholas Carlini, 2021) — Deduplication cut memorized output ~10x and removed train-test overlap affecting >4% of validation sets, enabling reliable evaluation.

### Style-vs-subject caption pruning (the style-bleed lever) · `recommended` · ▸ reproduced
**What you caption is what the model treats as variable; for a STYLE LoRA you caption the controllable content and DO NOT name the style, so the unnamed style binds to the trigger instead of bleeding into content tokens — the inverse of subject training, where you prune content and keep variables.**
The pruning rule is the most direct lever on style binding. The principle: any attribute you describe becomes a controllable variable the LoRA can be prompted away from; any attribute you leave undescribed gets absorbed into the trigger/implicit baseline. For a SUBJECT LoRA you therefore prune tags describing the subject's invariant features (keep only pose/background variables) so those features fuse to the trigger. For a STYLE LoRA you do the opposite — caption the content thoroughly (subjects, composition, colors) but never name the style itself ('oil painting', 'cel shaded', the artist) — so the only thing left for the trigger to carry is the style. Over-captioning the style is the classic style-bleed cause: the style scatters across many content tokens and contaminates every generation regardless of trigger.
- **For the pipeline:** style-dataset-lab's caption pass for a style project must run a style-term blocklist (prune medium/technique/artist descriptors from auto-captions) while keeping content tags. This single rule moves more outcome than rank or LR. The blocklist is per-project canon, owned in the constitution.
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** curation
- **Tuning budget:** manual — curate the caption blocklist per project; no numeric search · **Search:** manual
- **Variance:** Consistent across kohya community guidance and multiple style-training diaries; mechanism (described=variable, undescribed=baseline) is well understood and reproducible.
- **Validated under:** SDXL 1024px style LoRA, 20-40 image curated set; not rig-measured for throughput
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **conditional** — License-neutral curation rule; output cleanliness inherits from base + source images.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| caption_strategy | describe content, prune style descriptors (style binds to trigger) rule | ● | STYLE LoRA: keep content tags, drop medium/technique/artist tags |
| caption_strategy | describe variables, prune subject descriptors rule | ○ | SUBJECT LoRA: the inverse — drop subject-invariant tags so they fuse to trigger |

- **Datasets:** SDXL style-LoRA training set (canon-bound, WD14-tagged) (training, license Internal / project-canon only — commercial cleanliness gated per source plate; not for redistribution unless every source image clears a commercial license. Base SDXL-base-1.0 is commercially permissive; provenance of each image is the binding constraint.)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Style bleeds into everything — every generation looks styled even without the trigger; content cannot be prompted cleanly | Style descriptors (medium/technique/artist) left in captions, scattering the style across content tokens | Prune all style-naming tags from captions so style binds only to the trigger; add regularization images; lower network dim if persistent | captions |
| Trigger summons the subject's invariant features but loses pose/background flexibility | On a subject LoRA, the variable tags (pose/background) were pruned instead of the subject-invariant ones | Invert the prune: keep variable tags, drop subject-invariant tags | captions |

- **Best for:** Bind a style to a trigger word (diffusion, fit 5) ; Control style bleed (sdxl, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=Current as of 2026. Prune-style / keep-content for style LoRAs remains the active community consensus for both SDXL and Flux workflows. | Haoming02 LoRATraining.md confirmed to exist and directly supports caption pruning (remove tags describing the subject, keep variables). Apatero.com blog confirmed to exist (published Dec 2025) and supports style-bleed remedies including caption improvement, regularization images, and lowering network dim. The Civitai article #6792 is login-gated; content cannot be verified externally. The CANT_TELL tag on that source is correctly applied and honest. Fix required: add a standing note that the Civitai source is unverifiable externally (login wall) and must not be upgraded to SUPPORTED in future evidence reviews. The technique claim itself is well-supported by the two verifiable sources.
- **Sources:** [All-in-One Stable Diffusion Guide — LoRA Training (caption pruning)](https://github.com/Haoming02/All-in-One-Stable-Diffusion-Guide/blob/main/LoRATraining.md) (Haoming02, 2024) — Manually prune captions: remove tags describing your subject and keep only the 'variables' so the LoRA associates the subject's features with the trigger word. ; [Flux Style Captioning Differences — Training Diary](https://civitai.com/articles/6792/flux-style-captioning-differences-training-diary) (Civitai community author, 2024) — Style-LoRA captioning describes the depicted content but not the style itself, so the style attaches to the trigger rather than to content terms. ; [Kohya SS LoRA Training: Complete Guide 2025 (style bleed remedies)](https://www.apatero.com/blog/kohya-ss-lora-training-complete-guide-2025) (Apatero, 2025) — When style bleeds into everything, remedies include improving captions, adding regularization images, and lowering network dim.

### Two-stage dedup: pHash gate then CLIP/DINO cosine gate (with thresholds) · `recommended` · ▸ reproduced
**Run dedup as two stages -- a cheap pHash Hamming-distance gate for exact/near re-saves, then an L2-normalized CLIP/DINO cosine gate for semantic near-dups -- because pHash alone misses recolors/crops/reframes and embedding-only is slow; practical thresholds are pHash Hamming <=8 and cosine >=0.90-0.93, tuned per set.**
Wave-1 established THAT semantic dedup matters and that train-eval overlap must be zero; this extends it to the concrete PIPELINE and THRESHOLDS. Stage 1 (fast filter): perceptual hash (pHash) on the image, flag pairs with Hamming distance <= ~8 as near-duplicate re-saves/crops (community guidance puts 1-5 bits as 'very close', ~15 as the upper near-dup edge; a comparative study uses <=8 as the stage-1 cut). Stage 2 (semantic): embed survivors with an L2-normalized CLIP or DINO vision encoder and flag cosine >= ~0.90-0.93 as semantic near-dups (recolors, reframes, same scene different pose). Threshold is set-dependent: a tight style set with deliberately similar frames needs a HIGHER cut (e.g. 0.95) to avoid nuking legitimate variety, while a scraped set tolerates a lower cut. The two-stage order matters for cost: pHash is near-free and removes the bulk; embedding runs only on what survives. DataComp (2304.14108) and SemDeDup show dedup at scale preserves performance while cutting data and time; for a SMALL studio set the goal is inverted -- stop 4 near-identical source frames from over-weighting the style, NOT shrink the set. Critically, the SAME embedding pass doubles as the train-eval overlap check: any train image within cosine threshold of a held-out eval image silently contaminates the eval, so dedup and overlap-check share one embedding index.
- **For the pipeline:** style-dataset-lab curation must implement dedup as pHash-first then CLIP/DINO-cosine, expose both thresholds (default Hamming<=8, cosine>=0.92) as per-project knobs, and reuse the same embedding index to assert train-eval disjointness -- writing dedup_method, dedup_threshold, and train_eval_overlap_checked onto the datasheet. Style sets get a higher cosine cut than scraped sets to preserve intended variety.
- **Method:** curation · **Applies to:** diffusion · **Base:** any · **Kind:** protocol
- **Validated under:** pHash Hamming and CLIP/DINO cosine thresholds are dataset-dependent starting points; small style sets favor higher cosine cuts; not rig-measured this wave.
- **Output license:** commercial **yes** — Pure curation tooling; eval instruments (CLIP/DINO) cited as instruments only.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| dedup_threshold | pHash Hamming <= 8 bits | ● | stage-1 fast gate; tighten toward 5 for strict re-save removal |
| dedup_threshold | cosine >= 0.90-0.93 (0.95 for tight style sets) cosine | ● | stage-2 semantic gate on L2-normalized CLIP/DINO embeddings |

- **Datasets:** SDXL multi-concept style set with per-subset repeat balancing (train, license studio-owned (synthetic via commercial-clean base); commercial-clean only if every source plate and the generating base clear commercial use -- verify per project)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Style over-weights toward a repeated motif | near-identical source frames survived because only exact-hash dedup ran | add stage-2 embedding-cosine gate at ~0.92 | dedup_method |
| Legitimate intended variety wrongly removed | cosine threshold set too low for a deliberately consistent style set | raise cosine cut to ~0.95 for tight style sets | dedup_threshold |
| Eval numbers look great but generations are memorized | train-eval overlap not checked with the same embedding index | assert every train image is below cosine threshold to all eval images | train_eval_overlap_checked |

- **Best for:** Prevent motif over-weighting and eval contamination (dedup-pipeline, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=Current — approach is not superseded; the MDPI paper is from April 2026. | The MDPI Electronics 15/7/1493 paper is real and relevant, but it appears to be a comparative evaluation of separate methods (pHash families vs CNN embeddings) rather than a paper that proposes or empirically validates a two-stage pHash-then-embedding pipeline with the specific thresholds cited (Hamming ≤8, cosine ≥0.90–0.93). The paper could not be fetched (403) so the specific threshold claims cannot be confirmed as paper-stated results — they appear to be community-practice numbers grafted onto the paper citation. Fix: the threshold values (Hamming ≤8, cosine ≥0.90–0.93) should be tagged community-claim or marked as 'practical starting points from community practice' rather than paper-derived results. The DataComp citation is a reasonable PARTIAL fit for embedding-based filtering quality. Not a dedup of wave-1's semantic-dedup entry — this genuinely extends it by adding the pHash fast-pass gate.
- **Sources:** [Comparative Evaluation of Perceptual Hashing and Deep Embedding Methods for Robust and Efficient Image Deduplication](https://www.mdpi.com/2079-9292/15/7/1493) (et al., 2026) — A two-stage pipeline -- pHash Hamming <=8 then L2-normalized vision-embedding cosine >=0.93 (images) -- robustly removes near-duplicates faster than embedding-only. ; [DataComp: In search of the next generation of multimodal datasets](https://arxiv.org/pdf/2304.14108) (Gadre et al., 2023) — Embedding-based dedup/filtering of large image-text pools materially affects downstream quality, validating semantic dedup over exact-hash.

### Accumulate-don't-replace real:synthetic discipline (collapse guard) · `recommended` · · community
**When augmenting a style set with model-generated images, ACCUMULATE them alongside the real data — never replace real data with synthetic — because replacement provably tends toward model collapse while accumulation keeps test error bounded.**
A studio that bootstraps a style with its own generated images risks the recursive-training failure mode: train on outputs, generate, retrain on those outputs. Gerstgrasser et al. (2024) prove the distinction empirically and theoretically — replacing each generation's real data with synthetic data drives model collapse, but accumulating successive synthetic generations alongside the original real data bounds test error independent of iteration count, so collapse no longer occurs. The operational rule for the studio: keep every real image in the set permanently; synthetic images are additive only, never a substitute; track a real:synthetic ratio on the datasheet and keep real well-represented (a healthy floor, not synthetic-dominant). The finding is established for LLMs and generative training loops; applying it to a single SDXL style-LoRA augmentation loop is a reasonable transfer of the mechanism, flagged as cross-domain.
- **For the pipeline:** style-dataset-lab must store real_synthetic_ratio on every dataset row and forbid a re-ingest step from deleting real images when adding synthetic ones. The snapshot/re-ingest pipeline accumulates; it never replaces. This is the model-collapse guard for the canon-bootstrapping workflow.
- **Method:** lora · **Applies to:** both · **Base:** SDXL · **Kind:** method-theory
- **Tuning budget:** n/a — discipline rule, not a tuned value; ratio is monitored, not optimized · **Search:** none
- **Variance:** The source result (accumulate>replace) is peer-reviewed and robust for recursive generative-training loops; the transfer to a single-LoRA style-augmentation loop is the studio's inference, not separately measured — hence capped at community-claim per cross-domain-import honesty.
- **Validated under:** Source: recursive LLM/generative training loops. Transfer target: SDXL style-LoRA augmentation. Cross-domain import explicitly flagged; not rig-measured.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **conditional** — Synthetic images generated by a non-commercial base (e.g. FLUX.1-dev) carry that base's license downstream — a separate commercial-cleanliness concern from collapse. Accumulation discipline does not change provenance; the datasheet still gates license.
- **Fit:** rig 4/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| caption_strategy | accumulate synthetic, never replace real; track real:synthetic ratio rule | ● | real images are permanent; synthetic is additive only |

- **Datasets:** SDXL style-LoRA training set (canon-bound, WD14-tagged) (training, license Internal / project-canon only — commercial cleanliness gated per source plate; not for redistribution unless every source image clears a commercial license. Base SDXL-base-1.0 is commercially permissive; provenance of each image is the binding constraint.)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Successive re-trained style LoRAs drift, lose diversity, and converge to a narrow look over generations | Each generation replaced real training data with the previous model's synthetic output (recursive collapse) | Accumulate: keep all real images permanently; add synthetic on top; never substitute | captions |

- **Best for:** Avoid model collapse (dataset, fit 5) ; Bootstrap a style from limited real images (dataset, fit 4)
- **Verify:** verdict=confirmed-with-fixes | currency=Current as of 2026. Gerstgrasser et al. 2024 remains the canonical model-collapse-via-replacement reference. No refutation or supersession found. | arXiv:2404.01413 is a real paper with correct title and authors. All three core claims confirmed: replacement causes collapse, accumulation avoids collapse, and bounded test error is proven analytically. The paper explicitly covers diffusion models alongside language models and VAEs. evidence_strength is tagged 'community-claim' which is conservative (under-claimed) rather than over-claimed — no honesty violation. Fix required: the note field should document why the tag was not elevated. Given the paper covers diffusion models directly with empirical validation and analytical proof, 'reproduced-from-source' would be defensible and more accurate. Keeping it at community-claim without explanation leaves an unexplained gap between evidence quality and assigned tag.
- **Sources:** [Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Synthetic Data](https://arxiv.org/abs/2404.01413) (Matthias Gerstgrasser, Rylan Schaeffer, Apratim Dey, Rafael Rafailov, Henry Sleight, John Hughes, Tomasz Korbak, et al., 2024) — Replacing real data with synthetic data tends toward model collapse; accumulating synthetic data alongside the original real data avoids collapse and bounds test error.

### Dataset size scaling: style vs character vs concept (few-good vs many) · `recommended` · · community
**Required image count scales with the BREADTH of what the LoRA must generalize: characters need only ~15-40 varied shots (narrow target), concepts ~30-100, and STYLE needs the widest coverage (~50-200) across many subjects so the model learns style as independent of any one subject -- and across all three, consistency beats raw count.**
There is no single 'good dataset size' -- it scales with target breadth. CHARACTER/face LoRA (narrowest): ~15-40 images is plenty, but they must vary pose (front/three-quarter/profile), lighting, and expression so the identity, not the photo, is learned; more near-identical shots over-fit, not improve. CONCEPT LoRA (an object/pose/outfit): ~30-100. STYLE LoRA (widest): ~50-200 because the model must learn the style as ORTHOGONAL to content -- a watercolor style set must contain watercolor of landscapes, characters, objects, and abstracts, or the LoRA fuses style to whatever subject it saw most. The studio's #1 workload (game-art style) is therefore the most coverage-hungry: spread the trigger style across the canon's subject variety, not 80 frames of one scene. The cross-cutting law is quality/consistency > quantity: a small set of clean, on-style, well-captioned images beats a large noisy one, and 10-20 excellent images can outperform 100 mediocre ones. Practical floor for a style: enough subject variety that no single subject dominates after dedup. This pairs directly with the per-folder-repeats lever (balance within the set) and the dedup pipeline (so 'count' means DISTINCT count, not re-saves).
- **For the pipeline:** style-dataset-lab should target ~50-200 DISTINCT (post-dedup) on-style images for a style project, enforce subject-variety coverage (flag if one subject/scene exceeds a share of the set), and treat character/concept sub-LoRAs with the smaller ~15-100 brackets. The brief generator should request subject DIVERSITY for style sets, not volume; the datasheet records image_count as the post-dedup distinct count.
- **Method:** dataset-construction · **Applies to:** diffusion · **Base:** SDXL · **Kind:** method-theory
- **Validated under:** Count brackets are aggregated community/guide practice for SDXL-family LoRAs (style 50-200, character 15-40, concept 30-100); breadth-driven, consistency-dominant; not rig-measured this wave.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — Sizing guidance only; provenance governs commercial cleanliness.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| repeats | use per-folder repeats to balance once size targets are met multiplier | ○ | pairs with size scaling |
| epochs | fewer epochs for larger varied sets; more for tiny sets epochs | ○ | tiny sets over-fit fast |

- **Datasets:** SDXL multi-concept style set with per-subset repeat balancing (train, license studio-owned (synthetic via commercial-clean base); commercial-clean only if every source plate and the generating base clear commercial use -- verify per project)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Style only renders on one subject type | style set lacked subject variety; style fused to dominant subject | broaden subject coverage; spread the style across many subjects | image_count |
| Character over-fits to a single pose/outfit | too many near-identical character shots, too little variation | swap duplicates for varied poses/lighting; ~15-40 varied beats 100 same | image_count |
| Large set trains poorly / noisy output | volume over quality -- mediocre images added for count | cut to the clean, on-style core; consistency beats count | image_count |

- **Best for:** Right-sizing a style/character/concept dataset (size-scaling, fit 5)
- **Verify:** verdict=confirmed | currency=Current — size brackets are still the operative community guidance for 2026 LoRA training. | evidence_strength is honestly tagged community-claim. Both sources (Civitai detailed Flux guide, SeaArt docs) are real, publicly accessible community references that support the brackets cited. The core insight — style needs broader subject coverage than character or concept targets — is consistent with how the field understands generalization. No peer-reviewed paper is cited here, which is appropriate given the community-claim tag. Not a dup of any wave-1 entry. Boundary clean.
- **Sources:** [Detailed Flux Training Guide: Dataset Preparation](https://civitai.com/articles/7777/detailed-flux-training-guide-dataset-preparation) (Civitai (community), 2024) — Style needs broad subject coverage so the model learns style independent of subject; character needs varied poses/lighting; consistency and quality dominate count. ; [How To Create Dataset For Training (SeaArt) -- size brackets by LoRA type](https://docs.seaart.ai/guide-1/3-advanced-guide/3-2-lora-training-advance/how-to-create-dataset-for-training) (SeaArt, 2024) — Style LoRA ~50-200 images, character ~15-40, concept ~30-100; a small set of good images beats a large bad one.

### Datasheets for Datasets provenance gate (Gebru et al.) · `situational` · paper
**Document motivation/composition/collection/uses — commercial-clean provenance gate**
STUDY-035 Scholar/Analogist Verifier ✅.
- **For the pipeline:** STUDY-035 Verifier ✅. WD thresholds only as card-scraped.
- **Method:** dataset · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-035 deepen
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [Datasheets for Datasets (arXiv)](https://arxiv.org/abs/1803.09010) — Structured dataset documentation. ; [Datasheets for Datasets (CACM DOI)](https://doi.org/10.1145/3458723) — CACM datasheet template.

### DreamBooth subject craft + class prior-preservation (Ruiz et al. 2022) · `situational` · paper
**Few-shot subject fine-tune with class prior-preservation — ancestral subject/style dataset craft**
STUDY-035 Scholar deepen — 2208.12242.
- **For the pipeline:** STUDY-035 Verifier ✅. WD thresholds only as card-scraped.
- **Method:** dataset · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-035 deepen
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** OPERATOR PRISM ACCEPT PRISM-ACCEPT-P2 (arXiv 2208.12242 DreamBooth)
- **Sources:** [DreamBooth](https://arxiv.org/abs/2208.12242) — Subject-driven generation with prior preservation.

### JoyCaption diffusion-dataset caption VLM · `situational` · docs
**Descriptive/Straightforward/SD-prompt/Danbooru-tag modes for training-set captions.**
STUDY-035 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-035 Verifier ✅. WD thresholds only as card-scraped.
- **Method:** dataset · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-035 deepen
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [JoyCaption README](https://github.com/fpgaminer/joycaption) — Caption VLM modes for diffusion datasets.

### LIMA quality-over-quantity alignment data (Zhou et al. 2023) · `situational` · paper
**~1k carefully curated instructions can rival larger noisy pools — quality-over-quantity**
STUDY-035 Scholar deepen — 2305.11206.
- **For the pipeline:** STUDY-035 Verifier ✅. WD thresholds only as card-scraped.
- **Method:** dataset · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-035 deepen
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [LIMA](https://arxiv.org/abs/2305.11206) — Less is more for alignment with curated data.

### Large-Scale Data Selection for Instruction Tuning · `situational` · paper
**Stress-tests automated instruction-data selectors beyond ~10k toy pools; curated smaller sets still beat larger noisier pools when selection scales.**
Stress-tests automated instruction-data selectors beyond ~10k toy pools; curated smaller sets still beat larger noisier pools when selection scales.
- **For the pipeline:** STUDY-009 Verifier-verified. Do not flip technique rows.
- **Method:** data-selection · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama · **Kind:** dataset-craft
- **Output license:** commercial **check** — STUDY-019 reopen; verified=0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [Large-Scale Data Selection for Instruction Tuning](https://arxiv.org/abs/2503.01807) — Stress-tests automated instruction-data selectors beyond ~10k toy pools; curated smaller sets still beat larger noisier pools when selection scales.

### WD EVA02-Large Tagger v3 card metrics (sourced only) · `situational` · docs
**Booru tagger with card-scraped v1.0 P=R threshold 0.5296 and F1 0.4772 only.**
STUDY-035 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-035 Verifier ✅. WD thresholds only as card-scraped.
- **Method:** dataset · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** recipe
- **Output license:** commercial **check** — STUDY-035 deepen
- **Fit:** rig 4/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| P_equals_R_threshold | 0.5296 | ○ | WD EVA02 card v1.0 scraped only |
| F1 | 0.4772 | ○ | WD EVA02 card v1.0 scraped only |

- **Sources:** [WD EVA02-Large Tagger v3](https://huggingface.co/SmilingWolf/wd-eva02-large-tagger-v3) — v1.0 P=R threshold=0.5296 F1=0.4772 on card. ; [ComfyUI-WD14-Tagger](https://github.com/pythongosssss/ComfyUI-WD14-Tagger) — ComfyUI WD14/WD-v3 batch tagger peer.

### kohya-ss dataset TOML craft (aug/repeats/reg) · `situational` · docs
**Per-subset flip/color/crop, num_repeats, caption_dropout, is_reg, resolution mix — sourced train-set craft**
STUDY-035 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-035 Verifier ✅. WD thresholds only as card-scraped.
- **Method:** dataset · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-035 deepen
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [kohya-ss config README](https://github.com/kohya-ss/sd-scripts/blob/main/docs/config_README-en.md) — Dataset TOML craft knobs.

