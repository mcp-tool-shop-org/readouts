# readouts — tensor-engine-knowledge · wave dispatches

> The research log: how this KB was built, wave by wave. 17 waves · generated 2026-09-14.

## Wave 1 — Foundation — best tensor / inference / training engines per lane (2026-06-02)

_all (llm-inference, llm-serving, quantization, attention-kernels, training, diffusion-engines, runtime-foundations) · 14 agents · synthesized · +77 engines · +235 sources · +40 recipes_

**Verifier:** Reasoning-stripped adversarial verifier per lane (different model tier); WebFetch/WebSearch as retrieval oracle (existence/license/specs/currency). Family-different prism/roleos path deferred to a later wave.

## Wave 2 — Deep — close the verifier queue + version-pinned config recipes (2026-06-02)

_all (llm-inference, llm-serving, quantization, attention-kernels, training, diffusion-engines, runtime-foundations) · 14 agents · synthesized · +18 engines · +69 sources · +44 recipes_

**Verifier:** Reasoning-stripped adversarial verifier per lane (different model tier); WebFetch/WebSearch as retrieval oracle (existence/license/specs/currency). Family-different prism/roleos path deferred to a later wave.

## Wave 3 — Expansion — 3 new lanes (structured-output, speech, profiling) + deepen kernels & training (2026-06-02)

_all (llm-inference, llm-serving, quantization, attention-kernels, training, diffusion-engines, runtime-foundations) · 10 agents · synthesized · +39 engines · +127 sources · +33 recipes_

**Verifier:** Reasoning-stripped adversarial verifier per lane (different model tier); WebFetch/WebSearch as retrieval oracle (existence/license/specs/currency). Family-different prism/roleos path deferred to a later wave.

## Wave 4 — Measured rig baseline — RTX 5090 thermals / power / throughput via Ollama (2026-06-02)

_all (llm-inference, llm-serving, quantization, attention-kernels, training, diffusion-engines, runtime-foundations) · 2 agents · synthesized · +1 engines · +2 sources · +18 recipes_

**Verifier:** Reasoning-stripped adversarial verifier per lane (different model tier); WebFetch/WebSearch as retrieval oracle (existence/license/specs/currency). Family-different prism/roleos path deferred to a later wave.

## Wave 5 — Recipe-proving II (hands-on) - native-Win llama.cpp->llama-swap serving, SageAttention 2.2.x, Unsloth LLM-LoRA on the RTX 5090 (2026-06-03)

_llm-serving, attention-kernels/diffusion, training · hands-on · synthesized · +1 engines · +1 sources · +9 recipes_

**Verifier:** HANDS-ON MEASURED on the live RTX 5090 (llama-bench pp/tg, llama-swap OpenAI-proxy timings, nvidia-smi telemetry) - direct measurement IS the verifier. The one researched claim (the official prebuilt CUDA-12 llama.cpp ships working sm_120 MMQ) was empirically confirmed: pp512=7251 t/s = 7.3x the cuBLAS-fallback level.

Continues the recipe-proving pass begun under wave 4 (#147-151).

## Wave 6 — Wire offload into real workflows — verifier panel -> roleos verify-citations, study-swarm preread compress, ollama-intern companion (2026-06-03)

_llm-serving (verifier + token-economy wiring) · hands-on · synthesized · +0 engines · +0 sources · +3 recipes_

**Verifier:** HANDS-ON + MEASURED on the live RTX 5090 / llama-swap :9090. The 0-false-confirm PANEL property was RE-PROVEN on a REAL 16-case arXiv citation set (not the rig's own measurements): mistral-nemo-12b solo false-confirmed a refuted claim (inverting arXiv:2404.13076's finding), the 3-seat conservative-majority panel held it at 'insufficient' (0 panel false-confirms). role-os wiring covered by 1196 passing tests; live end-to-end confirmed through role-os's own module against llama-swap.

Closes the wave-5 #156 'NEXT' (wire the panel into roleos verify-citations). offload now SAVES Claude tokens in real pipelines, not on disk. Recipes #162-164.

## Wave 7 — kohya text-encoder + trigger-token style-LoRA path (hands-on) - extends #150/#151 from unet-only (2026-06-03)

_training (kohya_ss SDXL LoRA: TE training + trigger token + regularization gating) · hands-on · synthesized · +0 engines · +0 sources · +2 recipes_

**Verifier:** HANDS-ON MEASURED on the live RTX 5090 (kohya train-log it/s; nvidia-smi clean peak VRAM). EXTERNAL_VERIFIER = the trigger-fires A/B test in ComfyUI: the SDXL generator's output is judged by direct visual inspection of with-trigger vs without-trigger images against a base-only control (a DIFFERENT signal from the generator; the LoRA cannot 'explain' itself, the image is the only evidence; every image looked at per the visual-pipeline look-at-images rule). A semantically-EMPTY trigger (stdstyl) rules out the token's CLIP prior as the cause. Three runs (v1 alpha8/300, v2 alpha16/600, v3 alpha16/700+reg) cross-checked every finding.

Path B (real game canon) deferred: style-dataset-lab outputs/approved/ is empty post-2026-04-27 reformat and needs Mike's sign-off before generating for a game. Blue-fidelity follow-up (v4-v5): the cyanotype blue is NOT recoverable via kohya knobs on SDXL base 1.0 (proven across 5 configs) -- it is the base's color prior; fix = base swap (Z-Image/Lumina2) or drop gating for game styles.

## Wave 8 — Blue-fidelity base swap: Chroma1-HD (Flux-family) LoRA via kohya flux_train_network.py - resolves the wave-7 SDXL blue ceiling (2026-06-03)

_training (Chroma/Flux LoRA: flux_train_network.py --model_type chroma) · hands-on · synthesized · +0 engines · +0 sources · +2 recipes_

**Verifier:** HANDS-ON MEASURED on the live RTX 5090. EXTERNAL_VERIFIER = the trigger-fires A/B in ComfyUI (Chroma generator, judged by direct visual inspection vs a base-only control) PLUS a LoRA-strength sweep; every image looked at. The blue question is answered by measurement, not assertion: the ship reaches strong white-on-prussian-blue cyanotype at LoRA strength 1.5-2.0.

Z-Image/Lumina2 (the originally-named base) is NOT trainable here: Z-Image-Turbo's TE is Qwen3-4B but kohya lumina_train_network.py is hardcoded for Gemma-2; no Z-Image trainer installed. Pivoted to Chroma1-HD (Apache-2.0, Flux-family, kohya-native, a neutral LoRA base).

## Wave 9 — Harden the family-different verifier + prove the token economy at scale — 3rd family (IBM Granite), full-abstract evidence, prompt hardening, real-wave dogfood (2026-06-03)

_llm-serving (verifier panel hardening + token economy) · 3 agents · synthesized · +0 engines · +0 sources · +4 recipes_

**Verifier:** HANDS-ON + MEASURED on the live RTX 5090 / llama-swap :9090, PLUS a real 3-agent study-swarm whose citations were re-checked by the hardened panel. THE FINDING: adding a 3rd verifier FAMILY (IBM Granite 3.3 8B, Apache-2.0) improves accuracy and neutralizes UNCORRELATED single-seat slips, but an adversarial 24-case set BROKE the panel's 0-false-confirm property — #21/#22/#23 (a direction inversion + two plausible-but-unstated additions) fooled a MAJORITY of seats ACROSS ALL FAMILIES (#22 fooled all four), and conservative majority cannot catch a CORRELATED slip. The literature (Kim 2025 arXiv:2506.07962; Kuncheva-Whitaker 2003; PoLL arXiv:2404.18796) confirms family diversity fixes idiosyncratic bias, not correlated error. The FIX that worked is a different lever: a HARDENED verify prompt (explicit direction-check + added-specific-check) recovered ALL 3 correlated false-confirms (per-family panel 3 fc -> 0 fc, accuracy 79.2% -> 87.5%, no regressions) and is now the offload default. Move #2 (full-abstract evidence to the panel) and a real-wave dogfood (89.6% preread token saving + the panel catching a real agent mischaracterization) round it out. Receipts in verifier/: citation-panel-3family-receipt.json, prompt-hardening-receipt.json, e2e-full-abstract-receipt.json, wave9-dogfood-receipt.json.

Closes the standing '3rd family / multi-lens >=3' gap from #156/#162. Recipes #169-172.

## Wave 10 — Mechanistically-orthogonal NLI verifier seat — breaks the correlated false-confirm ceiling family diversity couldn't (encoder NLI cross-encoder as a monotone-safe floor) (2026-06-03)

_llm-serving (verifier panel — orthogonal NLI floor + calibrated abstention) · hands-on · synthesized · +0 engines · +0 sources · +1 recipes_

**Verifier:** HANDS-ON + MEASURED on the live RTX 5090 (no research swarm). THE FINDING: wave-9's 3-family LLM panel (all decoder-only instruct = SAME mechanism) shares a CORRELATED credulity blind spot (#21/#22/#23; #22 fooled all three families); conservative majority + a 3rd family cannot catch a CORRELATED slip (Kuncheva & Whitaker 2003 — majority-vote accuracy is bounded by member CORRELATION, not count). The durable fix is a member that FAILS DIFFERENTLY: an encoder NLI cross-encoder (DeBERTa-v3-large MNLI+FEVER+ANLI+LingNLI+WANLI, MIT; reasoning-stripped, no prompt). MEASURED on the 24-case adversarial set: NLI seat SOLO 100%/0fc (8/8 traps), catches ALL 3 correlated false-confirms; combined LLM-panel + NLI FLOOR (veto on 'supported', downgrade-only -> CANNOT add a false-confirm) holds 0fc under BOTH the legacy (79.2->91.7%) and the hardened (87.5%) prompt; the floor BEATS a 4th-seat majority (which still slips #22 — the correlated bloc out-votes the orthogonal seat). HONEST: n=24 small + the traps are NLI-canonical, so 100% is not a general claim; the durable value is the COMBINATION (LLM reasoning + NLI orthogonal floor), and the floor is monotone-safe. Receipt: verifier/citation-panel-nli-receipt.json.

Closes the wave-9 #171 NEXT (mechanistically-orthogonal verifier + calibrated abstention). Recipe #173. Companion: studio-local/nli_floor.py.

## Wave 11 — Stress the orthogonal NLI seat beyond NLI-canonical traps + sentence-level evidence selection (a hard 15-case set; a negative result on sentence-level; the hardened LLM panel over-escalates numerics) (2026-06-03)

_llm-serving (verifier panel — hard-set stress + sentence-level FEVER selection) · hands-on · synthesized · +0 engines · +0 sources · +1 recipes_

**Verifier:** HANDS-ON + MEASURED on the live RTX 5090 / llama-swap :9090 (LLM panel ran LIVE on 15 new cases). A DECONFIRMING wave: (1) the hard set (numeric/multi-hop/scope/paraphrase grounded in the same sha-pinned abstracts) did NOT break NLI doc-level (100%/0fc/0-over-escalation) — the wave-10 NLI-canonical caveat is weaker than feared; (2) sentence-level FEVER selection is a NEGATIVE result (80% hard, 70.8% on the 24-case regression vs doc-level 100%/100% — loses document context the numeric cases need), so doc-level STAYS the default; (3) the hardened LLM panel is the WEAKEST verifier here (73.3%) — its added-specific-check over-escalates legitimate numeric paraphrases (#25/#26/#27) and over-refutes a scope claim (#34); on ALL 4 NLI-vs-LLM disagreements NLI doc-level was right. 0 false-confirms across EVERY method (the safety property is universal on this set). Receipt: verifier/citation-panel-hard-receipt.json.

Recipe #174. Negative result on sentence-level (kept behind verify_one_sentencewise(), not promoted). The LLM numeric over-escalation is a future prompt-refinement lever, NOT a floor change.

## Wave 12 — Numeric-paraphrase prompt fix — a QUANTITY EXCEPTION in the verify prompt's added-specific-check (closes the wave-11 over-escalation; clean win, 0 new false-confirms) (2026-06-03)

_llm-serving (verifier panel — verify-prompt refinement) · hands-on · synthesized · +0 engines · +0 sources · +1 recipes_

**Verifier:** HANDS-ON + MEASURED on the live RTX 5090 / llama-swap :9090 (refined panel ran LIVE on 39 cases). Closes the wave-11 finding that the hardened added-specific-check over-escalates legitimate numeric PARAPHRASES (it stamped 'fewer than two-thirds' of 23/36, 'more than half', 'roughly 200' of N=199 as insufficient). Surgical fix = a QUANTITY EXCEPTION: a number that is a restatement/rounding/one-step arithmetic consequence of a STATED quantity is NOT 'added' (evaluate under support/contradiction); a CONTRADICTORY number is still refuted; an ABSENT number is still insufficient. CLEAN WIN, 0 false-confirms everywhere, no trap regressions: 24-case 87.5->95.8% (also fixed #8 'over 100,000' + #20 'all 36' insufficient->refuted), hard-15 73.3->86.7% (#25/#27 fixed), combined 82.1->92.3%. Honest residual: #26 went insufficient->refuted (still a safe miss; NLI doc-level gets it right). Adoptable via OFFLOAD_VERIFY_SYS_FILE; PROMOTED to offload's DEFAULT with Mike's sign-off + verified (byte-identical to verify_sys_numeric.txt; the CLI returns supported on #25; _V_SYS_HARDENED_V1 preserved; role-os inherits it). Receipt: verifier/citation-panel-prompt-v2-receipt.json.

Recipe #175. PROMOTED to offload's default with Mike's sign-off + verified (byte-identical to verify_sys_numeric.txt; `offload verify --panel` returns supported on #25); _V_SYS_HARDENED_V1 preserved; role-os --local-panel inherits it via the shelled CLI.

## Wave 13 — Generality test (physical-sciences abstracts) + a disagreement-gated consensus — the verifier's 0-false-confirm property is DOMAIN-DEPENDENT; numeric-comparison + unit claims break BOTH learned verifiers (2026-06-03)

_llm-serving (verifier panel — generality + consensus gate) · hands-on · synthesized · +0 engines · +0 sources · +1 recipes_

**Verifier:** HANDS-ON + MEASURED on the live RTX 5090 / llama-swap :9090 (LLM panel ran LIVE on offload's PROMOTED wave-12 default). THE GENERALITY TEST BROKE THE VERIFIER — the first false-confirms in the whole arc, which is what a rigorous test should find. On 17 physics cases (LIGO/ATLAS/CMS/Planck/EHT, real sha-pinned abstracts): NLI doc-level drops to 76.5% with 2 FALSE-CONFIRMS (#48 'exceeded' missing 5.0<5.8; #55 milliarcseconds vs microarcseconds), and the CORRELATED-failure ceiling RE-EMERGES — #48/#55 false-confirm BOTH the LLM panel AND the orthogonal NLI seat (#55 fooled all 3 LLM seats + NLI). Mechanistic orthogonality REDUCES but does not ELIMINATE correlated error; quantitative-comparison + unit failure modes are shared by a decoder LLM and an encoder NLI alike. The combination's value is real but partial (#45 the NLI floor caught a panel false-confirm; #41 the panel did arithmetic the NLI couldn't). The consensus gate fixes the #26 residual on AI/ML (escalate instead of auto-refuting a true claim; 0 fc on the 39) but inherits the correlated blind spot. The durable fix = a mechanistically-THIRD, DETERMINISTIC numeric/unit verifier (wave-14). Receipt: verifier/citation-panel-multidomain-receipt.json.

Recipe #176. Honest negative finding: the 0-fc property is DOMAIN-DEPENDENT (AI/ML-validated, physics-broken). Wave-14 = a deterministic numeric/unit checker (the third, non-learned mechanism).

## Wave 14 — Deterministic numeric/unit floor — the third, non-learned mechanism catches the correlated failures both learned verifiers shared, restoring 0-false-confirm across domains (the capstone) (2026-06-03)

_llm-serving (verifier panel — deterministic numeric/unit floor) · hands-on · synthesized · +0 engines · +0 sources · +1 recipes_

**Verifier:** MEASURED on all 56 labeled cases (stdlib, no GPU). The wave-13 generality test found 2 correlated false-confirms (#48 numeric comparison, #55 unit) that fooled BOTH the LLM panel AND the orthogonal NLI seat. Wave-14 adds the fix the finding named: a DETERMINISTIC numeric/unit verifier (numeric_floor.py) — the quantity analog of prism's existence floor, a refute-or-abstain mechanism that can't be fooled by surface plausibility. It catches BOTH #48 (5.0<5.8 so not 'exceeded') and #55 (42 milli- vs micro-arcsec, the case that fooled all 4 learned verifiers) with 0 false-refutes across all 56 cases (100% precision). THE FULL STACK RESTORES 0-FALSE-CONFIRM ON PHYSICS: + the numeric floor takes nli_doc / NLI-veto-floor / consensus from 2 fc to 0 fc (the complete deterministic-floor + LLM-panel + NLI-floor stack = 0 fc on BOTH AI/ML and physics). Validates defense-in-depth: three mechanistically-DIFFERENT layers each catch what the others miss. Receipt: verifier/citation-panel-numeric-receipt.json.

Recipe #177. The capstone of the verifier arc: deterministic floor (existence + numeric/unit) -> LLM panel -> NLI floor, 0-fc across domains. Honest residual: the comparison rule is targeted (shared-noun anchor) and abstains safely on structures it can't bind.

## Wave 15 — Wave 15 (2026-09-06)

_all (llm-inference, llm-serving, quantization, attention-kernels, training, diffusion-engines, runtime-foundations) · 8 agents · synthesized · +13 engines · +13 sources · +0 recipes_

**Verifier:** Reasoning-stripped adversarial verifier per lane (different model tier); WebFetch/WebSearch as retrieval oracle (existence/license/specs/currency). Family-different prism/roleos path deferred to a later wave.

## Wave 16 — Wave 16 (2026-09-07)

_all (llm-inference, llm-serving, quantization, attention-kernels, training, diffusion-engines, runtime-foundations) · 6 agents · synthesized · +22 engines · +22 sources · +0 recipes_

**Verifier:** Reasoning-stripped adversarial verifier per lane (different model tier); WebFetch/WebSearch as retrieval oracle (existence/license/specs/currency). Family-different prism/roleos path deferred to a later wave.

## Wave 17 — Wave 17 (2026-09-07)

_all (llm-inference, llm-serving, quantization, attention-kernels, training, diffusion-engines, runtime-foundations) · 8 agents · synthesized · +22 engines · +22 sources · +0 recipes_

**Verifier:** Reasoning-stripped adversarial verifier per lane (different model tier); WebFetch/WebSearch as retrieval oracle (existence/license/specs/currency). Family-different prism/roleos path deferred to a later wave.
