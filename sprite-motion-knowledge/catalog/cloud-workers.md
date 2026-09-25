# Cloud GPU workers
_Run bigger-than-VRAM animation/edit models as a pipeline worker, not a website: RunPod / Modal / fal.ai / Replicate / HF Inference Endpoints; ComfyUI-as-serverless, cold starts, model caching, cost. Source-of-truth stays in the repo._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

7 recipes · 5 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 2 | ComfyUI-as-serverless pattern (platform-agnostic) | custom | cloud-compute/pipeline | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Modal custom Python pipeline on H100/H200/B200 | modal | cloud-compute/pipeline | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | RunPod serverless ComfyUI worker | runpod | cloud-compute/pipeline | ▸ reproduced | ✅ yes | 5 | 4 | ✓ |
| 2 | fal.ai serverless media API and custom deployment | fal | cloud-compute/pipeline | ▸ reproduced | ✅ yes | 4 | 4 | ✓ |
| 4 | Replicate Cog custom model deployment | replicate | cloud-compute/pipeline | ▸ reproduced | ✅ yes | 4 | 3 | ✓ |
| 6 | Cloud worker pipeline architecture (input/output contract) | custom | cloud-compute/pipeline | · community | ✅ yes | 5 | 5 | ✓ |
| 6 | Hugging Face Inference Endpoints (managed HF model deploy) | huggingface | cloud-compute/pipeline | ▸ reproduced | ✅ yes | 3 | 3 | ✓ |

## Detail

### ComfyUI-as-serverless pattern (platform-agnostic) · `recommended` · ▸ reproduced
**ComfyUI's API mode serializes any node graph as a JSON workflow that can be POSTed to a serverless endpoint on any platform — RunPod, Modal, or fal — making the studio's local graph the portable unit of work rather than a platform-specific script.**
ComfyUI exposes an API mode (--listen flag) that converts the node-editor graph to a JSON workflow file. This JSON is the portable artifact: it encodes model checkpoints (by filename), LoRA stacks, sampler settings, controlnet inputs, image seeds, and output nodes. On RunPod the worker-comfyui Docker image accepts this JSON directly. On Modal the studio can mount a ComfyUI environment and POST the same JSON to a local ComfyUI server running inside the container. On fal a custom fal.App can do the same. The workflow JSON is versioned in the repo; a CI step can POST it to whichever cloud backend is configured, making the graph a reproducible, platform-switchable pipeline step. Model weights in the worker are either baked into the Docker image or loaded from a mounted volume/Network Volume to avoid per-cold-start download cost.
- **For the pipeline:** Export animation/repaint ComfyUI graphs from the local RTX 5090 rig in API JSON mode, commit them to the repo, and use them as the payload for cloud workers. This makes the graph the source of truth — not a script that re-creates the graph. When switching cloud providers, only the HTTP adapter changes. Bake model weights into the worker image for cold-start predictability; use Network Volumes / mounted volumes for experimental models not yet frozen.
- **Engine:** custom · **Applies to:** cloud-compute|pipeline · **Kind:** workflow
- **VRAM:** n/a — cloud (worker targets H100/H200/B200 for large animation models)
- **Output license:** commercial **yes** (license: n/a — workflow pattern (ComfyUI itself is GPL-3.0; the JSON workflow output is not covered by GPL)) — The ComfyUI JSON workflow format is the portable artifact; the platform executing it is commercial SaaS. Model outputs are governed by the model license, not by ComfyUI or the cloud platform. GPL-3.0 on ComfyUI source does not restrict the images you generate with it.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| ComfyUI API mode: --listen flag; workflow exported as JSON from Save (API Format) button |  | ○ |  |
| RunPod: worker-comfyui accepts JSON workflow directly via POST /run or /runsync |  | ○ |  |
| Modal/fal: run ComfyUI server inside container, POST JSON workflow to localhost:8188/prompt |  | ○ |  |
| Model weight strategy: bake into Docker image for stable models; Network Volume / mounted volume for experimental |  | ○ |  |
| Workflow JSON versioned in repo; CI/CD POSTs to configured cloud backend |  | ○ |  |

- **Best for:** Make the ComfyUI node graph the portable, versioned unit of work across cloud backends (-, fit -) ; Eliminate platform lock-in by keeping the graph as the source of truth (-, fit -) ; CI/CD integration: POST workflow JSON to cloud worker as a pipeline step (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Deploy ComfyUI on Serverless — RunPod Tutorial](https://docs.runpod.io/tutorials/serverless/comfyui) (RunPod, 2025) — ComfyUI workflows submitted as JSON to a RunPod serverless endpoint execute the graph and return outputs as base64 or S3 URL — confirming JSON-workflow portability as the integration mechanism. ; [Automate AI Image Workflows with ComfyUI + Flux on RunPod](https://www.runpod.io/articles/guides/comfy-ui-flux) (RunPod, 2025) — ComfyUI's API format (exported JSON workflow) is the payload consumed by RunPod serverless workers, enabling automated pipelines that POST a graph and receive generated images.

### Modal custom Python pipeline on H100/H200/B200 · `recommended` · ▸ reproduced
**Modal lets the studio run an arbitrary Python animation pipeline (not just ComfyUI) on data-center GPUs from A100 through B200 — with multi-GPU support up to 8× — using a decorator-driven API that keeps infrastructure versioned alongside code.**
Modal is the cleanest 'run my own pipeline on bigger GPUs' path: define a Python function, decorate it with @app.function(gpu='H100') or a fallback list like @app.function(gpu=['H100','A100-80GB:2']), and Modal builds the container, allocates the GPU, and returns results. The B200 offers 192 GB HBM3e at $0.001736/s (~$6.25/hr); H100 is $0.001097/s (~$3.95/hr); A100 80 GB is $0.000694/s (~$2.50/hr). Multi-GPU containers are supported: up to 8× on H100, H200, A100, B200 (up to 1,536 GB total). Billing is per-second from function invocation to return. The Starter plan includes $30/month free credits; the free-tier concurrency cap is 10 GPUs.
- **For the pipeline:** Best choice when the studio needs to run custom Python — a bespoke diffusion sampler loop, a video interpolation model not packaged for ComfyUI, or a multi-stage animation pipeline. Code + GPU spec live in the same file, making the pipeline a first-class versioned repo artifact. Use H100 or B200 for models that need 80–192 GB; use gpu= fallback lists to reduce queue wait.
- **Engine:** modal · **Applies to:** cloud-compute|pipeline · **Kind:** service
- **VRAM:** n/a — cloud (A100-40 GB through B200 192 GB; multi-GPU up to 8×)
- **Output license:** commercial **yes** (license: Commercial SaaS — per-second GPU compute) — Modal is a commercial compute platform; no output license is imposed by Modal. The OUTPUT's license is governed by the model running inside the container (e.g., HunyuanVideo, Wan2.1, CogVideoX). Review each model's license before using outputs in a shipped commercial game.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| GPU classes: T4 ($0.000164/s), A10 ($0.000306/s), A100-40GB ($0.000583/s), A100-80GB ($0.000694/s), L40S ($0.000542/s), H100 ($0.001097/s), RTX PRO 6000 ($0.000842/s), H200 ($0.001261/s), B200 ($0.001736/s) |  | ○ |  |
| Multi-GPU: up to 8× per container on H100/H200/A100/B200 (up to 1,536 GB GPU RAM); A10 up to 4× |  | ○ |  |
| GPU fallback syntax: @app.function(gpu=['H100', 'A100-80GB:2']) — allocates preferred first |  | ○ |  |
| Free tier: $30/month credits, Starter plan, 10 GPU concurrency |  | ○ |  |
| Cold start: container build on first deploy; subsequent calls reuse warm runners |  | ○ |  |

- **Best for:** Run bespoke Python animation/video-diffusion pipelines not wrapped in ComfyUI (-, fit -) ; Multi-GPU inference for large video generation models (HunyuanVideo, Wan2.1, CogVideoX) (-, fit -) ; Versioned pipeline-as-code: GPU spec + model + sampler config live in the repo (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Modal Pricing](https://modal.com/pricing) (Modal, 2025) — Per-second GPU billing: T4 $0.000164/s, A100-40GB $0.000583/s, A100-80GB $0.000694/s, H100 $0.001097/s, H200 $0.001261/s, B200 $0.001736/s. Starter plan: $30/month free credits, 0 base cost. ; [GPU acceleration — Modal Docs](https://modal.com/docs/guide/gpu) (Modal, 2025) — GPU types T4 through B200 supported; multi-GPU up to 8× on H100/H200/A100/B200 (1,536 GB max). Fallback GPU lists supported via gpu=['H100','A100-40GB:2'] syntax. @app.function(gpu='H100:8') syntax for multi-GPU. ; [How much does it cost to run NVIDIA B200 GPUs in 2025?](https://modal.com/blog/nvidia-b200-pricing) (Modal, 2025) — Modal B200 costs $0.001736/s (~$6.25/hr); 192 GB HBM3e, 8 TB/s bandwidth, ~5× H100 inference throughput for certain workloads.

### RunPod serverless ComfyUI worker · `recommended` · ▸ reproduced
**RunPod serverless runs a ComfyUI graph from a JSON workflow payload on pay-per-second GPUs — including A100, H100, H200, and B200 — letting the studio offload animation graphs that exceed the local 32 GB VRAM budget without a separate website workflow.**
Package the studio's ComfyUI animation/repaint graph into a serverless RunPod worker (custom Docker image or a pre-built variant from the runpod-workers/worker-comfyui repo, with model weights baked in or loaded from a Network Volume). The pipeline POSTs a RunPod-format JSON body containing the ComfyUI workflow, optional base64 input frames, and returns generated frames as base64 or S3 URLs. Cold starts are the primary latency tax; RunPod's FlashBoot mechanism reduces them from ~20 s to under 2 s by maintaining warm GPU pools. Workers scale to zero when idle; Flex workers incur charges from start to termination, billed per second. GPU options range from A100 (80 GB, $0.00076/s) through H100 PRO (80 GB, $0.00116/s), H200 PRO (141 GB, $0.00155/s), and B200 (180 GB, $0.00240/s).
- **For the pipeline:** The natural first offload target for any ComfyUI-shaped motion or repaint graph. Keep approved art, rigs, motion specs, and receipts in the repo; POST only the job payload. Bake model weights into the Docker image variant to eliminate per-cold-start download time. Use H100 PRO or H200 PRO when the local 32 GB ceiling blocks the animation model.
- **Engine:** runpod · **Applies to:** cloud-compute|pipeline · **Kind:** service
- **VRAM:** n/a — cloud (16–180 GB GPU classes; H100/H200/B200 for big motion models)
- **Output license:** commercial **yes** (license: Commercial SaaS — pay-per-second GPU compute) — The RunPod platform itself is a commercial compute service with no output license restrictions. The OUTPUT's license is governed entirely by the model you run inside the worker (e.g., AnimateDiff, Wan2.1, HunyuanVideo) — not by RunPod. Review the model's license before shipping game assets.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| GPU classes: A4000/A4500/3090 (16–24 GB), A100 (80 GB, $0.00076/s), H100 PRO (80 GB, $0.00116/s), H200 PRO (141 GB, $0.00155/s), B200 (180 GB, $0.00240/s) |  | ○ |  |
| Cold start (FlashBoot): typically under 2 s for warm pools; 60+ s for first-ever cold container with large model weights |  | ○ |  |
| Model caching: weights baked into Docker image variant or loaded from persistent Network Volume |  | ○ |  |
| Billing: per-second, Flex workers scale to zero; idle timeout default 5 s before scale-down |  | ○ |  |
| Input size limit: 10 MB for async /run, 20 MB for sync /runsync |  | ○ |  |

- **Best for:** Offload big ComfyUI animation/repaint/upscale graphs that exceed local 32 GB (-, fit -) ; Cloud step in: reference frame + motion spec JSON in → candidate frames + receipts out (-, fit -) ; Autoscaling batch — multiple concurrent workers for high-throughput character variant generation (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [RunPod Serverless — Overview](https://docs.runpod.io/serverless/overview) (RunPod, 2025) — Serverless pay-as-you-go GPU endpoints with custom Docker workers, ComfyUI generation from JSON workflows, cold starts, cached models, and worker scaling. Flex workers scale to zero; workers start automatically on request. ; [RunPod Serverless Pricing](https://docs.runpod.io/serverless/pricing) (RunPod, 2025) — Per-second billing; GPU classes from $0.00016/s (16 GB) through A100 80 GB at $0.00076/s, H100 PRO at $0.00116/s, H200 PRO at $0.00155/s, B200 at $0.00240/s. Idle workers incur charges up to 5 s before scale-down. ; [Deploy ComfyUI on Serverless — RunPod Tutorial](https://docs.runpod.io/tutorials/serverless/comfyui) (RunPod, 2025) — ComfyUI workflows submitted as JSON are executed on a serverless endpoint; outputs returned as base64 or S3 URL. Pre-built Docker image variants bundle FLUX, SDXL, SD3 weights. ; [runpod-workers/worker-comfyui — GitHub](https://github.com/runpod-workers/worker-comfyui) (RunPod, 2025) — Open-source RunPod ComfyUI worker: input accepts workflow JSON + optional base64 images (10/20 MB limits); output is list of generated images as base64 or s3_url. Model weights baked into Docker image variants to eliminate runtime downloads. ; [Unpacking Serverless GPU Pricing for AI Deployments](https://www.runpod.io/articles/guides/serverless-gpu-pricing) (RunPod, 2025) — FlashBoot reduces cold starts from ~20 s to under 2 s by maintaining warm GPU pools and preserving GPU state for rapid restoration.

### fal.ai serverless media API and custom deployment · `recommended` · ▸ reproduced
**fal.ai provides both a curated API for 1,000+ generative media models and a custom-app deployment path (fal.App Python class) running on H100/H200/B200 with autoscaling to zero — enabling the studio to either call a packaged animation model instantly or deploy a proprietary pipeline on the same infrastructure.**
fal.ai runs on a fleet of H100 (80 GB, from $1.89/hr), H200 (141 GB, from $2.10/hr), B200 (180 GB, from $3.49/hr), B300 (288 GB, from $4.49/hr), and RTX PRO 6000 (96 GB, from $1.10/hr) GPUs. Custom apps use the fal.App class: a setup() method loads model weights once per runner; @fal.endpoint() methods handle requests; autoscaling parameters (keep_alive, min_concurrency, max_concurrency) control cold-start/cost trade-off. Infrastructure scales to zero between jobs. The marketplace offers ready-made endpoints for video generation models (Wan2.1, HunyuanVideo, CogVideoX, etc.) callable via REST with a file URL in, file URL out pattern.
- **For the pipeline:** Strong fit for two distinct use-cases: (1) calling an already-packaged video animation model as a REST step in the pipeline — no Docker work required; (2) deploying a studio-owned Python pipeline when custom sampler logic is needed. The B200/B300 options give the highest available VRAM budget on this platform for very large models. Use min_concurrency=1 only for time-sensitive interactive runs; keep at 0 for batch to eliminate idle cost.
- **Engine:** fal · **Applies to:** cloud-compute|pipeline · **Kind:** service
- **VRAM:** n/a — cloud (H100 80 GB through B300 288 GB)
- **Output license:** commercial **yes** (license: Commercial SaaS — per-second compute) — fal is a commercial compute platform. The OUTPUT's license is governed by the model running on fal, not by fal itself. For custom deployments with studio-owned models, this is clean; for marketplace models, check each model's specific license (Apache 2.0, non-commercial, etc.) before shipping game assets.
- **Fit:** rig 4/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| GPU classes: H100 80 GB (from $1.89/hr), H200 141 GB (from $2.10/hr), B200 180 GB (from $3.49/hr), B300 288 GB (from $4.49/hr), RTX PRO 6000 96 GB (from $1.10/hr) — list prices higher, discounted prices shown |  | ○ |  |
| Custom app: fal.App class, setup() once per runner, @fal.endpoint() per route, machine_type='GPU-H100' syntax |  | ○ |  |
| Autoscaling: keep_alive (idle runner retention), min_concurrency, max_concurrency; scales to zero |  | ○ |  |
| Marketplace: 1,000+ models accessible via REST without custom deployment |  | ○ |  |

- **Best for:** Call packaged video/animation models (Wan2.1, HunyuanVideo, CogVideoX) via REST without Docker work (-, fit -) ; Deploy studio-owned Python pipeline on H100/H200/B200 with fal.App (-, fit -) ; Highest-VRAM cloud option (B300 288 GB) for models that outgrow H100 80 GB (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [fal Pricing](https://fal.ai/pricing) (fal, 2025) — GPU compute: H100 80 GB from $1.89/hr, H200 141 GB from $2.10/hr, B200 180 GB from $3.49/hr, B300 288 GB from $4.49/hr, RTX PRO 6000 96 GB from $1.10/hr. Pay-per-use billing. ; [Introduction to Serverless — fal Docs](https://fal.ai/docs/serverless) (fal, 2025) — Custom apps use fal.App Python class; setup() runs once per runner to load weights; @fal.endpoint() methods serve requests; machine_type parameter selects GPU class (GPU-H100, GPU-A100, etc.); infrastructure autoscales to zero with keep_alive, min_concurrency, max_concurrency controls.

### Replicate Cog custom model deployment · `runner-up` · ▸ reproduced
**Replicate's Cog tool packages any Python model into a production-ready container with an auto-generated API, deployable on T4 through H100 GPUs, giving the studio a fast path from a local model checkpoint to a REST endpoint callable from the pipeline.**
Cog (open-source, Apache 2.0) wraps a model's predict() function in a standard container with a generated HTTP API; push to Replicate and get a REST endpoint. Hardware ranges from T4 ($0.000225/s, $0.81/hr) through A100-80GB ($0.001400/s, $5.04/hr) and H100 ($0.001525/s, $5.49/hr); multi-GPU configurations available up to 8× H100 or A100. Private model deployments bill for all time the instance is online (setup + idle + active), except fast-booting fine-tunes which bill active-only. Setting min instances to 1 eliminates cold boot delay but adds continuous idle cost. The large library of community models (AnimateDiff, motion ControlNets, upscalers) is immediately callable via REST without deployment.
- **For the pipeline:** Good fit when the studio has a locally-trained or fine-tuned checkpoint that needs to become a pipeline REST step without building a full Docker/Modal setup. Also the fastest way to prototype using a community animation model already on Replicate. For production volume, private deployments on H100 are cost-competitive; monitor billing since private models charge idle time by default.
- **Engine:** replicate · **Applies to:** cloud-compute|pipeline · **Kind:** service
- **VRAM:** n/a — cloud (T4 16 GB through H100 80 GB, up to 8×)
- **Output license:** commercial **yes** (license: Commercial SaaS — per-second GPU compute) — Replicate is a commercial compute platform. The OUTPUT's license is governed by the specific model running on Replicate. Community models may carry non-commercial licenses (e.g., SD 1.x, some ControlNet checkpoints); always check the model card. Studio-owned models pushed via Cog produce outputs under whatever license the studio applies to the weights.
- **Fit:** rig 4/5 · studio 3/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| GPU classes: CPU ($0.000115/s), T4 ($0.000225/s, $0.81/hr), L40S ($0.000975/s, $3.51/hr), A100-80GB ($0.001400/s, $5.04/hr), H100 ($0.001525/s, $5.49/hr) |  | ○ |  |
| Multi-GPU: up to 8× H100 or A100 |  | ○ |  |
| Private model billing: setup + idle + active time (default); fast-booting fine-tunes: active-only |  | ○ |  |
| Cold start mitigation: set min_instances=1 in deployment config (adds idle cost) |  | ○ |  |
| Cog: open-source (Apache 2.0), generates REST API automatically from predict() function |  | ○ |  |

- **Best for:** Package a locally fine-tuned animation checkpoint as a REST endpoint without full Docker work (-, fit -) ; Prototype with community animation models (AnimateDiff, motion ControlNets) already on Replicate (-, fit -) ; Multi-GPU H100 inference for large video generation models (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Replicate Pricing](https://replicate.com/pricing) (Replicate, 2025) — Per-second GPU billing: T4 $0.000225/s ($0.81/hr), L40S $0.000975/s ($3.51/hr), A100-80GB $0.001400/s ($5.04/hr), H100 $0.001525/s ($5.49/hr). Multi-GPU up to 8×. Private models bill setup+idle+active; fast-booting fine-tunes bill active-only. ; [Deploy a custom model — Replicate Docs](https://replicate.com/docs/get-started/deploy-a-custom-model) (Replicate, 2025) — Cog packages arbitrary Python model code in a production container with auto-generated API; push with `cog push`; hardware upgrades (T4 → A100 → H100) require no code changes. Set min_instances=1 to avoid cold boots at the cost of continuous idle billing.

### Cloud worker pipeline architecture (input/output contract) · `recommended` · · community
**A platform-agnostic input/output contract for cloud animation workers — reference frame + 8-view turnaround + motion spec + proxy/pose + weapon layer in; candidate frames + masks + receipts (seed, config, model ID, license) out — keeps approved art and truth in the repo while cloud is purely compute.**
The studio's cloud animation job has a defined shape regardless of which platform runs it. Input bundle: approved reference frame (base64 or signed URL), 8-view character turnaround (signed URL or repo artifact ID), motion spec JSON (animation curve / proxy keyframes / duration / fps), optional pose/proxy overlay, optional weapon/accessory layer. The cloud worker runs the animation/repaint model and returns: candidate frames (base64 or S3 URL per frame), per-frame alpha masks, and a receipt JSON containing seed, sampler config, model identifier, model license string, and timestamp. The receipt is committed to the repo alongside the approved frame to make the pipeline reproducible and auditable. No source-of-truth assets (rigs, approved art, motion specs) ever live in the cloud worker — only the job.
- **For the pipeline:** Implement this contract as the adapter layer between the pipeline orchestrator (local repo + CI) and any cloud backend (RunPod, Modal, fal, Replicate). Because the receipt travels with every output, the studio can always re-run the exact job from the repo. The weapon layer as a separate input enables safe compositing without re-running the full character animation. Swap cloud backends by swapping the adapter; the pipeline contract stays stable.
- **Engine:** custom · **Applies to:** cloud-compute|pipeline · **Kind:** workflow
- **VRAM:** n/a — cloud
- **Output license:** commercial **yes** (license: n/a — architecture pattern) — The architecture pattern itself carries no license. The outputs produced by running this pattern inherit the license of the model executed by the cloud worker. Receipts must capture the model license string to support future audits.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| Input: reference_frame (base64/URL), turnaround_views (8-view, URL/artifact-id), motion_spec (JSON: keyframes/duration/fps), pose_overlay (optional), weapon_layer (optional) |  | ○ |  |
| Output: candidate_frames[] (base64/URL per frame), masks[] (per-frame alpha), receipt {seed, sampler_config, model_id, model_license, timestamp} |  | ○ |  |
| Receipt committed to repo alongside approved output for reproducibility |  | ○ |  |
| No source-of-truth assets stored in cloud worker — cloud is stateless compute only |  | ○ |  |

- **Best for:** Define the canonical pipeline input/output contract for all cloud animation workers (-, fit -) ; Ensure every cloud job is reproducible from the repo via the receipt (-, fit -) ; Separate approved art / rigs / motion specs (repo) from compute (cloud) (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [RunPod Serverless — worker-comfyui input/output schema](https://github.com/runpod-workers/worker-comfyui) (RunPod, 2025) — RunPod ComfyUI worker accepts workflow JSON + base64 input images; returns images as base64 or s3_url list — establishing the practical JSON-in / file-out pattern this architecture generalizes.

### Hugging Face Inference Endpoints (managed HF model deploy) · `situational` · ▸ reproduced
**Hugging Face Inference Endpoints deploys any HF Hub model (or a custom container) as a managed, autoscaling REST endpoint on AWS or GCP GPU instances — from T4 through H200 — billed by the minute per active replica.**
Inference Endpoints is optimized for models already on the HF Hub: point at a repo, select a GPU instance, and HF manages the container (TGI, vLLM, SGLang, TEI, or a custom image). AWS GPU options span nvidia-t4-x1 ($0.50/hr), nvidia-a10g-x1 ($1.00/hr), nvidia-a100-x1 ($2.50/hr), nvidia-h200-x1 ($5.00/hr), with multi-GPU variants up to ×8. GCP adds nvidia-h100 (×1–×8, $10–$80/hr). Autoscaling sets min/max replica counts; min=1 prevents cold starts (continuous billing); min=0 (scale-to-zero) is possible but adds ~20-30 s warm-up latency. Custom containers allow non-Transformers models or bespoke inference logic. Billing is by the minute at the instance rate times active replica count.
- **For the pipeline:** Best fit when the animation or video model is already published on the HF Hub and the studio wants to avoid packaging Docker images from scratch. Less flexible than Modal/fal for custom Python pipelines, but the fastest path for running an HF model at scale. Pin the endpoint to a specific revision commit so the studio's pipeline always runs the exact approved model weights.
- **Engine:** huggingface · **Applies to:** cloud-compute|pipeline · **Kind:** service
- **VRAM:** n/a — cloud (T4 14 GB through H200 141 GB ×8 = 1,128 GB, AWS/GCP)
- **Output license:** commercial **yes** (license: Commercial SaaS — per-minute GPU compute) — Hugging Face Inference Endpoints is a commercial compute service. The OUTPUT's license is governed by the model's HF Hub license (Apache 2.0, CC-BY-NC, etc.), not by HF as a platform. Many video generation models on HF Hub carry non-commercial licenses; verify the model card before using outputs in a shipped commercial game.
- **Fit:** rig 3/5 · studio 3/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| AWS GPU instances: nvidia-t4-x1 $0.50/hr (14 GB), nvidia-l4-x1 $0.80/hr (24 GB), nvidia-a10g-x1 $1.00/hr (24 GB), nvidia-a100-x1 $2.50/hr (80 GB), nvidia-h200-x1 $5.00/hr (141 GB), nvidia-h200-x8 $40/hr (1,128 GB) |  | ○ |  |
| GCP GPU instances: nvidia-t4-x1 $0.50/hr, nvidia-a100-x1 $3.60/hr, nvidia-h100-x1 $10.00/hr, nvidia-h100-x8 $80/hr |  | ○ |  |
| Autoscaling: min ≥ 0 replicas (0 = scale-to-zero), max configurable; warm-up from zero ~20-30 s |  | ○ |  |
| Custom containers: Docker Hub, AWS ECR, Azure ACR, Google GCR; use for non-Transformers models |  | ○ |  |
| Revision pinning: target specific HF Hub commit for reproducible inference |  | ○ |  |
| Billing: per-minute, cost = instance hourly rate × active replicas ÷ 60 |  | ○ |  |

- **Best for:** Deploy an HF Hub animation/video model (Wan2.1, AnimateDiff, etc.) without building Docker images (-, fit -) ; Multi-GPU H200/H100 inference via managed endpoint with HF's TGI/vLLM serving layer (-, fit -) ; Custom container path for non-Transformers pipeline on managed HF infrastructure (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Inference Endpoints Pricing — Hugging Face](https://huggingface.co/docs/inference-endpoints/en/pricing) (Hugging Face, 2025) — AWS: nvidia-t4-x1 $0.50/hr, nvidia-a100-x1 $2.50/hr, nvidia-h200-x1 $5.00/hr, nvidia-h200-x8 $40/hr. GCP: nvidia-h100-x1 $10.00/hr, nvidia-h100-x8 $80/hr. Billed by the minute, cost = instance rate × active replicas. ; [Advanced Setup (Instance Types, Auto Scaling, Versioning) — Hugging Face Inference Endpoints](https://huggingface.co/docs/inference-endpoints/guides/advanced) (Hugging Face, 2025) — Autoscaling via min/max replica counts; custom containers supported (Docker Hub, AWS ECR, Azure ACR, GCR); revision pinning to specific HF Hub commit for reproducibility; custom container use-case: non-Transformers models or bespoke inference handlers.

