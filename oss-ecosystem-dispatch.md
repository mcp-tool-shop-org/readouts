# OSS Ecosystem Scout — study-swarm dispatch (2026-08-01)

Studio: mcp-tool-shop (1-human + LLM crew, commercial 2.5D JRPGs). Question: where should
the studio ADOPT open source instead of hand-building, and fork/depend/contribute on what
terms? Five parallel research lanes; every citation below is subject to the Step-4 gate.

## Research grounding (the dispatch's empirical floor)

### Fork vs depend vs contribute

1. **Divergent forks almost never re-integrate code in either direction.** Businge, Openja, Nadi & Berger 2022 (DOI:10.1007/s10664-021-10078-2), EMSE — across 38 Android, 526 .NET and 8,837 JavaScript fork-based families. Implication: budget any fork as a permanent second codebase, never as a temporary divergence.
2. **Only ~11% of mainline–variant pairs ever exchange code, and flow is mainline→variant.** Businge et al. 2022 (arXiv:2204.11083). Implication: a studio fork is a subscription to upstream, not a contribution to it.
3. **Porting a peer project's patch lagged 725–944 days on average across 18 years of BSD history, and did not improve over time.** Ray & Kim 2012 (DOI:10.1145/2393596.2393659), FSE. Implication: patch-carrying is a permanent recurring tax.
4. **`git cherry-pick` failed on 64.4% of 478 bug-fix PRs across 14 divergent variant pairs, due to structural drift.** Wang et al. 2025 (arXiv:2508.06718). Implication: "we'll just rebase our patches" is empirically false past the first refactor.
5. **No downstream strategy wins on all axes: rebasers get zero delay but 100% mainline bug inheritance; conservative pickers inherit 0.2–6.3% but port slowest.** Li, Zhang, Qian, Jaeger & Song 2024 (arXiv:2402.05212), MSR. Implication: staying close to upstream is the cheapest of the bad options.
6. **Very few forks ever merge back with the original, across several hundred significant forks.** Robles & González-Barahona 2012 (DOI:10.1007/978-3-642-33442-9_1), OSS. Implication: forking is a one-way door.
7. **Successful forks succeed by capturing the upstream community's most active long-term committers.** Gamalielsson & Lundell 2014 (DOI:10.1016/j.jss.2013.11.1077), JSS — LibreOffice showed no stagnation 33 months post-fork. Implication: a 1-human studio cannot supply the success condition.
8. **Better modularity and centralized management predict more contributions and higher PR acceptance.** Zhou, Vasilescu & Kästner 2019 (DOI:10.1145/3338906.3338918), ESEC/FSE. Implication: extension points are the lever the studio controls; prefer plugin seams to forks.
9. **Most hard forks evolved accidentally out of social forks rather than being planned.** Zhou et al. 2020 (DOI:10.1145/3377811.3380412), ICSE — 15,306 classified hard forks. Implication: forks must be a deliberate, dated decision or they happen by drift.
10. **Dormant packages accumulate outdated dependencies and unpatched vulnerabilities.** Zerouali, Pontillo & De Roover 2025 (DOI:10.1007/s10664-025-10753-8), EMSE. Implication: dependency risk is real but different in kind — pin and lock rather than pre-emptively fork.
11. **174 real malicious packages across npm/PyPI/RubyGems, mostly typosquatting and maintainer-account compromise.** Ohm, Plate, Sykosch & Meier 2020 (arXiv:2005.09535), DIMVA. Implication: vendor-on-incident, not vendor-by-default.
12. **51.1% of license-declaring forks violated modification terms; 95.3% of obligating commits lacked required modification notices.** Huang, Xia, Chen, Zhou, Guo & Peng 2023 (arXiv:2310.07991). Implication: near-universal non-compliance is the DEFAULT outcome — a fork needs a NOTICE/MODIFICATIONS gate in shipcheck or it will be non-compliant.

### Metrics (for the impasto question)

13. **FID carries a sample-size-dependent bias whose magnitude differs per model, so ranking can invert on bias alone.** Chong & Forsyth 2020 (arXiv:1911.07023), CVPR. Implication: do NOT use FID on the 73-plate set.
14. **FID has poor sample complexity and gives inconsistent results as sample size varies; its normality assumption on Inception embeddings is wrong. CMMD is an unbiased, distribution-free alternative.** Jayasumana et al. 2024 (arXiv:2401.09603), CVPR.
15. **KID is an unbiased MMD-based estimator with no Gaussian assumption.** Bińkowski et al. 2018 (arXiv:1801.01401). Implication: usable at n=73 if subset size is set below the sample count.
16. **Aligning ImageNet class histograms cuts FID substantially with no quality gain.** Kynkäänniemi et al. 2022 (arXiv:2203.06026). Implication: FID measures class distribution, not the surface quality being asked about.
17. **Aliased resizing and JPEG compression shift FID enough to flip model rankings.** Parmar, Zhang & Zhu 2021 (arXiv:2104.11222). Implication: any texture metric must control preprocessing — resize/format artifacts fake high-frequency energy.
18. **LPIPS deep features beat classical metrics on human 2AFC judgment.** Zhang et al. 2018 (arXiv:1801.03924). Implication: strong, but full-reference/paired — cannot compare two unpaired sets.
19. **DISTS explicitly separates texture similarity from structure similarity using spatial averages of VGG feature maps, and is deliberately tolerant to texture resampling.** Ding, Ma, Wang & Simoncelli 2020 (arXiv:2004.07728), TPAMI. Implication: THE metric for "same surface character, different pixels" — the impasto question exactly.
20. **Feature-map correlations (Gram matrices) are a validated texture representation.** Gatys, Ecker & Bethge 2015 (arXiv:1505.07376). Implication: use the established Gram/StyleLoss form rather than a hand-rolled variant.
21. **CLIP consistently prioritizes content over style, causing style mismatches; CSD outperforms it on style retrieval.** Somepalli et al. 2024 (arXiv:2404.01292). Implication: do not use CLIP similarity as a style/texture judge.
22. **DreamSim deliberately transcends low-level colour and texture, weighting semantics and layout.** Fu et al. 2023 (arXiv:2306.09344), NeurIPS. Implication: engineered to ignore exactly what the impasto question measures — exclude it.
23. **DINO's self-supervised features preserve instance-specific detail that CLIP-I discards.** Ruiz et al. 2022 (arXiv:2208.12242), DreamBooth. Implication: prefer DINO embeddings over CLIP-I for fidelity.
24. **ImageNet-trained CNNs are texture-biased.** Geirhos et al. 2019 (arXiv:1811.12231). Implication: VGG/Inception features are already texture-sensitive, which favours DISTS/Gram here.

### License / compliance

25. **Apache-2.0 §4 binds redistribution of Source or Object form: ship the licence, mark modified files, retain notices, reproduce NOTICE attribution.** Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0). Implication: a shipped game needs a third-party notices surface.
26. **The GPL does not cover a program's output; using GPL tools imposes no licence restriction on what you produce.** FSF GPL FAQ (https://www.gnu.org/licenses/gpl-faq.en.html#WhatCaseIsOutputGPL). Implication: running GPL-3.0 ComfyUI to render a PNG does not GPL the PNG — the studio's art pipeline is clean.
27. **Separate programs communicating via pipes, sockets and command-line arguments are mere aggregation, not a combined work.** FSF GPL FAQ (https://www.gnu.org/licenses/gpl-faq.en.html#MereAggregation). Implication: driving ComfyUI over HTTP as a separate process keeps the game clean; linking would not.
28. **ComfyUI core is licensed GPL-3.0.** (https://github.com/comfyanonymous/ComfyUI/blob/master/LICENSE). Implication: never statically embed; never distribute modified nodes.
29. **FLUX.1 [dev] restricts MODEL use to non-commercial while permitting commercial use of outputs.** (https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/LICENSE.md). Implication: a revenue pipeline generating art is using the model commercially — Qwen-Image (Apache-2.0) avoids the ambiguity.
30. **The GPL forms an enforceable contract by conduct.** Artifex v. Hancom, N.D. Cal. 2017 (https://www.fsf.org/blogs/licensing/update-on-artifex-v-hancom-gnu-gpl-compliance-case-1). Implication: compliance is a contractual exposure, not merely a copyright one.
31. **US copyright requires human authorship for AI-assisted works.** US Copyright Office (https://www.copyright.gov/ai/). Implication: bears on whether shipped assets can be PROTECTED — a second, independent justification for the art contract's human finishing pass.

### Tooling state

32. **kohya-ss/sd-scripts contains no Qwen-Image trainer; Qwen support lives in the separate musubi-tuner repo.** (https://github.com/kohya-ss/sd-scripts). Implication: the sd-scripts clone already on the rig cannot train this studio's base model.
33. **kohya-ss/musubi-tuner provides Qwen-Image and Qwen-Image-Edit training, LoRA extraction, and a VLM captioner (`caption_images_by_qwen_vl.py`).** (https://github.com/kohya-ss/musubi-tuner/blob/main/docs/qwen_image.md). Implication: the strongest single adoption candidate — subsumes the studio's bespoke caption builder.
34. **ostris/ai-toolkit publishes no tags or releases.** (https://github.com/ostris/ai-toolkit). Implication: the studio's current trainer can only be pinned by commit SHA — an open PIN_PER_STEP gap in the shipped saltroad runs.

## Architectural connections (Step 5 — pending verification)

Held until the Step-4 gate completes. No finding above is load-bearing until verified.
