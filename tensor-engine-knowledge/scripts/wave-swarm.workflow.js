export const meta = {
  name: 'tensor-engine-wave-1',
  description: 'Study-swarm wave 1: best tensor/inference/training engines per lane for the single RTX 5090 / Blackwell / Windows 11 studio rig (32 GB VRAM + 64 GB RAM), web-grounded + adversarially verified',
  phases: [
    { title: 'Research', detail: '7 web-grounded lane researchers (one per engine category)' },
    { title: 'Verify', detail: '1 reasoning-stripped retrieval-verifier per lane (Sonnet, decorrelated)' },
  ],
}

// ── PRE-READ CONVENTION (offload token-saver) ───────────────────────────────────────────────────
// When a wave's agent must INGEST a large pre-existing source — a long incident log, a multi-page
// spec, a DB/JSON dump, prior-wave prose, or a heavyweight docs page — do NOT paste the raw into the
// agent prompt. Pre-compress it ORCHESTRATOR-SIDE first (Workflow scripts cannot shell out, so this
// runs before/around the workflow, not inside it):
//
//     python scripts/preread.py --file <big-source> --words 150 --json   # or --url <page>
//
// preread.py shells `offload compress` (qwen3-4b on llama-swap, local + free) and returns a digest +
// a token receipt; embed the DIGEST in the agent prompt so the raw never reaches Claude. Measured on
// this KB's OWN wave-1 artifacts: 7242 -> 572 Claude-tokens, 92.1% smaller (receipt:
// verifier/preread-wave-receipt.json; config_recipe #162). Sources under --threshold-words pass
// through (don't pay a model call to shrink something already small); sources over the local model's
// ~16K-token context must be chunked per-source.
//
// THIS wave needs no pre-read — its inputs are already compact (lane instructions + structured claims,
// not raw source dumps). The convention is for source-ingesting waves; it lives here as the template
// so the next such wave reaches for it. The VERIFY stage is the EXTERNAL_VERIFIER seat; a local
// non-Claude entailment panel (offload verify --panel) is the decorrelated companion check — see
// readouts/tensor-engine-knowledge/verifier/ and role-os `verify-citations --local-panel`.

const RIG = `TARGET RIG — the ONE machine this is for (filter every recommendation for it):
- HP OMEN 45L · NVIDIA RTX 5090 · Blackwell sm_120 · 32 GB VRAM · Intel Core Ultra 9 · 64 GB system RAM · Windows 11 Pro. CUDA 12.8+ / cu128 wheels. This is the ONLY rig — there is NO Mac and no second machine.
- WINDOWS-NATIVE support is LOAD-BEARING: many engines are Linux-first or need WSL2. State Windows support honestly and rate it down if it is Linux-only or WSL2-painful.
- 64 GB system RAM makes CPU/RAM OFFLOAD viable — models a bit over 32 GB VRAM can spill to RAM (GGUF partial offload, ZeRO/CPU-offload, KTransformers-style CPU+GPU MoE). Note where an engine does this well.
- USE: a local-first, single-human + LLM-crew game studio. Local inference, local-LLM delegation, local diffusion/ComfyUI, and LoRA/style fine-tuning are the REAL workloads — NOT datacenter-scale multi-node serving. Catalogue datacenter tools too, but score studio_fit by usefulness on a single powerful workstation.
- Apple-Silicon / MLX / Metal: there is no Mac here, so treat these as CROSS-PLATFORM REFERENCE knowledge (worth recording that an engine supports them) — NOT a rig you must fit.`

const LANES = [
  { slug: 'llm-inference', name: 'LLM inference engines',
    scope: `Local LLM inference engines/runtimes that load and run text/code/reasoning LLMs. Cover at least: llama.cpp (+ the GGUF ecosystem), vLLM, SGLang, ExLlamaV2 AND ExLlamaV3, TensorRT-LLM, Ollama, LM Studio's engine (llama.cpp/MLX backends), KTransformers, MLC-LLM, Hugging Face TGI, LMDeploy, ik_llama.cpp, llamafile, Aphrodite Engine. For each: what it's best at (max throughput vs single-stream latency vs lowest-VRAM), which model formats it consumes, Windows + Blackwell/RTX-5090 (sm_120, CUDA 12.8+) support TODAY, multi-GPU strategy, CPU/RAM offload for >32 GB models on a 64 GB-RAM box, ease of setup, license. Explicitly flag the Linux-only / poor-Windows-support engines — that is decisive for this rig.` },
  { slug: 'llm-serving', name: 'Serving, batching & routing',
    scope: `The production serving / batching / routing / multi-model layer that sits ON TOP of inference engines, plus embedding & reranker servers. Cover: NVIDIA Triton Inference Server, Ray Serve, the vLLM and SGLang OpenAI-compatible server modes, llama-swap (model hot-swap), LiteLLM proxy, KServe, BentoML / OpenLLM, Text Embeddings Inference (TEI), Infinity (embeddings/rerank), TorchServe. Axes: continuous/in-flight batching, OpenAI API compatibility, model hot-swap, multi-model hosting, observability, Windows support, and — important for this rig — single-workstation usefulness vs datacenter-only complexity.` },
  { slug: 'quantization', name: 'Quantization frameworks & formats',
    scope: `Quantization algorithms, frameworks, AND weight formats for shrinking models to fit VRAM and/or speed inference. Cover formats and the tools that make them: GGUF (k-quants, i-quants, imatrix calibration), GPTQ, AWQ, EXL2 AND EXL3, bitsandbytes (NF4/INT8), FP8 (E4M3/E5M2), NVFP4 and MXFP4 (Blackwell-native 4-bit), HQQ, AutoRound, SmoothQuant, llm-compressor, llama.cpp quantize. Axes: quality-vs-size tradeoff at each bit width, WHICH inference engines consume each format (the format-to-engine compatibility matrix is the key deliverable), Blackwell FP4 hardware support, calibration cost, license.` },
  { slug: 'attention-kernels', name: 'Attention backends & GPU kernels',
    scope: `Attention backends and GPU kernel libraries that engines plug in for speed/memory. Cover: FlashAttention 2 AND 3, FlashInfer, xFormers memory-efficient attention, PagedAttention (vLLM), SageAttention 1/2/3 (esp. for diffusion + Blackwell), FlexAttention (PyTorch), Triton kernels + triton-windows, Marlin / Machete (quantized GEMM kernels), cuDNN fused attention. Axes: which engines use each, Blackwell/sm_120 + Windows support, the diffusion-vs-LLM split, when each wins (prefill vs decode, long-context), license. Capture the well-known Blackwell pitfall: do NOT pip install xformers into embedded Python; the modern Windows stack is SageAttention + triton-windows + torch.compile.` },
  { slug: 'training', name: 'Training & fine-tuning engines',
    scope: `Training and fine-tuning engines/frameworks — full fine-tune, LoRA/QLoRA, RLHF/DPO. Cover: PyTorch FSDP AND FSDP2, DeepSpeed (ZeRO-1/2/3 + CPU/NVMe offload), Megatron-LM / Megatron-Core, Unsloth, Axolotl, LLaMA-Factory, torchtune, Hugging Face PEFT + TRL + Trainer, Liger-Kernel, NVIDIA NeMo. Axes: single-GPU (RTX 5090, 32 GB VRAM + 64 GB RAM) LoRA/QLoRA fit, multi-GPU strategies, memory-saving tricks (gradient checkpointing, ZeRO/CPU-offload, paged optimizers, fused kernels), Blackwell + Windows support (be honest about the WSL2 reality), ease of setup, license. This lane ties directly to the studio's LoRA-training-for-style needs (incl. SDXL/Qwen image-LoRA training where relevant).` },
  { slug: 'diffusion-engines', name: 'Diffusion inference engines & accelerators',
    scope: `Inference engines and accelerators specifically for DIFFUSION (image/video) models — the ENGINE/accelerator layer, NOT the models (models are catalogued in a separate model-knowledge KB; do not re-list checkpoints). Cover: ComfyUI (as a runtime/engine), Hugging Face Diffusers, stable-fast, TensorRT for diffusers / the ComfyUI TensorRT path, xDiT (parallel/multi-GPU diffusion), Nunchaku (SVDQuant 4-bit kernels), OneDiff, DeepCache / FBCache, SageAttention-for-diffusion, ComfyUI-GGUF (city96), para-attention. Axes: the speedup technique (compile, caching, quant, parallelism, distillation runtime), Blackwell + Windows support, VRAM reduction, which model families supported (Flux / SDXL / Wan / Qwen-Image), license. Complement the model KB's comfy.md — this is the accelerator/engine layer beneath those workflows. Note the known Blackwell facts: ComfyUI portable now ships CUDA 13 + py3.13, PyTorch 2.7+ has stable sm_120, do NOT hand-install torch nightly, never pip install xformers — use SageAttention.` },
  { slug: 'runtime-foundations', name: 'Foundational runtimes & compilers',
    scope: `The foundational tensor runtimes, compilers, and cross-platform backends that everything else is built on. Cover: PyTorch (eager + torch.compile / TorchInductor), JAX + XLA, ONNX Runtime (+ DirectML for Windows GPUs), NVIDIA TensorRT (core), Apple MLX (record it as cross-platform reference — there is no Mac on this rig), ggml, OpenVINO, Apache TVM, Triton (the compiler/language), and the CUDA / cuDNN / cuBLAS substrate (incl. the sm_120 / CUDA 12.8 Blackwell story — which PyTorch version first shipped stable Blackwell wheels, Windows specifics). Axes: what sits on each, Blackwell/CUDA-12.8+/sm_120 support, Windows-native vs WSL2, when to reach for each, license. This is the 'what is underneath' lane.` },
]

const ENGINE_SCHEMA = {
  type: 'object',
  required: ['name', 'slug', 'license', 'commercial_use', 'status', 'summary', 'sources'],
  properties: {
    name: { type: 'string' },
    slug: { type: 'string', description: 'kebab-case unique id' },
    developer: { type: 'string' },
    engine_type: { type: 'string', description: 'inference-server | runtime | kernel-lib | quant-format | quant-tool | training-framework | serving-layer | compiler' },
    language: { type: 'string' },
    latest_version: { type: 'string' },
    release_date: { type: 'string' },
    license: { type: 'string' },
    commercial_use: { type: 'string', enum: ['yes', 'no', 'conditional', 'unknown'] },
    commercial_notes: { type: 'string' },
    maturity_tier: { type: 'string', enum: ['production', 'mature', 'stable', 'experimental', 'legacy', 'avoid'] },
    platforms: { type: 'string', description: 'e.g. "linux, windows, macos" — which OSes are supported' },
    accelerators: { type: 'string', description: 'e.g. "cuda, rocm, metal, cpu, vulkan, xpu"' },
    model_formats: { type: 'string', description: 'formats it loads/produces: gguf, safetensors, gptq, awq, exl2, exl3, fp8, nvfp4 ...' },
    blackwell_ready: { type: ['boolean', 'null'], description: 'runs on RTX 5090 / sm_120 / CUDA 12.8+ on Windows TODAY' },
    optimization_for: { type: 'string', description: 'throughput | latency | memory | flexibility | portability' },
    multi_gpu: { type: 'string', description: 'none | tensor-parallel | pipeline-parallel | data-parallel | fsdp | zero' },
    rig_fit: { type: ['integer', 'null'], minimum: 0, maximum: 5, description: 'fit for THE rig: RTX 5090 / Blackwell sm_120 / Windows 11 / 32 GB VRAM + 64 GB RAM' },
    studio_fit: { type: ['integer', 'null'], minimum: 0, maximum: 5, description: 'fit for the local single-user studio workload (local LLM + diffusion + LoRA training) vs datacenter-only tooling' },
    speed_note: { type: 'string' },
    status: { type: 'string', enum: ['recommended', 'runner-up', 'situational', 'legacy', 'avoid'] },
    summary: { type: 'string', description: '3-6 dense sentences: what it is, when to reach for it, key config/optimization knobs, Blackwell/Windows gotchas' },
    best_for: {
      type: 'array',
      items: {
        type: 'object',
        required: ['purpose'],
        properties: {
          purpose: { type: 'string' },
          use_tag: { type: 'string', description: 'nvidia | windows | local | server | training | reference' },
          fitness: { type: ['integer', 'null'], minimum: 0, maximum: 5 },
        },
      },
    },
    repo_url: { type: 'string' },
    sources: {
      type: 'array',
      minItems: 1,
      items: {
        type: 'object',
        required: ['url'],
        properties: {
          url: { type: 'string' },
          claim: { type: 'string', description: 'one-sentence finding this source backs' },
          kind: { type: 'string', description: 'repo | docs | release-notes | benchmark | model-card | article | community' },
          title: { type: 'string' },
        },
      },
    },
  },
}

const RESEARCH_SCHEMA = {
  type: 'object',
  required: ['domain', 'notes', 'engines'],
  properties: {
    domain: { type: 'string' },
    notes: { type: 'string', description: 'lane-level synthesis: findings -> a concrete recommendation for THIS single rig. Which 2-3 engines to actually install for this lane and why; the decisive axis; what changed recently.' },
    engines: { type: 'array', minItems: 5, items: ENGINE_SCHEMA },
    extras: {
      type: 'array',
      description: 'config recipes (kind:"recipe") = the how-to-configure/optimize-properly knowledge; plus kind:"tool"|"resource" for adjacent tools/benchmarks',
      items: {
        type: 'object',
        properties: {
          kind: { type: 'string', description: 'recipe | tool | resource' },
          name: { type: 'string' },
          url: { type: 'string' },
          note: { type: 'string' },
        },
      },
    },
  },
}

const VERIFY_SCHEMA = {
  type: 'object',
  required: ['verdicts'],
  properties: {
    verdicts: {
      type: 'array',
      items: {
        type: 'object',
        required: ['model', 'overall'],
        properties: {
          model: { type: 'string', description: 'engine name (matches the research engine name exactly)' },
          overall: { type: 'string', enum: ['confirmed', 'confirmed-with-fixes', 'unverified', 'refuted'] },
          currency: { type: 'string', enum: ['current', 'superseded', 'deprecated', 'unknown'] },
          license_status: { type: 'string', enum: ['ok', 'corrected'] },
          license_correction: { type: 'string' },
          fixes: { type: 'string' },
          note: { type: 'string' },
        },
      },
    },
    proposed_additions: {
      type: 'array',
      description: 'up to 3 must-have engines in this lane the researcher omitted',
      items: { type: 'object', properties: { name: { type: 'string' }, why: { type: 'string' } } },
    },
    receipt: { type: 'string', description: 'one-paragraph verifier summary' },
  },
}

function researchPrompt(lane) {
  return `You are a senior ML-infrastructure engineer building a long-lived, queryable knowledge base of TENSOR / INFERENCE / TRAINING ENGINES — the *software frameworks* that run and train AI models (NOT the models themselves; those live in a separate KB, so do not catalogue checkpoints here).

LANE: ${lane.name}
SCOPE: ${lane.scope}

${RIG}

It is 2026-06-02. Your training cutoff predates many current versions — VERIFY LIVE with web search/fetch. Do NOT trust memory for version numbers, licenses, or Blackwell/Windows support. Prefer official repos, docs, release notes, and engine cards. Every non-obvious claim (especially license, latest version, and Blackwell/Windows support) must carry a source.

For EACH engine (aim for 6-10 of the genuinely meaningful ones, ranked by how strongly you'd recommend it for this rig — set status accordingly):
- Identity: name, slug (kebab), developer, engine_type, primary language, latest_version + release/version date.
- License: license + commercial_use (yes|no|conditional|unknown) + commercial_notes. License is a real axis (GPL vs Apache vs MIT vs custom). Call out anything that constrains commercial/studio use.
- Platform reality: platforms, accelerators, model_formats it loads/produces, blackwell_ready (does it run on RTX 5090 / sm_120 / CUDA 12.8+ on WINDOWS today?), multi_gpu, optimization_for.
- Fit: rig_fit (0-5 for the RTX 5090 / Blackwell / Windows / 32 GB-VRAM + 64 GB-RAM rig), studio_fit (0-5 for the local single-user studio workload vs datacenter-only tooling), maturity_tier, status, speed_note.
- summary: 3-6 dense, technical sentences — what it is, when to reach for it, the key config/optimization knobs, and the Blackwell/Windows gotchas. Match the depth of an excellent engineering README.
- best_for: 2-5 {purpose, use_tag, fitness}.
- repo_url and sources (>=1 {url, claim, kind, title}).

Also fill:
- notes: a lane-level synthesis (findings -> a concrete recommendation for THIS rig). Which 2-3 engines should the studio actually install for this lane, and why? What is the decisive axis in this lane? What changed recently that inverts old advice?
- extras: the "how to configure/optimize PROPERLY" knowledge as {kind:"recipe", name, url, note} — exact build flags, launch commands, tensor-parallel / quant / offload settings tuned for a 32 GB-VRAM + 64 GB-RAM RTX 5090 on Windows — plus {kind:"tool"|"resource", ...} for adjacent tools and benchmarks. This is what makes the KB actionable, not just a list.

Be specific, current, and sourced. Return ONLY the structured object.`
}

function verifyPrompt(lane, claims) {
  return `You are an ADVERSARIAL, REASONING-STRIPPED verifier in a study-swarm EXTERNAL_VERIFIER stage. You are deliberately given ONLY the bare claims and source URLs below — NOT the researcher's reasoning, summaries, or recommendations — so your check is decorrelated from how the claims were produced. It is 2026-06-02.

LANE: ${lane.name}
CLAIMS (one entry per engine):
${JSON.stringify(claims, null, 1)}

Use web search / fetch as a RETRIEVAL ORACLE. For EACH engine, check against the LIVE page:
1. EXISTS — does the repo/page resolve with that name + developer?
2. LICENSE + commercial_use — correct? If wrong, set license_status="corrected" and give the correction. This is the highest-value axis — be exacting about Apache vs GPL vs MIT vs custom community licenses (and any revenue/territory/use caps).
3. SPECS — latest_version, blackwell_ready (sm_120 / CUDA 12.8+ on Windows), platforms, model_formats: plausible and current?
4. CURRENCY — current | superseded | deprecated as of 2026-06-02?

Default verdict on NON-confirmation is "unverified" — do NOT pass on faith. overall is one of confirmed | confirmed-with-fixes | unverified | refuted. Put concrete corrections in fixes / license_correction / note.

Then list up to 3 must-have engines in THIS lane that the researcher OMITTED (proposed_additions, each with a one-line why), and write a one-paragraph receipt of what you checked and caught.

Return ONLY the structured object.`
}

phase('Research')
log(`Dispatching ${LANES.length} lane researchers + verifiers (single RTX 5090 / Win11 rig, date ${args.date})`)

const lanes = await pipeline(
  LANES,
  (lane) => agent(researchPrompt(lane), {
    label: `research:${lane.slug}`,
    phase: 'Research',
    schema: RESEARCH_SCHEMA,
    agentType: 'general-purpose',
  }),
  (research, lane) => {
    const claims = (research.engines || []).map((e) => ({
      name: e.name,
      developer: e.developer,
      license: e.license,
      commercial_use: e.commercial_use,
      latest_version: e.latest_version,
      blackwell_ready: e.blackwell_ready,
      platforms: e.platforms,
      model_formats: e.model_formats,
      repo_url: e.repo_url,
      source_urls: (e.sources || []).map((s) => s.url),
    }))
    return agent(verifyPrompt(lane, claims), {
      label: `verify:${lane.slug}`,
      phase: 'Verify',
      schema: VERIFY_SCHEMA,
      agentType: 'general-purpose',
      model: 'sonnet',
    }).then((verify) => {
      const conf = (verify.verdicts || []).filter((v) => v.overall === 'confirmed' || v.overall === 'confirmed-with-fixes').length
      log(`${lane.slug}: ${(research.engines || []).length} engines, ${conf}/${(verify.verdicts || []).length} verified-ok`)
      return { slug: lane.slug, name: lane.name, research, verify }
    })
  }
)

const ok = lanes.filter(Boolean)
const totalEngines = ok.reduce((n, l) => n + ((l.research.engines || []).length), 0)
const totalSources = ok.reduce((n, l) => n + (l.research.engines || []).reduce((m, e) => m + ((e.sources || []).length), 0), 0)
log(`Wave 1 assembled: ${ok.length}/${LANES.length} lanes, ${totalEngines} engines, ${totalSources} sources`)

return { date: args.date, wave: 1, lanes: ok }
